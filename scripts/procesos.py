#!/usr/bin/env python
import os
import time
import logging
import requests
import pandas as pd
import math
from datetime import datetime, timedelta
import pause

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


def scrap_repository(stream_url, label, factor=150, path="", delay=0):
    if not os.path.isdir(path):
        os.makedirs(path)

    # logging.info(f"[{label}] start downloading ...")

    hora_inicio = time.time()
    minutos = 10
    inicio = math.ceil((hora_inicio // 60) / minutos) * 600 - minutos * 60

    date_init = datetime.fromtimestamp(inicio)
    key = date_init.hour * 6 + date_init.minute // 10 + 1

    final = inicio + 60 * minutos

    str_inicio = datetime.fromtimestamp(inicio).strftime('%Y-%m-%d %H:%M:%S')
    str_final = datetime.fromtimestamp(final).strftime('%Y-%m-%d %H:%M:%S')

    logging.info(f"[{label}] 10 min audio Hora inicio - {str_inicio} Hora fin - {str_final}")

    now = datetime.today().strftime("%Y-%m-%d")

    if not os.path.isdir(path + f"/{now}"):
        os.makedirs(path + f"/{now}")

    # Evaluamos si se encuentra en inicio
    pause.until(datetime.fromtimestamp(inicio))
    inicio = final

    try:
        r = requests.get(stream_url, stream=True)
        # print('Factor: ', factor)

        filename = f"/{key}.wav"

        # Si existe previamente, la eliminamos
        if os.path.exists(path + f"/{now}/" + filename):
            os.remove(path + f"/{now}/" + filename)

        with open(path + f"/{now}/" + filename, "wb") as file:
            for i, block in enumerate(r.iter_content(1024)):
                if time.time() >= final:
                    break
                file.write(block)
    except:
        pass


