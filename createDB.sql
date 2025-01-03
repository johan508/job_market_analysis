CREATE DATABASE job_data_DB;

use job_data_DB;

CREATE TABLE dbo.job_list (
	id_sk int identity (1,1),   -- this is a surrogate key starting from 1
	job_id nvarchar(255),            -- this is a real job id from the web
	company_name nvarchar(255),
	job_title nvarchar(255),
	category nvarchar(255),
	province nvarchar(255),
	city nvarchar(255),
	contract_time nvarchar(255),
	contract_type nvarchar(255),
	salary_min float,
	salary_max float,
	publish_date datetime,
	job_description nvarchar(max),
	job_count int
)
