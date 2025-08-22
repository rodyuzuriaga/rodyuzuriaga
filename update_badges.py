import requests
from pathlib import Path
import re

badges_dir = Path("badges")
badges_dir.mkdir(exist_ok=True)

url = "https://www.credly.com/users/rody-angel-uzuriaga-aviles/badges.json?page=1"
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers)
data = resp.json()

badge_tags = []

for item in data.get("data", []):
    badge_name = item.get("badge_template", {}).get("name", "Badge")
    badge_img_url = item.get("badge_template", {}).get("image_url", item.get("earner_photo_url", ""))
    badge_link = item.get("url")
    
    if not badge_img_url or not badge_link:
        continue
    
    filename = f"{badge_name.replace(' ', '_').replace('/', '_')}.png"
    local_path = badges_dir / filename

    if not local_path.exists():
        r = requests.get(badge_img_url, headers=headers)
        if r.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(r.content)
    
    badge_tags.append(f'<a href="{badge_link}" target="_blank"><img src="{local_path.as_posix()}" height="100" style="margin:5px"/></a>')

badges_html = "<div align='center'>" + "\n".join(badge_tags) + "</div>"

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
