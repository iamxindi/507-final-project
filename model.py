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

def search_job(keyword = '', country = 'all', time = "range",jobtype = 'contract', start_time = "2018-03-01", end_time = "2018-04-30"):
    statement = '''
    SELECT Title, JobType, Country, PostDate, Id
    FROM Jobs

    '''
    if country == 'all':
        statement += ''
        statement += "WHERE Title LIKE " + "'%" + keyword + "%'"
    else:
        statement += "WHERE Country LIKE "+ "'%" + country + "'"
        statement += " AND Title LIKE " + "'%" + keyword + "%'"

    if time != 'most_recent':
        statement += " AND Postdate BETWEEN '{}' AND '{}' ".format(start_time, end_time)

    if jobtype == 'full_time':
        statement += "AND JobType = 'Full-time' "
    elif jobtype == 'freelance':
        statement += "AND JobType = 'Freelance' "
    elif jobtype == 'contract':
        statement += "AND JobType = 'Contract' "
    elif jobtype == 'internship':
        statement += "AND JobType = 'Internship' "
    else:
        statement += ''

    statement += "ORDER BY PostDate DESC"
    if time == "most_recent":
        statement += " LIMIT 5"

    # print(statement)

    cur.execute(statement)
    result = []
    for row in cur:
        result.append(row)
    return result

def search_company():
    statement = '''
    SELECT Companies.Id
    FROM Companies
    JOIN Jobs
    ON Jobs.CompanyId = Companies.Id
    WHERE Companies.Country LIKE "%India"
    '''

    cur.execute(statement)
    company_id_list = []
    for row in cur:
        company_id_list.append(row[0])
    for id in company_id_list:
        statement = '''
        SELECT Jobs.Title, PostDate
        FROM Companies
        JOIN Jobs
        ON Jobs.CompanyId = Companies.Id
        WHERE  Companies.Id =
        '''
        statement += str(id)
        cur.execute(statement)
        for row in cur:
            print (row)

search_company()
