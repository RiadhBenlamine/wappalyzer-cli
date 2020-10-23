''' Wappalyzer client
    version: 1.0
'''

import sys

import requests
from termcolor import colored

if len(sys.argv) < 2:
    print("Usage:")
    print("$ python wappalyzer.py (http|https)://example.com")
    print("\nAuthor: Riadh Benlamine")
    sys.exit()
else:
    pass

target = sys.argv[1]
API_KEY = '' # Your API key for wappalyzer
headers = { 'x-api-key': f'{API_KEY}', }
try:
    request = requests.get(f"https://api.wappalyzer.com/lookup/v2/?urls={target}", headers=headers)

    if request.status_code == 400:
        print("There was an error with the request.")
        sys.exit()
    elif request.status_code == 403:
        MESSAGE ="Authorisation failure (incorrect API key, "
        MESSAGE += "invalid method or resource or insufficient credits)."
        print(MESSAGE)
        sys.exit()

    elif request.status_code == 429:
        print("Rate limit exceeded.")
        sys.exit()

    print(f"Spent {request.headers['wappalyzer-credits-spent']} from your credits !")
    print(f"Your Credits: {request.headers['wappalyzer-credits-remaining']}")
    json_data = request.json()[0]
    print('Url:', json_data['url'])
    print("Technologies:")
    techs = json_data['technologies']
    for tech in techs:
        print('='*30)
        print(f"Category: {tech['categories'][0]['name']}")
        print('='*30)
        version = tech['versions'][0] if len(tech['versions']) != 0 else "Unknown"
        print(colored(f"{tech['name']}: {version}", 'red', 'on_white'))
        print()
except requests.ConnectionError:
    print("Check your connection")
