from ba_sd_cron.meta.meta_campaigns import fetch_data_and_store_to_postgres
from dateutil.relativedelta import relativedelta
import datetime as dt
import os


def sync_daily_campaign_stats_with_interval(
    start_interval=dt.date(2024, 12, 1), end_interval=dt.date(2025, 1, 1)
):
    ad_account_ids = [os.getenv("META_ACCOUNT_ID_1"), os.getenv("META_ACCOUNT_ID_2")]
    start_date = start_interval
    while start_date < end_interval:
        end_date = start_date + relativedelta(month=1)
        print(f"Fetching campaigndata for month {str(start_date)}")
        for id in ad_account_ids:
            fetch_data_and_store_to_postgres(
                start_date=start_date, end_date=end_date, ad_account_id=id  # type: ignore
            )
        start_date = start_date + relativedelta(months=1)


if __name__ == "__main__":
    sync_daily_campaign_stats_with_interval()
