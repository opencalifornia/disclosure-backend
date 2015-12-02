"""
Command to download and load California campaign finance data from Netfile.
"""

import os
import csv
import cStringIO
import codecs
import glob
import re

from calaccess_raw import get_download_directory
from calaccess_raw.management.commands import loadcalaccessrawfile
from django.db import connection
from optparse import make_option

from netfile.connect2_api import Connect2API


custom_options = (
    make_option(
        "--skip-download",
        action="store_true",
        dest="skip_download",
        default=False,
        help="Skip downloading of the raw data"
    ),
    make_option(
        "--skip-combine",
        action="store_true",
        dest="skip_combine",
        default=False,
        help="Skip combining of the downloaded data"
    ),
    make_option(
        "--skip-load",
        action="store_true",
        dest="skip_load",
        default=False,
        help="Skip loading up the raw data files"
    ),
)

class UnicodeDictWriter(object):
    """
    A CSV DictWriter which will write rows to CSV file "f",
    which is encoded in the given encoding.

    Adapted from https://docs.python.org/2/library/csv.html#examples
    """
    def __init__(self, f, headers, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, headers, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writeheader(self):
        self.writer.writeheader()

    def writerow(self, row):
        utf8_row = dict()
        for k, v in row.iteritems():
            utf8_row[k] = codecs.encode(unicode(v), 'utf-8')

        self.writer.writerow(utf8_row)
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


class Command(loadcalaccessrawfile.Command):
    help = 'Download and load the Netfile raw data'
    option_list = loadcalaccessrawfile.Command.option_list + custom_options
    # netfile gives us ISO8601 formatted dates, so we have to override the
    # calaccess_raw date hack with a slightly different one :)
    date_sql = "DATE_FORMAT(str_to_date(@`%s`, '%%Y-%%m-%%d'), '%%Y-%%m-%%d')"

    def handle(self, *args, **options):
        self.verbosity = int(options['verbosity'])
        self.max_lines_per_load = int(options.get('max_lines_per_load', 1000))
        self.data_dir = os.path.join(get_download_directory(), 'csv')
        self.combined_csv_path = os.path.join(
            self.data_dir, 'netfile_cal201_transaction.csv')
        self.connect2 = Connect2API()

        if not options['skip_download']:
            self.download()

        if not options['skip_combine']:
            self.combine()

        if not options['skip_load']:
            self.cursor = connection.cursor()
            self.load()

    def combine(self):
        headers_written = False
        fname_pattern = re.compile('netfile_\d{4}_(.+)_cal201')
        #                                          ^^ Agency shortcut in filename 
        with file(self.combined_csv_path, 'w') as combined_csv:
            for path in glob.glob(os.path.join(self.data_dir, 'netfile_*_*_cal201_export.csv')):
                agency_shortcut = fname_pattern.search(path).group(1)
                with file(path, 'r') as agency_csv:
                    headers = ','.join(
                        ['agency_shortcut', agency_csv.readline()])
                    if not headers_written:
                        combined_csv.write(headers)
                        headers_written = headers
                    else:
                        # make sure things don't go all wierd between files.
                        assert headers == headers_written
                    for line in agency_csv.readlines():
                        combined_csv.write(','.join([agency_shortcut, line]))


    def download(self):
        if self.verbosity:
            self.header("Downloading raw data files")

        if not os.path.isdir(self.data_dir):
            os.makedirs(self.data_dir)

        # Fetch agencies
        agencies = self.fetch_agencies()
        print "Found %s agencies" %  (len(agencies))
        self._write_csv('netfile_agency.csv', iter(agencies))

        for agency in agencies:

            for year in ['2014','2015']:
                csv_path = 'netfile_%s_%s_cal201_export.csv' % (year, agency['shortcut'])
                transactions = self.fetch_transactions_agency_year(agency, year)
                self._write_csv(csv_path, transactions)


    def load(self):
        if self.verbosity:
            self.header("Loading Agency CSV file")
        super(Command, self).load('NetFileAgency', app='netfile')
        if self.verbosity:
            self.success("ok.")
        if self.verbosity:
            self.header("Loading Cal201 Transaction Data")
        super(Command, self).load('NetFileCal201Transaction', app='netfile')
        if self.verbosity:
            self.success("ok.")


    def _write_csv(self, csv_path, iterator):
        if self.verbosity:
            self.log('Writing %s...' % (csv_path))

        try:
            item = iterator.next()
        except StopIteration:
            self.failure('No data')
            return

        with open(os.path.join(self.data_dir, csv_path), 'w') as csv_handle:
            headers = item.keys()
            writer = UnicodeDictWriter(csv_handle, headers)
            writer.writeheader()
            writer.writerow(item)
            for item in iterator:
                writer.writerow(item)

        if self.verbosity:
            self.success('OK')


    def fetch_transactions_agency_year(self, agency, year):
        # Break this up by transaction type?
        query = {
            'Aid': agency['id'],
            'Year': year,
            'sortOrder': 1, # DateDescending
            }

        return self.connect2.postpubliccampaignexportcal201transactionyear(query)


    def fetch_agencies(self):
        """Fetches agencies from Netfile API"""
        return self.connect2.getpubliccampaignagencies()
