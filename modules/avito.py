from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import time

def search_avito_flats(district, budget_val):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={UserAgent().random}")
    options.add_argument("--lang=ru-RU,ru")

    url = f"https://www.avito.ru/moskva/kvartiry/sdam-ASgBAgICAUSSA8YQ?cd=1&q={district}&pmax={budget_val}"

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)   # <-- вот тут!

    driver.get(url)
    time.sleep(4)  # можно увеличить до 6-8 при медленном инете

    results = []
    flats = driver.find_elements(By.CSS_SELECTOR, '[data-marker="item"]')
    for item in flats[:10]:
        try:
            title = item.find_element(By.CSS_SELECTOR, '[itemprop="name"]').text
            desc_el = item.find_elements(By.CSS_SELECTOR, '[data-marker="item-description"]')
            desc = desc_el[0].text if desc_el else ""
            price = int(''.join(filter(str.isdigit, item.find_element(By.CSS_SELECTOR, '[itemprop="price"]').text)))
            link = item.find_element(By.CSS_SELECTOR, '[data-marker="item-title"]').get_attribute("href")
            results.append({
                "title": title,
                "desc": desc,
                "price": price,
                "link": link
            })
        except Exception:
            continue

    driver.quit()
    return results