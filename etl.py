import json
import subprocess
import psycopg2
import packaging.version

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
sqs_command = ["awslocal", "sqs", "receive-message", "--queue-url", "http://localhost:4566/000000000000/login-queue"]
sqs_response = subprocess.run(sqs_command, capture_output=True, text=True)
sqs_output = json.loads(sqs_response.stdout)

if 'Messages' in sqs_output:
    for message in sqs_output['Messages']:
        # Parse the received JSON message
        data = json.loads(message['Body']) 
        # Check if all required fields exist in the data
        if 'user_id' in data and 'device_type' in data and 'ip' in data and 'device_id' in data and 'locale' in data and 'app_version' in data:
            # Mask the PII data (device_id and ip) using a hash function
            masked_device_id = hash(data['device_id'])
            masked_ip = hash(data['ip'])

            # Extract the fields from the data
            user_id = data['user_id']
            device_type = data['device_type']
            locale = data['locale']

            # Parse app_version as a numeric value converting into string and then to integer to parse
            app_version = packaging.version.parse(data['app_version'])
            app_version_str = "{}{}".format(app_version.release[0], app_version.release[1])
            app_version_int = int(app_version_str)

            # Set create_date to None if it is missing
            create_date = data.get('create_date')

            # Insert the transformed record into the user_logins table
            insert_query = """
            INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (user_id, device_type, masked_ip, masked_device_id, locale, app_version_int, create_date))
            conn.commit()
        else:
            print("Required fields are missing in the data")

# Close the database connection
cursor.close
