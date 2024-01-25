from sqlalchemy import create_engine, Column, VARCHAR, INT
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError  # Import IntegrityError
from sqlalchemy_utils import create_database, database_exists
from decouple import config
import os

# Determine the base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Retrieve database configuration from environment variables
MYSQL_HOST = config('DB_HOST')
MYSQL_PORT = config('DB_PORT')
MYSQL_USER = config('DB_USER')
MYSQL_PASSWORD = config('DB_PASSWORD')
MYSQL_DB = config('DB_DATABASE')

# Construct the database URL
url = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4'

# Check if the database exists, and create it if it doesn't
if not database_exists(url):
    create_database(url)

# Create a base class for declarative models
Base = declarative_base()

# Create a SQLAlchemy engine
engine = create_engine(url, echo=True)

# Define the CounterTable model
class CounterTable(Base):
    __tablename__ = 'counter'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_0900_ai_ci'
    }
    name = Column(VARCHAR(32), primary_key=True, nullable=False)
    count = Column(INT, default=None)

# Create the 'counter' table in the database
Base.metadata.create_all(engine, tables=[CounterTable.__table__])

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Create a new record in the 'counter' table and handle IntegrityError
new_record = CounterTable(name='test', count=0)

try:
    session.add(new_record)
    session.commit()
except IntegrityError as e:
    # Handle the case where the entry already exists
    session.rollback()
    existing_record = session.query(CounterTable).filter_by(name='test').first()
    if existing_record:
        # Update the count for the existing record
        existing_record.count += 1
        session.commit()
    else:
        print(f"Error: {e}")
