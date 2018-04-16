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

    cur.execute(statement)
    result = []
    for row in cur:
        result.append(row)
    return result



def company_jobs(id):
    statement = '''
    SELECT Jobs.Title,JobType, Jobs.Country, PostDate, Lat, Lon
    FROM Companies
    JOIN Jobs
    ON Jobs.CompanyId = Companies.Id
    WHERE  Companies.Id =
    '''
    statement += str(id)
    cur.execute(statement)
    company_job_list = []
    for row in cur:
        company_job_list.append(row)
    return company_job_list

def search_company(keyword = '', country = 'all'):
    statement = '''
    SELECT Companies.Id, Companies.Name
    FROM Companies
    JOIN Jobs
    ON Jobs.CompanyId = Companies.Id
    '''
    if country != 'all':
        statement += "WHERE Companies.Country LIKE " + "'%" + country + "'"
        statement += "AND Companies.Name LIKE" + "'%" + keyword + "%'"
    else:
        statement += "WHERE Companies.Name LIKE" + "'%" + keyword + "%'"

    cur.execute(statement)
    company_job_dic = {}
    comp_tup_list = []
    for row in cur:
        comp_id = row[0]
        comp_name = row[1]
        tup = (comp_id, comp_name)
        comp_tup_list.append(tup)
    for company_tup in comp_tup_list:
        comp_id = company_tup[0]
        job_list = company_jobs(comp_id)
        company_job_dic[company_tup] = job_list

    return company_job_dic

# print(search_job())
