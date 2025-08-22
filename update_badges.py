import requests
import re

url = "https://www.credly.com/users/rody-angel-uzuriaga-aviles/badges.json?page=1"
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers)
data = resp.json()

badges = []
for item in data.get("data", []):
    attributes = item.get("badge_template", {})
    img = attributes.get("image_url", item.get("earner_photo_url", ""))
    if img:
        badges.append(f'<img src="{img}" height="100"/>')

badges_html = " ".join(badges) if badges else "<p>No se encontraron insignias en Credly</p>"

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

new_content = re.sub(
    r"<!--START_SECTION:badges-->.*<!--END_SECTION:badges-->",
    f"<!--START_SECTION:badges-->\n<div align='center'>{badges_html}</div>\n<!--END_SECTION:badges-->",
    content,
    flags=re.S
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)
