from datetime import datetime, timedelta
from numpy import where
from pandas import DataFrame, IntervalIndex, cut
from azure.storage.blob import BlobServiceClient
import os
from typing import Optional


def format_date(dates, from_format:str, to_format:str):

    return [datetime.strptime(date, from_format).strftime(to_format) for date in dates]


# get date str for plotting
def date_str_to_date_int(dates, start_date:str, date_format:str):

    start_date_date_time = datetime.strptime(start_date, date_format)
    dates_date_time = [datetime.strptime(date, date_format) for date in dates]

    return [(date - start_date_date_time).days for date in dates_date_time]


def date_int_to_date_str(dates_ints, start_date:str, date_format:str):

    start_date_date_time = datetime.strptime(start_date, date_format)

    return [(start_date_date_time + timedelta(days=date_int)).strftime(date_format) for date_int in dates_ints]


date_format_global = "%Y-%m-%d"
def get_mutual_dates(dates_list: list, date_format: str = date_format_global, order: str = "chronological") -> list:

    """
    Uses the set opperation intersection (set.intersection) to provide the mutual set of dates for the passed list of date lists
    """

    dates = set(dates_list[0])
    for i, dates_l in enumerate(dates_list):
        if i > 0:
            dates = dates.intersection(dates_l)

    dates = list(dates)

    if order is None:
        pass
    elif order == "chronological":
        dates = sorted([datetime.strptime(date, date_format) for date in dates])
        dates = [date.strftime(date_format) for date in dates]
    else:
        print(f"Returning unordered as {order} os not an option!")

    return dates


def bin_column(df: DataFrame, intervals: list[tuple], column: str, new_column: str, closed='left',
               fillna: bool = False) -> DataFrame:
    # set intervals for binning ages
    bins = IntervalIndex.from_tuples(intervals, closed=closed)
    binned = cut(df[column], bins=bins)
    df1 = df.copy()
    df1[new_column] = binned  # should swap with concat
    # convert column to strings
    df1[new_column] = df1[new_column].astype(str)

    if fillna:
        df1.ages_binned.fillna('Unknown', inplace=True)

    return df1


def save_to_blob(df: DataFrame, path: str, blob_container_name: str, storage_account_name: str,
                 keep_index: bool = False, secret_key: Optional[str] = None) -> None:

    blob_storage_url = f"https://{storage_account_name}.blob.core.windows.net"
    if secret_key is None:
        secret_key = os.getenv("BLOBSTORAGEKEY")
    blob_service_client = BlobServiceClient(blob_storage_url, secret_key)
    blob_client = blob_service_client.get_blob_client(container=blob_container_name, blob=path)
    blob_client.upload_blob(df.to_csv(index=keep_index), blob_type="BlockBlob", overwrite=True)
