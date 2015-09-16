import sqlite3 as lite
import csv

'''
Convert house information records in a CSV file to SQLite DB
Table columns: id,street,status,price,bedrooms,bathrooms,sq_ft,lat,lng
Raw data: https://s3.amazonaws.com/opendoor-problems/listings.csv
Run: python cvs2sqlite.py
'''
def main():
    house_info = []
    with open('listings/data/listings.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            house_info.append(
                (
                    row['id'],
                    row['street'],
                    row['status'],
                    int(row['price']),
                    int(row['bedrooms']),
                    int(row['bathrooms']),
                    int(row['sq_ft']),
                    float(row['lat']),
                    float(row['lng']),
                )
            )
    with lite.connect('opendoor.db') as con:
        cur = con.cursor()
        cur.executemany(
            "INSERT INTO listings_house VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
            house_info
        )

        # Verify data
        cur.execute("SELECT * FROM listings_house")
        all_records = cur.fetchall()
        assert len(all_records) == len(house_info)
        print('Inserted {} records into opendoor.db.listings_house'.format(
            len(all_records)
        ))

if __name__ == "__main__":
    main()
