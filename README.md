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
8. run Command : "psql -h localhost -p 5432 -U postgres -W" - connect to localhost server
9. command to check the table names " \dt ,check if the table user_login visible or not.
10. Run the code "etl.py" using command " python etl.py", Note: please install python using pip install python
11. Verify the results using command "Select * FROM user_logins;" in the psql database.

**Questions and Answers:**


For this assignment an ounce of communication and organization is worth a pound of execution.
Please answer the following questions:
● How would you deploy this application in production?

=> I would deploy this application in production by using a container orchestration platform, such as Kubernetes. This would allow me to scale the application up or down as needed, and to make it more resilient to failures. I would also use a continuous integration and continuous delivery (CI/CD) pipeline to automate the deployment process.


● What other components would you want to add to make this production ready?

=> Apart from CI/CD pipline these components can be added for 

* A load balancer to distribute traffic across multiple instances of the application.
* A monitoring system to track the health of the application and to alert me if there are any problems.
* A logging system to store all of the application's logs.
* A disaster recovery plan to ensure that the application can be restored in the event of a failure.


● How can this application scale with a growing dataset.

=> using a distributed database, such as Amazon Aurora or EC2 instances. This would allow me to distribute the data across multiple servers, which would improve performance and scalability.

● How can PII be recovered later on?

=> PII can be recovered later on by storing the original values of the `device_id` and `ip` fields in a separate table. This table would be encrypted, and access to it would be restricted to authorized users.

● What are the assumptions you made?

=> 

* The JSON data in the SQS queue is valid.
* The Postgres database is configured correctly.
* The `packaging.version` module is installed.
