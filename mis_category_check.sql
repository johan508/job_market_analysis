
-- check database mega data (such as size)
EXEC sp_helpdb;

use job_data_DB;


-- Adzuna sometimes puts the job record into the wrong province / city, e.x. a job supposed to be in Vancouver, but categorized into Toronto
-- this code will check geographical mis-category on the date of pulling (from the 00:00:00 to the next 00:00:00)
-- each city should exist once with one total (if there are 2 or more, one must be mis-categorized)
-- find them out and UPDATE the Province / City manually

select distinct r.city_name, l.total_job_count
from dbo.job_list as l
join dbo.region_city as r
on l.city = r.city_region_pk
WHERE publish_date >= '2025-01-09 00:00:00' 
  AND publish_date < '2025-01-10 00:00:00';



