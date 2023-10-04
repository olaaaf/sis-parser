from bs4 import BeautifulSoup
import pandas as pd

html_content = ""
with open("sis.html", mode="r", encoding="utf-8") as html_file:
    html_content = html_file.read()

soup = BeautifulSoup(html_content, "html.parser")
table = soup.find("table", {"class": "table table-bordered table-striped", "id": "tb"})
