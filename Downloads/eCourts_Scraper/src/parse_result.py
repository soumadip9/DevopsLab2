from bs4 import BeautifulSoup
import json

with open("result_page.html", "r", encoding="utf8") as f:
    soup = BeautifulSoup(f, "html.parser")

data = {}

court_title = soup.find("div", class_="container-fluid")
if court_title:
    heading = court_title.find("div", string=lambda x: x and "Judge" in x)
    if heading:
        data["Court Name"] = heading.get_text(strip=True)

case_details_table = soup.find("table", class_="table")
if case_details_table:
    for row in case_details_table.find_all("tr"):
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        if len(cells) == 2:
            data[cells[0]] = cells[1]

status_rows = soup.select("div[style*='border'] tr, table tr")
for row in status_rows:
    cols = [c.get_text(strip=True) for c in row.find_all("td")]
    if len(cols) == 2:
        data[cols[0]] = cols[1]

pet_adv_section = soup.find("div", string=lambda x: x and "Petitioner" in x)
if pet_adv_section:
    data["Petitioner and Advocate"] = pet_adv_section.get_text(strip=True)

if "No Record Found" in soup.get_text():
    print("⚠️ No record found for this CNR.")
else:
    with open("case_data.json", "w", encoding="utf8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("✅ Extracted case details saved to case_data.json")
