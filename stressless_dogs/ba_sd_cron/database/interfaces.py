from psycopg2.extras import execute_values
import datetime as dt
import psycopg2
import json
import os


def store_data_in_postgres(data_list):
    """
    Store a list of dictionaries in the raw.raw_meta_campaigns table in PostgreSQL.

    Args:
        data_list (list): A list of dictionaries top be stored as JSON.
    """
    # Database connection details
    db_config = {
        "dbname": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "host": os.getenv("POSTGRES_HOST"),
        "port": 5432,  # Default PostgreSQL port
    }
    # SQL query to insert data

    sync_date = dt.datetime.now(dt.timezone.utc)

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_config)
    try:
        with conn:
            with conn.cursor() as cur:
                # Create a list of tuples (sync_date, json_item) for bulk insertion
                records = [(sync_date, json.dumps(item)) for item in data_list]

                # Use the `execute_values` method for bulk insert
                execute_values(  # type: ignore
                    cur,
                    """
                    INSERT INTO raw.raw_meta_campaigns (sync_date, data)
                    VALUES %s
                    """,
                    records,
                )
                print(f"{len(records)} rows inserted successfully.")
    except Exception as e:
        raise Exception(f"An error occurred:{e}")
    finally:
        conn.close()
