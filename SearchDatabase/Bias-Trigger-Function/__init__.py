import datetime
import logging
from concurrent.futures import ThreadPoolExecutor
import azure.functions as func
from main_insertion import fetch_from_engine
from main_insertion import fetch_from_twitter

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Insertion function ran at %s', utc_timestamp)
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(fetch_from_engine, 'google')
        executor.submit(fetch_from_engine, 'bing')
        executor.submit(fetch_from_twitter)