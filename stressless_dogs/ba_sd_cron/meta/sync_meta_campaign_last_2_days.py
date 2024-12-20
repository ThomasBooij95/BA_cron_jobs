import os
import datetime as dt
from ba_sd_cron.meta.meta_campaigns import fetch_data_and_store_to_postgres


def sync_daily_campaign_stats_last_day():

    ad_account_ids = [os.getenv("META_ACCOUNT_ID_1"), os.getenv("META_ACCOUNT_ID_2")]
    start_date = dt.datetime.today() - dt.timedelta(days=2)
    end_date = start_date + dt.timedelta(days=1)
    print(f"Fetching campaigndata for the last 2 days")
    for id in ad_account_ids:
        fetch_data_and_store_to_postgres(start_date=start_date, end_date=end_date, ad_account_id=id)  # type: ignore


if __name__ == "__main__":
    sync_daily_campaign_stats_last_day()
