from sql_insertions_main_data.Twitter_Fetch.get_twitter_data import fetch_from_twitter
from sql_insertions_main_data.sql_insertion import del_active_schedules, fetch_from_engine, add_job_schedule, get_active_schedules
from concurrent.futures import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
import time
    
def main_fetch_data(nres, list_kw):
    print (nres)
    for i in list_kw:
        print (i)
    print ('-----------------------------------------')
    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     executor.submit(fetch_from_engine, 'google', list_kw, nres)
    #     executor.submit(fetch_from_engine, 'bing', list_kw, nres)
    #     executor.submit(fetch_from_twitter, list_kw, nres)

def flask_fetch_data(sch, list_kw, lint, nres, kwid):
    jjid = add_job_schedule(list_kw, lint, nres, kwid)
    lint = int(lint)
    jid = jjid[0]
    try:
        sch.start()
        sch.add_job(main_fetch_data,  'interval', seconds = lint, id = str(jid), args = [nres, list_kw])
    except:
        sch.add_job(main_fetch_data,  'interval', seconds = lint, id = str(jid), args = [nres, list_kw])
    while True:
        time.sleep(2)
        
def flask_delete_job(sch, iid):
    iid = str(iid)
    sch.remove_job(iid)