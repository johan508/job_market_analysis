# job_market_analysis
This project is created by Han Zhang.  

The dataflow is:     
Adzuna API --> Exract in Python --> Save into SQL Server --> Check & Modify errors in SQL Server --> Extract into Power Query (transform) --> Report in Power BI   

The aim is to investigate the job supplies and categories on the market of selected cities in Canada (Toronto, Montreal, Quebec City, Vancouver, Calgary, Halifax, Sherbrooke) in a certain period based on a third party job platform - Adzuna. It's an ongoing project, the raw data pulled from Adzuna will be updated on every Friday (started from 2024-11-22). It's a "trial and error" project, which means the algorithm will probably be adjusted and updated based on the results accordingly. 

Jobs will be categorized into several groups, for example, Agriculture, Customer Services, Financial Services, IT, Education, etc. (there are 30 categories in Adzuna). The results will show the percentage of each category in a city, say, in the past week, among the 2000 random samples (job posts) from Montreal, 40% of the job falls into customer service; 30% falls into financial services; 20% falls into IT, etc. 

For the moment this project is conducted by myself, so, it could go very slowly, or even wrong. But, at least I'm doing something fun ...  
Report is published here: https://zhanghan.ca/project_4.html  
