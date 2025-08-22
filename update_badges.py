import requests
import re

url = "https://www.credly.com/users/rody-angel-uzuriaga-aviles/badges.json?page=1"
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers)
data = resp.json()

badges = []
for item in data.get("data", []):
    template = item.get("badge_template", {})
    img = template.get("image_url") or item.get("image_url") or item.get("earner_photo_url")
    link = template.get("global_activity_url") or template.get("vanity_url") or "#"
    name = template.get("name", "Badge")
    if img and link:
        badges.append(f'[![{name}]({img})]({link})')

badges_md = "<br>".join(badges) if badges else "No se encontraron insignias en Credly"

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

new_content = re.sub(
    r"<!--START_SECTION:badges-->.*<!--END_SECTION:badges-->",
    f"<!--START_SECTION:badges-->\n{badges_md}\n<!--END_SECTION:badges-->",
    content,
    flags=re.S
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)
