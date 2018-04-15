# read data from database
import sqlite3
DBNAME = 'ux-job.db'

conn = sqlite3.connect(DBNAME, check_same_thread=False)
cur = conn.cursor()

def search_company_lon_lat(company_name):

    statement = """
    SELECT Lat, Lon
    FROM Companies
    WHERE Name = """
    statement += "'" + company_name + "'"

    cur.execute(statement)
    row = cur.fetchone()
    return (row)
