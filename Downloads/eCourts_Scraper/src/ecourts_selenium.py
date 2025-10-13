from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def search_by_cnr(cnr_number):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")

    try:
        cnr_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "cino"))
        )
        cnr_input.send_keys(cnr_number)

        print("\n🧩 Please solve the CAPTCHA manually in the browser window.")
        input("Press Enter here in the terminal after solving the CAPTCHA and clicking Search... ")

        # ✅ Wait for the case result section to appear
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "history_cnr"))
            )
            print("📄 Case result loaded.")
        except:
            print("⚠️ Result not detected — saving page anyway.")

        time.sleep(2)
        page_source = driver.page_source

        with open("result_page.html", "w", encoding="utf8") as f:
            f.write(page_source)

        print("✅ Page saved as result_page.html")

    finally:
        driver.quit()
        print("🚪 Browser closed.")

if __name__ == "__main__":
    cnr = input("Enter 16-digit CNR number: ").strip()
    search_by_cnr(cnr)
