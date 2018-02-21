[![Waffle.io - Columns and their card count](https://badge.waffle.io/caciviclab/disclosure-backend.png?columns=all)](https://waffle.io/caciviclab/disclosure-backend?utm_source=badge)
[![Build
Status](https://travis-ci.org/caciviclab/disclosure-backend.svg?branch=master)](https://travis-ci.org/caciviclab/disclosure-backend)
[![Coverage Status](https://coveralls.io/repos/caciviclab/disclosure-backend/badge.svg?branch=master&service=github)](https://coveralls.io/github/caciviclab/disclosure-backend?branch=master)

California Civic Lab Disclosure Backend
==================================================

## Overview

This is the back-end Django application for scraping ballot measure funding
data (from NetFile and CalAccess), pushing it to our database, and exposing the
data to our front-end apps via a RESTful API.

Helpful links:
* [How to contribute](CONTRIBUTING.md) - links to the overall app technical
  design and status, as well as information on how to contribute ocde.
* [Adding your city][adding]
  \- How to test and add your city's disclosure information to this app.
* [Example Dataset][example_data]
  \- This is a sample Form 460 for Oakland. If you want to dive into the data,
  please check this out!

See below for server setup.

Mock-ups for data tables that this app intends to support are here:
https://github.com/caciviclab/caciviclab.github.io/wiki/Mock-ups


## Setting up the app.

If you've worked with Django and python before, these steps should be familiar
to you.  We're going to create an environment with Python 2.7.9 for the project


### Software Installation

0. Clone `disclosure-backend` (or your fork of it) to your own local copy.

1. Install `python` or `anaconda` or `conda`  (If using OSX (Mac) python is
   already installed, if using Linux, install anaconda, if using Windows, you
   can choose between conda and python but we recommend python)
 * [Anaconda Distribution] (https://docs.continuum.io/anaconda/install)
 * [Python Distribution - Windows] (http://www.howtogeek.com/197947/how-to-install-python-on-windows/) - install version 2.7.9

2. Install `pip` (if using Anaconda, pip is already installed.)
    ```
    sudo easy_install pip
    ```
 
3. Create an environment for this project:
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

  You will have to activate this environment (or virtualenv) every time you want to start working. You activate using:
 ```
 source env/bin/activate
 ```
 Or
 ```
 source activate ODB
 ```

4. Install mysql and other system dependencies

  OSX:
   ```
    brew install pkg-config
    pkg-config --cflags-only-I libcgraph
 
    brew install mysql
    brew install libssl
    brew install graphviz
   ```
  * If ```brew install libssl``` does not work don't worry about it.
  * When prompted for a password, remember it because you'll need it.

5. Install project requirements with:
   ```
   pip install -r requirements.txt
   pip install -r requirements_dev.txt
   ```
  * Did you encounter an error that says something like  ` fatal error: 'graphviz/cgraph.h' file not found` ? 
    Run
 
    ```
    cd /usr/local/Cellar/graphviz/2.38.0/include/graphviz/
    mkdir graphviz
    cp cgraph.h graphviz/
    ```
 
    Then try
 
    ```
    pip install -r requirements_dev.txt
    ```

### Database setup

1. Create the database
  ```
  mysql -u root
  mysql> create database opendisclosure;
  mysql> create database calaccess_raw;
  mysql> \q
  ```

2. Run the server setup script
  ```
  python manage.py setuptestserver
  ```

  This will run database migrations, add a superuser (username: `admin`, password: `admin`),
  and other setup steps.

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


### Download data

#### Zipcode/metro data

```
python manage.py downloadzipcodedata
```

#### Netfile

Netfile contains campaign finance data for a number of jurisdictions. Not all
jurisdictions will have data.

```
# Download netfile data and load into calaccess_raw.NETFILE_CAL201_TRANSACTION
python manage.py downloadnetfilerawdata
# Process NETFILE_CAL201_TRANSACTION into opendisclosure
python manage.py xformnetfilerawdata
```


### Run the server

To run for the purposes of development, accessing Django's admin interface:

```
python manage.py runserver
```

Then go to http://127.0.0.1:8000/admin to log in and see data.


## Deploying the app

For deployment to the official website:

```
ssh opencal.opendisclosure.io /usr/local/bin/deploy-backend
```

[adding]: https://github.com/caciviclab/caciviclab.github.io/wiki/On-boarding-a-new-city
[example_data]: https://data.oaklandnet.com/dataset/Campaign-Finance-FPPC-Form-460-Schedule-A-Monetary/3xq4-ermg
