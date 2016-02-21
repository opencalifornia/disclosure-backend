[![Build
Status](https://travis-ci.org/caciviclab/disclosure-backend.svg?branch=master)](https://travis-ci.org/caciviclab/disclosure-backend)
[![Coverage Status](https://coveralls.io/repos/caciviclab/disclosure-backend/badge.svg?branch=master&service=github)](https://coveralls.io/github/caciviclab/disclosure-backend?branch=master)

California Civic Lab Disclosure Backend
==================================================

## Overview

This is the back-end Django application for scraping ballot measure funding data (from NetFile and CalAccess), pushing it to our database, and exposing the data to our front-end apps via a RESTful API.

Helpful links:
* [How to contribute](CONTRIBUTING.md) - links to the overall app technical design and status, as well as information on how to contribute ocde.
* [Adding your city](https://github.com/caciviclab/caciviclab.github.io/wiki/On-boarding-a-new-city) - How to test and add your city's disclosure information to this app.
* [Example Dataset](https://data.oaklandnet.com/dataset/Campaign-Finance-FPPC-Form-460-Schedule-A-Monetary/3xq4-ermg) - This is a sample Form 460 for Oakland. If you want to dive into the data, please check this out!

See below for server setup. Here are mock-ups for data tables that this app intends to support:

-[![Mockup](/mockups/odca-mobile-09-ballot_measure-small.jpeg)](/mockups/odca-mobile-09-ballot_measure.jpeg)
-[![Mockup](/mockups/odca-mobile-09-ballot_measure 2-small.jpeg)](/mockups/odca-mobile-09-ballot_measure 2.jpeg)
-[![Mockup](/mockups/odca-mobile-09-ballot_measure 3-small.jpeg)](/mockups/odca-mobile-09-ballot_measure 3.jpeg)
-[![Mockup](/mockups/odca-mobile-09-ballot_measure 4-small.jpeg)](/mockups/odca-mobile-09-ballot_measure 4.jpeg)
-[![Mockup](/mockups/odca-mobile-09-ballot_measure 5-small.jpeg)](/mockups/odca-mobile-09-ballot_measure 5.jpeg)
-[![Mockup](/mockups/odca-mobile-09-ballot_measure 6-small.jpeg)](/mockups/odca-mobile-09-ballot_measure 6.jpeg)
-[![Mockup](/mockups/odca-mobile-09-ballot_measure 7-small.jpeg)](/mockups/odca-mobile-09-ballot_measure 7.jpeg)
-[![Mockup](/mockups/odca-mobile-09-ballot_measure 8-small.jpeg)](/mockups/odca-mobile-09-ballot_measure 8.jpeg)

## Setting up the app.

If you've worked with Django and python before, these steps should be familiar to you.
We're going to create an environment with Python 2.7.9 for the project


### Software Installation

0. Clone `disclosure-backend` (or your fork of it) to your own local copy.
1. Install `python` and `pip` (if using Anaconda, pip is already installed)
2. Create an environment for this project:
  * For non-Anaconda Python distribution
    ```
    sudo pip install virtualenv
    virtualenv env
    source env/bin/activate
    ```

  * For Anaconda (we'll make an environment called ODB with Python 2.7.9 in it)
    ```
    conda create --name ODB python=2.7.9
    source activate ODB
    ```

  (you will have to activate this environment (or virtualenv) every time you want to start working)

3. Install mysql and other system dependencies

  OSX:
   ```
   brew install mysql
   brew install libssl
   brew install graphviz
   ```
  * When prompted for a password, remember it because you'll need it.

4. Install project requirements with:
   ```
   pip install -r requirements.txt
   pip install -r requirements_dev.txt
   ```


### Database setup

1. Create the database
  ```
  mysql -p --user root
  mysql> create database opendisclosure;
  mysql> create database calaccess_raw;
  mysql> \q
  ```

2. Create `disclosure/settings_local.py`

  ```
  DATABASES['default']['PASSWORD'] = ''  # replace with your password.
  DATABASES['calaccess_raw']['PASSWORD'] = ''  # replace with your password.
  ```

  Change the password field to the password you chose when you installed MySQL.


3. Run the database migration scripts
  ```
  python manage.py migrate
  python manage.py migrate --database calaccess_raw
  ```

  OSX: If you get the following error `django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module: dlopen(_mysql.so, 2): Library not loaded: libssl.1.0.0.dylib`

  Then, you need to add openssl to your `DYLD_LIBRARY_PATH`:
  1. Go to `/usr/local/Cellar/openssl/`, and locate your directory (e.g. 1.0.2d_1)
  2. Add the following to your `~/.bash_profile`:
   ```
   export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:/usr/local/Cellar/openssl/1.0.2d_1/lib
   ```

### Validate your install

#### Run the tests

```
python manage.py test
```

It should load and clean some files in a few seconds.

Note: if this fails with an SSL error and you are using conda/miniconda, use virtualenv instead. See [this link](https://groups.google.com/a/continuum.io/forum/#!topic/conda/Fqv93VKQXAc) for details about the conda issue.

#### Run with test data

A basic data check to make sure things are working:

```
python manage.py downloadcalaccessrawdata --use-test-data
```


### Download and load the data

```
python manage.py load_aliases  # Load known variations in city names.
python manage.py downloadnetfilerawdata --agencies CSD,COAK,SFO --years 2014,2015  # download the csv files
python manage.py xformnetfilerawdata --agencies CSD,COAK,SFO --years 2014,2015  # process the csv files
```


### Run the server

To run for the purposes of development, accessing Django's admin interface:

```
python manage.py createsuperuser  # create a username/password for yourself
python manage.py runserver
```

Then go to http://127.0.0.1:8000/admin to log in and see data.


## Deploying the app

For deployment to the official website:

```
ssh opencal.opendisclosure.io /usr/local/bin/deploy-backend
```
