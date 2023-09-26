import json
import csv
import time

import requests
from bs4 import BeautifulSoup

start_time = time.time()


def get_csv_by_url(url_list):
    with open('ph_data_table.csv', 'w') as file:
        writer = csv.writer(file)

        writer.writerow(
        (
            "Title",
            "Tag-line",
            "Url",
            "Upvotes",
            "Comments",
            "Reviews",
            "Rewiews rating",
            "Follower count",
            "Day rank",
            "Week rank",
            "Pricing type",
            "Topics",
            "Description",
            "Created at"

        )
    )
        i = 1
    for url in url_list:
        print(f'{i} / {len(url_list)}')
        url = 'https://www.producthunt.com' + url.strip()
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'lxml')
        script = soup.find('script', {'id' : '__NEXT_DATA__'})
        json_obj = json.loads(script.contents[0])
        product_id = [i for i in json_obj['props']['apolloState'].keys() if i[0:7] == 'Product'][0]
        product_info = json_obj['props']['apolloState'][product_id]
        post_id = [i for i in json_obj['props']['apolloState'].keys() if i[0:4] == 'Post' and 'name' in json_obj['props']['apolloState'][i].keys()][0]
        post_info = json_obj['props']['apolloState'][post_id]

        title = post_info['name']
        tag_line = post_info['tagline']
        link = product_info['websiteUrl']
        upvotes = post_info['votesCount']
        comments = post_info['commentsCount']
        reviews = product_info['reviewsCount']
        reviews_rating = product_info['reviewsRating']
        followers = product_info['followersCount']
        day_rank = post_info['dailyRank']
        week_rank = post_info['weeklyRank']
        try:
            price_type = soup.find('div', attrs={'data-test': 'pricing-type'}).text
        except:
            price_type = 'no info'
        tags = [i.text for i in soup.find_all('a', class_= 'styles_blank__s17fb')]
        description = post_info['description'].replace("\n", "")
        creation_date = post_info['createdAt'][0:10]

        with open('ph_data_table.csv', 'a') as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                    title,
                    tag_line,
                    link,
                    upvotes,
                    comments,
                    reviews,
                    reviews_rating,
                    followers,
                    day_rank,
                    week_rank,
                    price_type,
                    tags,
                    description,
                    creation_date
                )
            )
        i += 1
















def main():

    file = open('ph_items_urls', 'r')
    urls = file.readlines()

    get_csv_by_url(urls[0:50])

    finish_time = time.time() - start_time
    print(f"script execution time: {finish_time}")




if __name__ == "__main__":
    main()