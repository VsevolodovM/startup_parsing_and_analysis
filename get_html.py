import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

def get_new_html(url):

    service = Service(executable_path='/home/mikhail/Desktop/parsing/startup_parsing_and_analysis/chromed/chromedriver')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    try:
        driver.get(url=url)
        i = 0
        pages = 20
        while True:
            if i >= pages:
                break
            print('page:', i)
            time.sleep(1.5)                                                                       #change this to smaller value if u have good internet connection

            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            if driver.find_elements("xpath", "//button[contains(text(), 'View all from')]"):
                 buttons = driver.find_elements("xpath", "//button[contains(text(), 'View all from')]")
                 for btn in buttons:
                     btn.click()
                     time.sleep(1)


            i += 1


    except Exception as _ex:
        print(_ex)
    finally:
        time.sleep(10)
        with open(f'ph_html_{i}_scrolls', 'w') as file:
            file.write(driver.page_source)
        driver.close()
        driver.quit()



def get_items_urls(file_path):
    with open(file_path) as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    items_divs = soup.find_all('div', class_="styles_item__Dk_nz")

    urls = []
    for item in items_divs:
        item_url = item.find("a").get("href")
        urls.append(item_url)

    with open("ph_items_urls", "w") as file:
        for url in urls:
            file.write(f"{url}\n")
        return print("[INFO] Urls collected successfully")


def main():
    #get_new_html(url="https://www.producthunt.com/")
    print(get_items_urls(file_path = "/home/mikhail/Desktop/parsing/startup_parsing_and_analysis/ph_html_365_scrolls"))


if __name__ == "__main__":
    main()