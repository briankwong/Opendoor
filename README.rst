Opendoor Take Home Problem: listings
====================================

Prerequisite
------------------------------------
This project is developed based on ``Django Framework`` and ``Django REST Framework``:

.. code-block:: bash

    sudo pip install django
    sudo pip install djangorestframework
    sudo pip install django-filter

DataStore
------------------------------------
Raw data: https://s3.amazonaws.com/opendoor-problems/listings.csv

A local copy is stored in ``listings/data/listings.csv``

Raw data has been migrated to Table ``listings_house`` in ``opendoor.db``:

.. code-block:: bash

    python manage.py migrate
    python manage.py makemigrations listings
    python manage.py sqlmigrate listings 0001
    python cvs2sqlite.py

Table ``listings_house`` definition:

.. code-block:: python

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('street', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=40)),
                ('price', models.IntegerField()),
                ('bedrooms', models.IntegerField()),
                ('bathrooms', models.IntegerField()),
                ('sq_ft', models.IntegerField()),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
            ],
        ),
    ]

Notice that ``listings_house`` is indexed on ``id``. So if you run ``python cvs2sqlite.py``
again, you will get errors like ``sqlite3.IntegrityError: UNIQUE constraint failed: listings_house.id``.

Run Server
------------------------------------
In command line, run:

.. code-block:: bash

    python manage.py runserver

Usage
------------------------------------
URL: ``http://127.0.0.1:8000?listings?min_price=100000&max_price=200000&min_bed=2&max_bed=2&min_bath=2&max_bath=2``

.. code-block:: python

    min_price: 'The minimum listing price in dollars'
    max_price: 'The maximum listing price in dollars'
    min_bed: 'The minimum number of bedrooms'
    max_bed: 'The maximum number of bedrooms'
    min_bath: 'The minimum number of bathrooms'
    max_bath: 'The maximum number of bathrooms'

All query parameters are optional, all minimum and maximum fields are
inclusive (e.g. ``min_bed=2&max_bed=4`` should return listings with 2, 3, or 4 bedrooms).

.. code-block:: python

    {
        "type": "FeatureCollection",
        "count": 431,
        "next": "http://127.0.0.1:8000/listings?format=api&max_bath=2&max_bed=2&max_price=200000&min_bath=2&min_bed=2&min_price=100000&page=2",
        "previous": null,
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        33.45170447351804,
                        -112.20395000768927
                    ]
                },
                "properties": {
                    "status": "sold",
                    "bathrooms": 2,
                    "sq_ft": 2279,
                    "price": 181554,
                    "bedrooms": 2,
                    "street": "389 2nd Dv",
                    "id": "19"
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        33.568740034923174,
                        -112.15817982971032
                    ]
                },
                "properties": {
                    "status": "pending",
                    "bathrooms": 2,
                    "sq_ft": 3145,
                    "price": 157020,
                    "bedrooms": 2,
                    "street": "566 Walnut Ave",
                    "id": "85"
                }
            },
            ...
        ]
    }

Pagination
------------------------------------
Result is paginated via web linking with ``page_size = 50``. To edit the page size,
please update ``TakeHomeProblem/settings.py``

.. code-block:: python

    REST_FRAMEWORK = {
        ...
        'PAGE_SIZE': 50
    }

Admin Page
------------------------------------
Page: http://127.0.0.1:8000/admin
You can manage authentication and authorization of this website,
and add/update/delete house records in the database.

User name: admin
Password: 123456
