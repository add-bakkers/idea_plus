import requests

S = requests.Session()

URL = "https://ja.wikipedia.org/w/api.php"

while(1):
    SEARCHPAGE = input()

    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": SEARCHPAGE
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    for i in range(3):
        print(DATA['query']['search'][i]['title'])

