import pymysql
from sqlalchemy import create_engine, MetaData, Table, insert, select
from sqlalchemy.exc import IntegrityError
import json

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',  # Update to your DB host
    'port': 3306,         # Update to your DB port if necessary
    'user': 'your_user',  # Replace with your DB username
    'password': 'your_password',  # Replace with your DB password
    'database': 'your_database_name'  # Replace with your DB name
}

# Establish connection
engine = create_engine(f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")

# Load scraped data from JSON file
with open('bus_data.json') as f:
    bus_data = json.load(f)

# Define tables for insertion
metadata = MetaData(bind=engine)
metadata.reflect()

buses_table = metadata.tables.get('buses')
buses_images_table = metadata.tables.get('buses_images')

# Insert data into the `buses` table
def insert_bus_data():
    with engine.connect() as connection:
        for bus in bus_data:
            # Prepare core data for `buses`
            core_data = {
                'title': bus.get('title'),
                'year': str(bus.get('year')) if bus.get('year') else None,
                'make': bus.get('make'),
                'engine': bus.get('engine'),
                'source_url': bus_listings_url,
                'price': str(bus.get('price')) if bus.get('price') else None,
                'scraped': 1
            }
            try:
                # Insert and fetch the inserted bus ID
                result = connection.execute(insert(buses_table).values(core_data))
                bus_id = result.inserted_primary_key[0]

                # Insert image data if available
                image_url = bus.get('image_url')
                if image_url:
                    image_data = {
                        'url': image_url,
                        'bus_id': bus_id
                    }
                    connection.execute(insert(buses_images_table).values(image_data))

            except IntegrityError:
                print(f"Duplicate entry detected for bus: {bus.get('title')}")

# Execute insertion
insert_bus_data()

print("Data successfully inserted into the database.")
