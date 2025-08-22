import requests
import re

url = "https://www.credly.com/users/rody-angel-uzuriaga-aviles/badges.json?page=1"
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers)
data = resp.json()

badges = []
for item in data.get("data", []):
    template = item.get("badge_template", {})
    img = template.get("image_url")
    if img:
        badges.append(f'<img src="{img}" alt="badge" height="100" style="margin:5px"/>')

badges_html = f'<div align="center">{"".join(badges)}</div>' if badges else "<p>No se encontraron insignias</p>"

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
