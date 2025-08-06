import os
import pandas as pd
import pickle

from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.conversion.log import converter as log_converter

def load_event_log(xes_path='data/BPI_Challenge_2017.xes.gz', cache_path=None, force_reload=False):
    if cache_path is None:
        # Automatically generate a cache path in same folder as .xes.gz
        cache_path = xes_path.replace('.xes.gz', '.pkl').replace('.xes', '.pkl')

    if not force_reload and os.path.exists(cache_path):
        print(f"[INFO] Loading event log from cache: {cache_path}")
        with open(cache_path, 'rb') as f:
            return pickle.load(f)

    # Else parse and save cache
    print(f"[INFO] Parsing event log from XES: {xes_path}")
    log = xes_importer.apply(xes_path)
    event_log = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
    

# 🔁 Standardize column names for convenience
    event_log.rename(columns={
        "case:concept:name": "case_id",
        "concept:name": "activity",
        "time:timestamp": "timestamp"
    }, inplace=True)
    event_log['timestamp'] = pd.to_datetime(event_log['timestamp'])

    print(f"[INFO] Saving parsed log to cache: {cache_path}")
    with open(cache_path, 'wb') as f:
        pickle.dump(event_log, f)

    return event_log
