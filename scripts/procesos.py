#!/usr/bin/env python
import os
import time
import logging
import requests
import pandas as pd
from datetime import datetime, timedelta

def scrap_radio(stream_url, now, label, factor=150, path="", delay=0):
    if not os.path.isdir(path):
        os.makedirs(path)



    logging.info(f"[{label}] 20 seg audio start downloading ...")

    try:
        r = requests.get(stream_url, stream=True)
        filename = f"/{label}_{now}.mp3"
        inicio = time.time()
        final = inicio + 20
        with open(path + "/" +  filename, "wb") as file:
            for i, block in enumerate(r.iter_content(1024)):
                if time.time() >= final:
                    break
                file.write(block)

    except:
        pass
