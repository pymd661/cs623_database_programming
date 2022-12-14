# this code succesfully updates the name from p1 to pp1

# import Libraries
import psycopg2
import os

psql_pw = os.environ.get('PSQL_AUTH')


def drop_constraint(table_name, constraint_name):
    """Drops constraint of a table by passing table name and constraint name"""
    cur.execute(f'''ALTER TABLE {table_name} DROP CONSTRAINT {constraint_name}; ''')


# Log in info
con = psycopg2.connect(
    host="localhost",
    database="cs623_project",
    user="postgres",
    password=psql_pw
)

# The database needs to implement ACID properties
# For isolation: SERIALIZABLE
con.set_isolation_level(3)
# For atomicity
con.autocommit = False

try:
    cur = con.cursor()
    # call function to drop the foreign key
    drop_constraint("Stock", "fk_stock_product")

    # create a new constraint specifying the constraint to have ON UPDATE CASCADE ON DELETE CASCADE action
    cur.execute('''ALTER TABLE Stock ADD CONSTRAINT fk_stock_product FOREIGN KEY(prodId) REFERENCES Product(prodId)
    ON DELETE CASCADE ON UPDATE CASCADE;''')

    # Rename p1 to pp1 in the product table
    cur.execute('''UPDATE Product SET prodId='pp1' WHERE  prodId='p1';''')

    print('Tables have been successfully updated')
except (Exception, psycopg2.DatabaseError) as err:
    print(err)
    print("Transactions could not be completed so database will be rolled back before start of transactions")
    con.rollback()
finally:
    if con:
        con.commit()
        con.close()
        print("PostgresSQL connection is now closed.")
