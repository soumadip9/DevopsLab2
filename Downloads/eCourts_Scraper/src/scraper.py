import requests
from bs4 import BeautifulSoup
from tenacity import retry, wait_exponential, stop_after_attempt
from datetime import date

HEADERS = {"User-Agent": "eCourts-Scraper/1.0"}

@retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3))
def fetch(url, params=None):
    r = requests.get(url, params=params, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.text

def get_cause_list_html(target_date):
    url = "https://services.ecourts.gov.in/ecourtindia_v6/causelists"
    params = {"date": target_date.strftime("%d-%m-%Y")}
    return fetch(url, params)

def parse_cause_list(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    rows = []
    if not table:
        return rows
    for tr in table.find_all("tr"):
        tds = [td.get_text(strip=True) for td in tr.find_all("td")]
        if not tds:
            continue
        serial = tds[0] if len(tds) > 0 else ""
        case_no = tds[1] if len(tds) > 1 else ""
        court_name = tds[2] if len(tds) > 2 else ""
        link = None
        tag = tr.find("a", href=True)
        if tag and tag["href"].endswith(".pdf"):
            link = tag["href"]
        rows.append({
            "serial": serial,
            "case_no": case_no,
            "court_name": court_name,
            "pdf": link
        })
    return rows

def find_case_by_cnr(data, cnr):
    for item in data:
        if cnr.lower() in item.get("case_no", "").lower():
            return item
    return None

def check_case_by_cnr(cnr, target_date):
    html = get_cause_list_html(target_date)
    data = parse_cause_list(html)
    match = find_case_by_cnr(data, cnr)
    return match, data
