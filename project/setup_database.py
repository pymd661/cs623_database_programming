# this creates the database

# Import libraries
import psycopg2
import os
psql_pw = os.environ.get('PSQL_AUTH')


# Establish connection
con = psycopg2.connect(
    host="localhost",
    user="postgres",
    password=psql_pw
)


# For isolation: SERIALIZABLE
con.set_isolation_level(3)
# For atomicity
con.autocommit = True

# Create cursor object
cur = con.cursor()


def create_database(db_name):
    """Create a database by passing a db_name to name the database"""
    postgres_create_db = f"CREATE DATABASE {db_name};"
    cur.execute(postgres_create_db)
    print(f'Database {db_name} has been successfully created.')


try:
    cur = con.cursor()
    # Create database called 'cs623_project'
    create_database('cs623_project')

except (Exception, psycopg2.DatabaseError) as err:
    print(err)
    print("There was an error and database was not created.")

finally:
    if con:
        con.commit()
        cur.close()
        con.close()
        print("PostgresSQL connection is now closed.")
