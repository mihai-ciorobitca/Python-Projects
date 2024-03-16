from bs4 import BeautifulSoup as BS
from requests import get
from time import sleep
from json import dump, load

url = "https://www.librabank.ro/jobs/aplica/1099"

def get_words():
    with open("names.json", "r") as f:
        names = load(f)
    times = 1
    len_words = len(names)
    while len_words < 20:
        r = get(url)
        content = r.content
        soup = BS(content, "html.parser")
        name = soup.select_one(".mainButton").select_one("span").text
        if name not in names:
            names[name] = ""
            len_words += 1
        print(f"Tried {times} times")
        times += 1
        sleep(1)
    with open("names.json", "w") as f:
        dump(names, f, indent=2)
