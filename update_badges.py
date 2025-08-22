import requests
import re
from math import ceil

url = "https://www.credly.com/users/rody-angel-uzuriaga-aviles/badges.json?page=1"
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers)
data = resp.json()

badges = []
for item in data.get("data", []):
    attributes = item.get("badge_template", {})
    link = attributes.get("global_activity_url", "")
    img = attributes.get("image_url", item.get("earner_photo_url", ""))
    name = attributes.get("name", "Badge")
    if link and img:
        badges.append(f"[![{name}]({img})]({link})<br>{name}")

columns = 3
rows = ceil(len(badges) / columns)
table_rows = []

for r in range(rows):
    row = badges[r*columns:(r+1)*columns]
    table_rows.append("| " + " | ".join(row) + " |")

separator = "| " + " | ".join(["---"]*columns) + " |"
table_md = "\n".join([table_rows[0], separator] + table_rows[1:]) if badges else "No se encontraron insignias en Credly"

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

new_content = re.sub(
    r"<!--START_SECTION:badges-->.*<!--END_SECTION:badges-->",
    f"<!--START_SECTION:badges-->\n{table_md}\n<!--END_SECTION:badges-->",
    content,
    flags=re.S
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)
