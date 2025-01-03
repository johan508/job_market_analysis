# Developed by Han Zhang
# This code will pull raw data from Adzua, parse data from json into dataframe and save data into SQL Server database

import pyodbc
import requests
import math

# set up the Adzuna API id & key
APP_ID = 'YOUR_ID'
APP_KEY = 'YOUR_KEY'
  
# set up some peremeters
RESULTS_PER_PAGE = 50
MAX_DAYS_OLD = 7
DISTANCE = 30
SORT_BY = 'date'

# population figure found on statistique Canada
city_population = {
    'Toronto,ON': 2794356,
    'Montreal,QC': 1762949,
    'Calgary,AB': 1306784,
    'Vancouver,BC': 662248,
    'Quebec City,QC': 549459,
    'Halifax,NS': 439819,
    'Sherbrooke,QC': 172950,
}

# set a cap sample size for Toronto (the biggest city)
toronto_cap = 2000 

# calculate the scaling factor from Toronto
scaling_factor = toronto_cap / city_population['Toronto,ON']
      
# define sample size of each city using a dictionary comprehension (for loop)
samples_per_city = {city: min(int(pop * scaling_factor), toronto_cap) for city, pop in city_population.items()}

# function to extract job data of a city from Adzuna API 
def fetch_jobs(city, sample_size):
    # get total number of pages to extract for each city
    total_pages = math.ceil(sample_size / 50)
    jobs = []

    for page in range (1, total_pages + 1):
        api_url = f'https://api.adzuna.com/v1/api/jobs/ca/search/{page}'
        params = {
            'app_id': APP_ID,
            'app_key': APP_KEY,
            'where': city,
            'results_per_page': RESULTS_PER_PAGE,
            'max_days_old': MAX_DAYS_OLD,
            'distance': DISTANCE,
            'sort_by': SORT_BY
        }
        
        response = requests.get(api_url, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching jobs for {city}: {response.status_code}")
            continue
        
        data = response.json()
        jobs_count = data.get('count')
        results = data.get('results', [])
        jobs.extend(results)
        print(f"{city} data in page {page} pulled.")
        
        if len(results) < 50:
            break
    print(f"{city} has been pulled {len(jobs)} sample jobs.")
    print(f"{city} has {jobs_count} total jobs from 7 days ago to the day of extraction!") 
    
    return jobs, jobs_count

# function to save data fetched from Adzuna to SQL Server database
def save_to_sql(jobs, jobs_count):
    # Define the connection string
    connection_string = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=DELL-XPS\SQLEXPRESS;"  # my server name, e.g., "localhost" or "192.168.1.100"
        "Database=job_data_DB;"
        "Trusted_Connection=yes;"
    )
    
    try:
        conn = pyodbc.connect(connection_string) # connect to SQL server
        cursor = conn.cursor()
        
        for job in jobs:
            cursor.execute('''
                INSERT INTO dbo.job_list (job_id, company_name, job_title, category, province, city, 
                contract_time, contract_type, salary_min, salary_max, publish_date, job_description, 
                total_job_count) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', 
                job.get('id'),
                job.get('company', {}).get('display_name'),
                job.get('title'),
                job.get('category', {}).get('label'),
                job.get('location', {}).get('area', [None, None])[1],
                job.get('location', {}).get('area', [None, None])[2],
                job.get('contract_time'),
                job.get('contract_type'),
                job.get('salary_min'),
                job.get('salary_max'),
                job.get('created'),
                job.get('description'),
                jobs_count)
        
        conn.commit()
        print(f"Successfully saved {len(jobs)} job(s) to the database.")
        
    except pyodbc.Error as e:
        print(f"An error occurred: {e}")
        
    finally:
        cursor.close()
        conn.close() 

for city, sample_size in samples_per_city.items():
    print(f"Fetching jobs for {city}...")
    city_jobs, total_jobs = fetch_jobs(city, sample_size)
    count_job_population = count_job_population + total_jobs
    count_job_sample = count_job_sample + len(city_jobs)
#     all_jobs.extend(city_jobs)
    save_to_sql(city_jobs, total_jobs)
print(f"ALL DONE! {count_job_sample} / {count_job_population} JOBS SAVED!")
