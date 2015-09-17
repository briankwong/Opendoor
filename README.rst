Take Home Problem: Listings
====================================

Prerequisite
------------------------------------
This simple project is developed based on ``Django Framework``
and ``Django REST Framework``:

.. code-block:: bash

    sudo pip install django
    sudo pip install djangorestframework
    sudo pip install django-filter

Folder Organization
------------------------------------
* ``TakeHomeProblem``: project settings
* ``listings``: source codes for ``listings`` server
    ** ``validator``: verify that results are GeoJSON compatible
        ***  ``library/geojson``: adapted ``geojson 1.3.0``
* ``cvs2sqlite.py``: process raw house info and populate the database

DataStore (SQLite)
------------------------------------
Raw data: https://s3.amazonaws.com/opendoor-problems/listings.csv

A local copy is stored in ``listings/data/listings.csv``

Raw data has been migrated to ``listings_house`` in ``opendoor.db``:

.. code-block:: bash

    python manage.py migrate
    python manage.py makemigrations listings
    python manage.py sqlmigrate listings 0001
    python cvs2sqlite.py

The schema of ``listings_house`` is defined in ``listings/migrations/0001_initial.py``,
which is auto-generated from ``listings/models.py``.

Notice that ``listings_house`` is indexed on ``id``. So if you run ``python cvs2sqlite.py``
again, you will get errors like ``sqlite3.IntegrityError: UNIQUE constraint failed: listings_house.id``.

Run Server
------------------------------------
In command line, run:

.. code-block:: bash

    python manage.py runserver [port]

The default value of ``port`` is ``8000``.

Client Side Query
------------------------------------
Example URL: ``http://127.0.0.1:[port]/listings?min_price=100000&max_price=200000&min_bed=2&max_bed=2&min_bath=2&max_bath=2``

* min_price: The minimum listing price in dollars
* max_price: The maximum listing price in dollars
* min_bed: The minimum number of bedrooms
* max_bed: The maximum number of bedrooms
* min_bath: The minimum number of bathrooms
* max_bath: The maximum number of bathrooms

All query parameters are optional, and all minimum and maximum fields are
inclusive (e.g. ``min_bed=2&max_bed=4`` should return houses with 2, 3, or 4 bedrooms).
Data are **read-only** for unauthorized clients.

Example result:

.. code-block:: python

    {
        "type": "FeatureCollection",
        "count": 431,
        "next": "http://127.0.0.1:8000/listings?max_bath=2&max_bed=2&max_price=200000&min_bath=2&min_bed=2&min_price=100000&page=3",
        "previous": "http://127.0.0.1:8000/listings?max_bath=2&max_bed=2&max_price=200000&min_bath=2&min_bed=2&min_price=100000",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        33.437859864651166,
                        -112.03801896441065
                    ]
                },
                "properties": {
                    "status": "active",
                    "bathrooms": 2,
                    "sq_ft": 1942,
                    "price": 110872,
                    "bedrooms": 2,
                    "street": "442 1st Cir",
                    "id": "1226"
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        33.48658345749951,
                        -112.1183982309859
                    ]
                },
                "properties": {
                    "status": "active",
                    "bathrooms": 2,
                    "sq_ft": 1292,
                    "price": 196307,
                    "bedrooms": 2,
                    "street": "685 5th Ave",
                    "id": "1243"
                }
            },
            ...
        ]
    }

To verify the result is GeoJSON compatible, please run:

.. code-block:: bash

    python listings/validator/validator.py <URL> (e.g., 'http://127.0.0.1:8000/listings?max_bath=2')

Pagination
------------------------------------
Results are paginated via web linking with ``page_size = 50``. You can follow
``previous`` or ``next`` links in results to navigate through pages.

To edit the default page size, please update ``TakeHomeProblem/settings.py``:

.. code-block:: python

    REST_FRAMEWORK = {
        ...
        'PAGE_SIZE': 50
    }

Admin Page
------------------------------------
Page: http://127.0.0.1:[port]/admin

You can manage authentication and authorization of this website,
and add/update/delete house info in the database in the admin page.

* User name: admin
* Password: 123456
