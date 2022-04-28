import pandas as pd
import random


df = pd.read_csv("randomkey_uk_data.csv")

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
    if index == 500:
        break
