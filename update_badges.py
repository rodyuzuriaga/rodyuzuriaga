import requests
import re

url = "https://www.credly.com/users/rody-angel-uzuriaga-aviles/badges.json?page=1"

headers = {
    "User-Agent": "Mozilla/5.0"
}
resp = requests.get(url, headers=headers)
data = resp.json()

badges = []
for item in data.get("data", []):
    attributes = item.get("badge_template", {})
    link = attributes.get("global_activity_url", "")
    img = attributes.get("image_url", item.get("image_url", ""))
    name = attributes.get("name", "Badge")
    if link and img:
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
