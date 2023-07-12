import json
import psycopg2
from awscli.clidriver import create_clidriver

# Connect to the Postgres database
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="postgres"
)
cursor = conn.cursor()

# Read messages from the SQS queue
sqs_command = create_clidriver().create_command('sqs', 'receive-message', '--queue-url', 'http://localhost:4566/000000000000/login-queue')
sqs_response = sqs_command.main()

if 'Messages' in sqs_response:
    for message in sqs_response['Messages']:
        # Parse the received JSON message
        data = json.loads(message['Body'])

        # Mask the PII data (device_id and ip) using a hash function
        masked_device_id = hash(data['device_id'])
        masked_ip = hash(data['ip'])

        # Flatten the JSON object and extract the required fields
        user_id = data['user_id']
        device_type = data['device_type']
        locale = data['locale']
        app_version = data['app_version']
        create_date = data['create_date']

        # Insert the transformed record into the user_logins table
        insert_query = """
        INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date))
        conn.commit()

# Close the database connection
cursor.close()
conn.close()
