import speech_recognition as sr

from shutil import move
from pydub import AudioSegment

import os

import pandas as pd
import logging

def read_speech_basic(path, ruta_read, ruta_transcript, ruta_fail,  tmp_dir="data/tmp"):
    print("------------------------------------------")
    if len(os.listdir(path))>0:

        _file = path + "/" + os.listdir(path)[0]
        filename = _file.split("/")[-1].split(".")[0]
        filedir = f"{tmp_dir}/stream_{filename}.wav"

        if not os.path.isdir(tmp_dir):
            os.makedirs(tmp_dir)

        move(f"{_file}", f"{ruta_read}/{filename}.mp3")

        try:

            print("Lectura de archivos")
            print(f"{ruta_read}/{filename}.mp3")
            audio = AudioSegment.from_file(f"{ruta_read}/{filename}.mp3")

            print("Exportar a wav")
            audio.export(filedir, format="wav")

            r = sr.Recognizer()
            print("Transcripcion")
            with sr.AudioFile(filedir) as source:

                audio = r.listen(source, timeout=30)
                text = r.recognize_google(audio, language="es-PE")
                logging.debug("Finish")


            data_text_new = pd.DataFrame([{"file": _file, "text": text}])
            data_text_new.to_csv(f"{ruta_transcript}/{filename}.csv")

            os.remove(filedir)
        except:
            move(f"{ruta_read}/{filename}.mp3", f"{ruta_fail}/{filename}.mp3")