import time
import json
import requests
import os.path

api_key = None
api_username = "system"

base_url = "https://discourse.processing.org"

search_base_url = f"{base_url}/search.json"

rate_limit_text = "Too many crawling requests."

category = "processing"
year = 2023

page = 1

while True:
    if os.path.isfile(f"{category}-{year}-{page}.json"):
        page += 1
    else:
        break

print(f"starting from page {page}")

while True:
    search_url = f"https://discourse.processing.org/search.json?q=category:{category}%20before:2024-01-01%20after:2023-01-01?page={page}"

    headers = {"Api-Username": api_username, "Api-Key": api_key} if api_key is not None else {}

    r = requests.get(search_url, headers=headers)
    if r.status_code == 429:
        print(f"Rate limit reached, sleeping for {r.headers['Retry-After']}")
        time.sleep(int(r.headers['Retry-After']))
    else:
        print(f"received page {page}")
        out_file = open(f"{category}-{year}-{page}.json", "w")
        out_file.write(r.text)
        j = json.loads(r.text)
        if j["grouped_search_result"]["more_full_page_results"]:
            page += 1
            print("sleeping for 60 seconds")
            time.sleep(60)
        else:
            print(f"No more pages, stopping")
            break
