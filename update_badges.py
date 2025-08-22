import requests
import re
import urllib.parse

CREDLY_USER = "rody-angel-uzuriaga-aviles"
CREDLY_API_URL = f"https://www.credly.com/users/{CREDLY_USER}/badges.json?page=1"
HEADERS = {"User-Agent": "Mozilla/5.0"}

WESERV_URL = "https://images.weserv.nl/?url="

BADGES_PER_ROW = 7

def fetch_badges():
    resp = requests.get(CREDLY_API_URL, headers=HEADERS)
    if resp.status_code != 200:
        print(f"Error al obtener datos de Credly: {resp.status_code}")
        return []

    data = resp.json()
    badges = []

    for item in data.get("data", []):
        attributes = item.get("badge_template", {})
        name = attributes.get("name", "Badge")
        img = attributes.get("image_url", "")
        link = attributes.get("global_activity_url", "")
        if img and link:
            img_encoded = urllib.parse.quote(img, safe='')
            img_proxy = f"{WESERV_URL}{img_encoded}&h=100"
            badges.append({
                "name": name,
                "img": img_proxy,
                "link": link
            })
    return badges

def generate_badges_html(badges):
    if not badges:
        return "<div align='center'>No se encontraron badges</div>"

    html = '<table align="center" cellspacing="10">\n'
    for i in range(0, len(badges), BADGES_PER_ROW):
        row_badges = badges[i:i+BADGES_PER_ROW]
        html += "  <tr>\n"
        for b in row_badges:
            html += f'    <td align="center">'
            html += f'<a href="{b["link"]}" target="_blank" title="{b["name"]}">'
            html += f'<img src="{b["img"]}" alt="{b["name"]}" height="100"></a></td>\n'
        html += "  </tr>\n"
    html += "</table>\n"
    return html

def update_readme(html):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    new_content = re.sub(
        r"<!--START_SECTION:badges-->.*<!--END_SECTION:badges-->",
        f"<!--START_SECTION:badges-->\n{html}\n<!--END_SECTION:badges-->",
        content,
        flags=re.S
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README.md actualizado correctamente con badges.")

if __name__ == "__main__":
    badges = fetch_badges()
    html = generate_badges_html(badges)
    update_readme(html)
