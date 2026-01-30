import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE = "https://web.archive.org/web/20250708180027/https://www.myfootdr.com.au"

def get_soup(url):
    time.sleep(1)  
    res = requests.get(url)
    return BeautifulSoup(res.text, "html.parser")

# Step 1 — Get regional page URLs
main_url = BASE + "/our-clinics/"
main_soup = get_soup(main_url)

# find region links
region_links = []
for a in main_soup.select("a"):
    href = a.get("href", "")
    if "/our-clinics/regions/" in href:
        link = href if href.startswith("http") else BASE + href
        if link not in region_links:
            region_links.append(link)

print(f"Found {len(region_links)} regions")

# Step 2 — For each region, collect clinic URLs
clinic_links = []
for r in region_links:
    soup = get_soup(r)
    for a in soup.select("a"):
        href = a.get("href", "")
        if "/our-clinics/" in href and "regions" not in href:
            url = href if href.startswith("http") else BASE + href
            if url not in clinic_links:
                clinic_links.append(url)

print(f"Found {len(clinic_links)} clinic pages")

# Step 3 — Visit each clinic page and scrape
data = []
for url in clinic_links:
    soup = get_soup(url)
    
    # Name
    name_tag = soup.find("h1")
    name = name_tag.get_text(strip=True) if name_tag else ""

    # Phone — try common patterns
    phone = ""
    email = ""
    address = ""
    services = []

    # Phone & email scanning
    text = soup.get_text(separator="\n")
    for line in text.split("\n"):
        if "@" in line and not email:
            email = line.strip()
        if any(char.isdigit() for char in line) and ("Phone" in line or "Ph:" in line or "+" in line):
            phone = line.strip()
        if any(word in line.lower() for word in ["st", "ave", "road", "rd", "street", "way", "centre", "centre"]):
            address = line.strip()
        if any(word in line.lower() for word in ["podiatry", "orthotic", "foot", "care", "treatment"]):
            services.append(line.strip())
    
    services = "; ".join(list(set(services)))

    data.append({
        "Name of Clinic": name,
        "Address": address,
        "Email": email,
        "Phone": phone,
        "Services": services
    })

print("Scraped all clinics")

# Step 4 — Write CSV
df = pd.DataFrame(data)
df.to_csv("myfootdr_clinics.csv", index=False, encoding="utf-8")
print("CSV saved")
