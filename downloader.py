import os
import requests
import json
from urllib.parse import quote
from dotenv import load_dotenv
from collections import defaultdict
from tree_builder import build_tree

SAVE_FILE = "progress.json"

headers = {
    "User-Agent": "Mozilla/5.0", 
    "Accept": "application/json",  
    }

all_results = []

def load_progress():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "data": [],
        "offset": 0
    }

def save_progress(data, offset):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump({"data": data, "offset": offset}, f, ensure_ascii=False, indent=2)

def fetch_data(API_KEY, offset, page_size):
    state = load_progress()
    all_results = state["data"]
    offset = state["offset"]

    try:
        while True: 
            source_dict = {
                # "query": {
                #     "term": {
                #         "AreaType": 0
                #     }
                # },
                "from" : offset,
                "size" : page_size
            }


            source_json = json.dumps(source_dict)


            url = f'https://data.egov.kz/api/v4/kato/data?apiKey={API_KEY}&source={source_json}'


            response = requests.get(url, headers=headers)


            if response.status_code != 200:
                    print(f"Ошибка {response.status_code}: {response.text}")
                    save_progress(all_results, offset)
                    break

            data = response.json()

            if not data:
                print("Больше данных нет.")
                break

            all_results.extend(data)
            print(f"Загружено {len(data)} записей (всего: {len(all_results)})")

            offset += page_size
            save_progress(all_results, offset)
    except Exception as e:
        print("Произошла ошибка:", e)
        save_progress(all_results, offset)
        print("Прогресс сохранён. Запусти снова для продолжения.")

    return all_results