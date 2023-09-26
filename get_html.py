
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

def get_new_html(url):

    service = Service(executable_path='../startup_parsing_and_analysis/chromed/chromedriver')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    try:
        driver.get(url=url)
        i = 0
        pages = 5
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






def main():
    get_new_html(url="https://www.producthunt.com/")



if __name__ == "__main__":
    main()