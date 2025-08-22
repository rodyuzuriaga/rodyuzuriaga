import requests
from bs4 import BeautifulSoup
import re

url = "https://www.credly.com/users/rody-angel-uzuriaga-aviles"

html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

badges = []
for badge in soup.select("div.cr-standard-grid-item"):
    link = badge.find("a", href=True)
    img = badge.find("img", src=True)
    if link and img:
        name = img["alt"]
        badges.append(f'<a href="https://www.credly.com{link["href"]}"><img src="{img["src"]}" alt="{name}" height="100"/></a>')

badges_html = "\n".join(badges)

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

new_content = re.sub(
    r"<!--START_SECTION:badges-->.*<!--END_SECTION:badges-->",
    f"<!--START_SECTION:badges-->\n{badges_html}\n<!--END_SECTION:badges-->",
    content,
    flags=re.S
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)
