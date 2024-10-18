import time
import json
import requests
import os.path

api_key = None
api_username = 'system'

base_url = "https://discourse.processing.org"
search_base_url = f"{base_url}/search.json"

category = "processing"
year = 2023

page = 1

s = requests.Session()
s.headers.update({ 'User-Agent': 'curl/8.1.2'})
if api_key is not None:
    s.headers.update({ 'Api-Key' : api_key , 'Api-Username' : api_username })

while True:
    if os.path.isfile(f"{category}-{year}-{page}.json"):
        page += 1
    else:
        break

print(f"starting from page {page}")

while True:
    search_url = f"{search_base_url}?q=category:{category}%20before:2024-01-01%20after:2023-01-01&page={page}"

    print(f"searching {search_url}")
    r = s.get(search_url)
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
            print("sleeping for 5 seconds")
            time.sleep(5)
        else:
            print(f"No more pages, stopping")
            break