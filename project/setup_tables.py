# this sets up up my relations and inserts data

# import Libraries
import psycopg2
import os
psql_pw = os.environ.get('PSQL_AUTH')

# Log in info, creates a database session
con = psycopg2.connect(
    host="localhost",
    database="cs623_project",
    user="postgres",
    password=psql_pw
)


# we created functions to have more efficient code
def delete_relations():
    """Deletes tables if they already exists"""
    cur.execute('''DROP TABLE IF EXISTS Stock;''')
    cur.execute('''DROP TABLE IF EXISTS Product;''')
    cur.execute('''DROP TABLE IF EXISTS Depot;''')


def create_relations():
    """ Create our tables for the project. It creates three tables: product, depot, stock."""
    # Product Table
    cur.execute('''CREATE TABLE Product(prodId VARCHAR(10), pname VARCHAR(20), price DECIMAL);''')
    # Depot Table
    cur.execute('''CREATE TABLE Depot(depId VARCHAR(10), addr VARCHAR(30), volume INTEGER);''')
    # Stock Table
    cur.execute('''CREATE TABLE Stock(prodId VARCHAR(10), depId VARCHAR(10), quantity INTEGER);''')


def create_constraints():
    """Create our primary key and foreign key constraints"""
    cur.execute('''ALTER TABLE Product ADD CONSTRAINT pk_product PRIMARY KEY(prodId);''')
    cur.execute('''ALTER TABLE Depot ADD CONSTRAINT pk_depot PRIMARY KEY(depId);''')
    cur.execute('''ALTER TABLE Stock ADD CONSTRAINT pk_stock PRIMARY KEY(prodId, depId);''')
    cur.execute('''ALTER TABLE Stock ADD CONSTRAINT fk_stock_product FOREIGN KEY(prodId) REFERENCES Product(prodId);''')
    cur.execute('''ALTER TABLE Stock ADD CONSTRAINT fk_stock_depot FOREIGN KEY(depId) REFERENCES Depot(depId);''')


def insert_data():
    """Populate our tables with data"""
    cur.execute('''INSERT INTO Product VALUES
        ('p1', 'tape', 2.5),
        ('p2', 'tv', 250),
        ('p3', 'vcr', 80);''')

    cur.execute('''INSERT INTO Depot VALUES
        ('d1', 'New York', 9000),
        ('d2', 'Syracuse', 6000),
        ('d4', 'New York', 2000);''')

    cur.execute('''INSERT INTO Stock VALUES
        ('p1', 'd1', 1000),
        ('p1', 'd2', -100),
        ('p1', 'd4', 1200),
        ('p3', 'd1', 3000),
        ('p3', 'd4', 2000),
        ('p2', 'd4', 1500),
        ('p2', 'd1', -400),
        ('p2', 'd2', 2000);''')


# The database needs to implement ACID properties
# For isolation: SERIALIZABLE
# controls how transactions are isolated from each other, makes sure that transactions do not interfere with
# other transactions
con.set_isolation_level(3)

# For atomicity
# This makes sure that NOT every SQL statement is a transaction. This means not every transaction will be saved unless
# we explicitly have a commit statement. This helps us rollback the database when one of the transactions fails.
con.autocommit = False

try:
    cur = con.cursor()
    delete_relations()
    create_relations()
    create_constraints()
    insert_data()
    print('Tables have been successfully created and populated.')
except (Exception, psycopg2.DatabaseError) as err:
    print(err)
    print("Transactions could not be completed so database will be rolled back before start of transactions")
    con.rollback() # rollback to original state, prior to try statement
finally:
    if con:
        con.commit()
        con.close()
        print("PostgresSQL connection is now closed.")
