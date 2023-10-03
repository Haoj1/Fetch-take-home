import json
import psycopg2
import subprocess
from datetime import datetime


# AWS SQS configuration using awslocal
sqs_queue_url = "http://localhost:4566/000000000000/login-queue"

# PostgreSQL configuration
db_host = "localhost"
db_port = 5432
db_name = "postgres"
db_user = "postgres"
db_password = "postgres"


def mask_pii(data):
    # Implement your PII masking logic here, e.g., hash device_id and IP
    app_version = data.get("app_version", "")
    if app_version.isdigit():
        app_version = int(app_version)
    else:
        app_version = 0

    create_date_str = data.get("create_date", "")
    try:
        create_date = datetime.strptime(create_date_str, "%Y-%m-%d")
    except ValueError:
        create_date = None

    masked_data = {
        "user_id": data.get("user_id", ""),
        "device_type": data.get("device_type", ""),
        "masked_ip": hash(data.get("ip", "")),
        "masked_device_id": hash(data.get("device_id", "")),
        "locale": data.get("locale", ""),
        "app_version": app_version,
        "create_date": create_date
    }
    return masked_data


def receive_message_from_sqs(queue_url):
    # Use awslocal to receive messages from SQS
    awslocal_command = [
        "awslocal", "sqs", "receive-message",
        "--queue-url", queue_url,
        "--attribute-names", "All"
    ]
    awslocal_output = subprocess.check_output(awslocal_command)
    messages = json.loads(awslocal_output).get("Messages", [])
    return messages


def delete_message_from_sqs(queue_url, receipt_handle):
    # Use awslocal to delete a message from SQS
    awslocal_command = [
        "awslocal", "sqs", "delete-message",
        "--queue-url", queue_url,
        "--receipt-handle", receipt_handle
    ]
    subprocess.run(awslocal_command)


def create_user_logins_table(cursor):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS user_logins (
        user_id varchar(128),
        device_type varchar(32),
        masked_ip varchar(256),
        masked_device_id varchar(256),
        locale varchar(32),
        app_version integer,
        create_date date
    );
    """
    cursor.execute(create_table_sql)


def process_sqs_messages():
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()

    create_user_logins_table(cursor)

    while True:
        # Receive messages from SQS using awslocal
        messages = receive_message_from_sqs(sqs_queue_url)

        for message in messages:
            # Parse JSON message
            data = json.loads(message["Body"])
            # Mask PII data
            masked_data = mask_pii(data)

            # Insert data into PostgreSQL
            insert_query = "INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (
                masked_data["user_id"],
                masked_data["device_type"],
                masked_data["masked_ip"],
                masked_data["masked_device_id"],
                masked_data["locale"],
                masked_data["app_version"],
                masked_data["create_date"]
            ))
            print("User query inserted")
            # Delete the processed message from SQS using awslocal
            delete_message_from_sqs(sqs_queue_url, message["ReceiptHandle"])

        # Commit the transaction
        conn.commit()

    # Close the PostgreSQL connection
    conn.close()


if __name__ == "__main__":
    process_sqs_messages()
