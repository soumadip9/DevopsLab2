import argparse
from datetime import date, timedelta
from src.scraper import check_case_by_cnr, get_cause_list_html, parse_cause_list
from src.output import save_json
from src.downloader import download_file

import os

def main():
    parser = argparse.ArgumentParser(description="eCourts Scraper")
    parser.add_argument("--cnr")
    parser.add_argument("--today", action="store_true")
    parser.add_argument("--tomorrow", action="store_true")
    parser.add_argument("--causelist", action="store_true")
    parser.add_argument("--download-pdf", action="store_true")
    parser.add_argument("--out", default="results.json")
    args = parser.parse_args()

    target = date.today()
    if args.tomorrow:
        target += timedelta(days=1)

    if args.cnr:
        match, data = check_case_by_cnr(args.cnr, target)
        print("Match found:" if match else "No match found.")
        if match:
            print(match)
        save_json(args.out, {"date": str(target), "match": match})
        if args.download_pdf and match and match["pdf"]:
            name = os.path.basename(match["pdf"])
            download_file(match["pdf"], name)
            print("Downloaded:", name)

    elif args.causelist:
        html = get_cause_list_html(target)
        data = parse_cause_list(html)
        save_json(args.out, {"date": str(target), "count": len(data), "data": data})
        print(f"Saved {len(data)} records to {args.out}")
        if args.download_pdf:
            for row in data:
                if row["pdf"]:
                    name = os.path.basename(row["pdf"])
                    download_file(row["pdf"], name)
                    print("Downloaded:", name)

if __name__ == "__main__":
    main()
