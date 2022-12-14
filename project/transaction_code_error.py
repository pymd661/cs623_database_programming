# import Libraries
import psycopg2
import os

psql_pw = os.environ.get('PSQL_AUTH')


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
