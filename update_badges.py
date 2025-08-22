import requests
from bs4 import BeautifulSoup
import re

url = "https://www.credly.com/users/rody-angel-uzuriaga-aviles/badges"

html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

badges = []

for badge in soup.select('div[data-testid="badge-card"]'):
    link_tag = badge.find("a", href=True)
    img_tag = badge.find("img", src=True)
    if link_tag and img_tag:
        link = "https://www.credly.com" + link_tag["href"]
        img = img_tag["src"]
        name = img_tag.get("alt", "Badge")
        badges.append(f'<a href="{link}"><img src="{img}" alt="{name}" height="100"/></a>')

if not badges:
    badges_html = "<p>No se encontraron insignias en Credly</p>"
else:
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
