import sqlite3
import requests
import json
from bs4 import BeautifulSoup
import secret

DBNAME = 'ux-job.db'
conn = sqlite3.connect(DBNAME)
cur = conn.cursor()

# ----------------------Set up caching-------------------------------
CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

def get_unique_key(url):
    return url

# ----------------------Cache------------------------------------

def get_data_using_cache(url):
    unique_ident =  get_unique_key(url)
    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        # Make the request and cache the new datad
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

# ----------------------Get job data------------------------------------
#
def get_job_and_company_data():
    url = 'https://www.uxjobsboard.com/'
    page_data = get_data_using_cache(url)
    page_soup = BeautifulSoup(page_data, 'html.parser')
    items = page_soup.find_all(class_='job-item')
    job_data_list = []
    company_data_list = []
    for num in range(50):
    # for item in items:
        link = items[num].find(class_='title-link')['href']
        detail_page_data = get_data_using_cache(link)
        detail_soup = BeautifulSoup(detail_page_data, 'html.parser')
        company_name = detail_soup.find(id='job_author_name').text.strip()
        title = detail_soup.find(id='job_title').text.strip().split('\t')[0]
        location = detail_soup.find(id='job_location').text.strip().split(',')
        # print(len(location))
        if len(location) > 1:
            city = location[0]
            country = location[-1]
        else:
            city = 'Anywhere'
            country ='Anywhere'
        job_type = detail_soup.find(id='job_type').text.strip()
        date = detail_soup.find("div", {"class": "date"}).text.strip()
        company_site = detail_soup.find(id = 'job_author_url')['href']
        lat = detail_soup.find('input', {'name': 'jobLocLat'}).get('value')
        lng = detail_soup.find('input', {'name': 'jobLocLng'}).get('value')
        tup_job_unit = (title, job_type, company_name, city,country,date)
        tup_company_unit = (company_name, city, country, lat, lng, company_site)
        job_data_list.append(tup_job_unit)
        company_data_list.append(tup_company_unit)
    return job_data_list,company_data_list

def create_database():
    statement = """
        CREATE TABLE 'Jobs' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Title' Text NOT NULL,
        'JobType' Text NOT NULL,
        'CompanyName' Text NOT NULL,
        'CompanyId' Integer,
        'City' Text NOT NULL,
        'Country' Text NOT NULL,
        'PostDate' Text
    );
        """
    cur.execute(statement)
    conn.commit()
    statement = """
        CREATE TABLE 'Companies' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Name' Text NOT NULL,
        'City' Text NOT NULL,
        'Country' Text NOT NULL,
        'Lat' Text NOT NULL,
        'Lon' Text NOT NULL,
        'CompanySite' Text NOT NULL
    );
        """
    cur.execute(statement)
    conn.commit()

def populate_database(two_list):
    job_data_list = two_list[0]
    company_data_list = two_list[1]
    for result in job_data_list:
        statement = """
        INSERT INTO Jobs (Id, Title, JobType, CompanyName, City, Country, PostDate)
        VALUES (NULL,?,?,?,?,?,?)
        """
        cur.execute(statement, result)
        conn.commit()
    print('ok')
    for result in company_data_list:
        statement = """
        INSERT INTO Companies (Id, Name, City, Country, Lat, Lon, CompanySite)
        VALUES (NULL,?,?,?,?,?,?)
        """
        cur.execute(statement, result)
        conn.commit()

    statement = '''
    UPDATE Jobs
    SET CompanyId = (SELECT Id
    FROM Companies
    WHERE Jobs.CompanyName= Companies.Name)
    '''
    cur.execute(statement)
    conn.commit()
    print('ok')




if __name__ == "__main__":
    two_list = get_job_and_company_data()
    # create_database()
    populate_database(two_list)
