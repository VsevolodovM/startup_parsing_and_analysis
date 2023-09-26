from bs4 import BeautifulSoup


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
    get_items_urls(file_path = "../ph_html_365_scrolls")


if __name__ == "__main__":
    main()