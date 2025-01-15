import pymysql
from sqlalchemy import (create_engine, MetaData, Table, Column, Integer, String, 
                        Text, Float, Enum, ForeignKey, Boolean, TIMESTAMP)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Buses(Base):
    __tablename__ = 'buses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256), nullable=True)
    year = Column(String(10), nullable=True)
    make = Column(String(25), nullable=True)
    model = Column(String(50), nullable=True)
    body = Column(String(25), nullable=True)
    chassis = Column(String(25), nullable=True)
    engine = Column(String(60), nullable=True)
    transmission = Column(String(60), nullable=True)
    mileage = Column(String(100), nullable=True)
    passengers = Column(String(60), nullable=True)
    wheelchair = Column(String(60), nullable=True)
    color = Column(String(60), nullable=True)
    interior_color = Column(String(60), nullable=True)
    exterior_color = Column(String(60), nullable=True)
    published = Column(Boolean, default=False)
    featured = Column(Boolean, default=False)
    sold = Column(Boolean, default=False)
    scraped = Column(Boolean, default=False)
    draft = Column(Boolean, default=False)
    source = Column(String(300), nullable=True)
    source_url = Column(String(1000), nullable=True)
    price = Column(String(30), nullable=True)
    cprice = Column(String(30), nullable=True)
    vin = Column(String(60), nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    gvwr = Column(String(50), nullable=True)
    dimensions = Column(String(300), nullable=True)
    luggage = Column(Boolean, default=False)
    state_bus_standard = Column(String(25), nullable=True)
    airconditioning = Column(Enum('REAR', 'DASH', 'BOTH', 'OTHER', 'NONE'), nullable=True)
    location = Column(String(30), nullable=True)
    brake = Column(String(30), nullable=True)
    contact_email = Column(String(100), nullable=True)
    contact_phone = Column(String(100), nullable=True)
    us_region = Column(Enum('NORTHEAST', 'MIDWEST', 'WEST', 'SOUTHWEST', 'SOUTHEAST', 'OTHER'), default='OTHER')
    description = Column(Text, nullable=True)
    score = Column(Boolean, default=False)
    category_id = Column(Integer, default=0)

class BusesOverview(Base):
    __tablename__ = 'buses_overview'

    id = Column(Integer, primary_key=True, autoincrement=True)
    bus_id = Column(Integer, ForeignKey('buses.id'), nullable=True)
    mdesc = Column(Text, nullable=True)
    intdesc = Column(Text, nullable=True)
    extdesc = Column(Text, nullable=True)
    features = Column(Text, nullable=True)
    specs = Column(Text, nullable=True)

class BusesImages(Base):
    __tablename__ = 'buses_images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=True)
    url = Column(String(1000), nullable=True)
    description = Column(Text, nullable=True)
    image_index = Column(Integer, default=0)
    bus_id = Column(Integer, ForeignKey('buses.id'), nullable=True)

class BusesAdditionalInfo(Base):
    __tablename__ = 'buses_additional_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    bus_id = Column(Integer, ForeignKey('buses.id'), nullable=True)
    warranty = Column(String(100), nullable=True)
    service_history = Column(Text, nullable=True)
    previous_owners = Column(Integer, nullable=True)

class BusDealers(Base):
    __tablename__ = 'bus_dealers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dealer_name = Column(String(256), nullable=False)
    contact_number = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    location = Column(String(256), nullable=True)

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'your_user',
    'password': 'your_password',
    'database': 'your_database_name'
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
