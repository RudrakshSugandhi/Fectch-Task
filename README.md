**Fetch Reward Home Exercise**

Objective: This project reads JSON data containing user login behavior from an AWS SQS Queue, transforms that data, then writes to a Postgres database.

How to run: 

1. Install docker.
2. Clone this reprository.
3. pip install psycopg2 awscli-local
4. install Psql
5. run command " docker-compose up" - Start the localstack and postgres containers
6. Run this query: "CREATETABLE IF NOTEXISTS user_logins(
   user_id varchar(128),
   device_type varchar(32),
   masked_ip varchar(256),
   masked_device_id varchar(256),
   locale varchar(32),
   app_version integer,
   create_date date
   ); "
7. Open another terminal to check if the table is created
   a. run Command : "psql -h localhost -p 5432 -U postgres -W" - connect to localhost server
   b. command to check the table names " \dt "c.Check if the table user_login visible or not.

  8. Run the code "etl.py" using command " python etl.py"

   Note: please install python using pip install python

9. Verify the results using command "Select * FROM user_logins;" in the psql database.
