from ba_sd_cron.database.interfaces import store_data_in_postgres
from dotenv import load_dotenv
import datetime as dt
import requests
import os

load_dotenv()


def fetch_data_and_store_to_postgres(
    start_date=dt.date(2022, 1, 1),
    end_date=dt.datetime.today().date() + dt.timedelta(days=1),
    ad_account_id="",  # Stressless dogs 2
):

    all_data = fetch_meta_daily_campaign_data(
        start_date,
        end_date,
        ad_account_id,
    )
    try:
        store_data_in_postgres(all_data)
        print("Data stored succesfully")
    except Exception as e:
        print(f"Error with storing the data:{e}")


def fetch_meta_daily_campaign_data(
    start_date,
    enddate,
    ad_account_id,
):
    url = f"https://graph.facebook.com/v20.0/{ad_account_id}/insights"
    params = {
        "access_token": os.getenv("META_ACCESS_TOKEN"),
        "fields": "campaign_id,campaign_name,account_id,spend,actions,impressions,clicks",  # adlabels
        "time_range": '{"since":"'
        + str(start_date.date())
        + '", "until":"'
        + str(enddate.date())
        + '"}',  # JSON string for time_range
        "time_increment": 1,  # Daily breakdown
        "level": "campaign",  # One row per campaign per day
        "limit": 25,  # Number of results per page
    }

    all_data = []  # To store all the results
    current_page = 1
    while url:
        # Make the API request
        print(f"fetching page {current_page}")
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()

        # Append the current page of data to all_data
        if "data" in data:
            all_data.extend(data["data"])
        else:
            print("No data found in response.")
            break

        # Check for the next page
        paging = data.get("paging", {})
        url = paging.get("next", None)  # Update URL to the next page if it exists

        # Clear parameters after the first request (next URL already includes them)
        params = None
        current_page += 1

    print(f"fetched {len(all_data)} objects")
    return all_data
