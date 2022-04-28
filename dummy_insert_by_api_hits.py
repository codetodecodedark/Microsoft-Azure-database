import pandas as pd
import requests
import threading
import random
import json

df = pd.read_csv("randomkey_uk_data.csv")


def insert_data(payload, index):
    response = requests.post(
        "https://personal-information.azurewebsites.net/personal-info", data=payload
    )
    print("inserted", response.status_code)


threads = []
for index, data in df.iterrows():
    # if index <= 2:
    #     continue
    age = int(random.random() * 100)
    if age < 1:
        age += 1
    payload = {
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "age": age,
        "gender": data["gender"],
        "city": data["city"],
        "country": data["country"],
    }
    threads.append(
        threading.Thread(target=insert_data, args=(json.dumps(payload), index))
    )
    if index == 500:
        break

for thread in threads:
    thread.start()
