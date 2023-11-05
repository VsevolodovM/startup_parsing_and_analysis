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
        print(req.text)
        soup = BeautifulSoup(req.text, 'lxml')
        script = soup.find('script', {'id' : '__NEXT_DATA__'})
        json_obj = json.loads(script.contents[0])
        product_id = [i for i in json_obj['props']['apolloState'].keys() if i[0:7] == 'Product'][0]
        product_id = [i for i in json_obj['props']['apolloState'].keys() if
                      i[0:7] == 'Product' and 'tagline' in json_obj['props']['apolloState'][i].keys()][0]
        product_info = json_obj['props']['apolloState'][product_id]
        post_id = [i for i in json_obj['props']['apolloState'].keys() if
                   i[0:4] == 'Post' and 'name' in json_obj['props']['apolloState'][i].keys()][0]
        post_info = json_obj['props']['apolloState'][post_id]

        title = post_info['name']
        try:
            tag_line = post_info['tagline']
        except:
            try:
                tag_line = product_info['tagline']
            except:
                tag_line = None

        try:
            link = product_info['websiteUrl']
        except:
            try:
                link = post_info['websiteUrl']
            except:
                link = None

        try:
            upvotes = post_info['votesCount']
        except:
            try:
                upvotes = product_info['votesCount']
            except:
                upvotes = None

        try:
            comments = post_info['commentsCount']
        except:
            try:
                comments = product_info['commentsCount']
            except:
                comments = None

        try:
            reviews = product_info['reviewsCount']
        except:
            try:
                reviews = post_info['reviewsCount']
            except:
                reviews = None

        try:
            reviews_rating = product_info['reviewsRating']
        except:
            try:
                reviews_rating = post_info['reviewsRating']
            except:
                reviews_rating = None

        try:
            followers = product_info['followersCount']
        except:
            try:
                followers = post_info['followersCount']
            except:
                followers = None

        try:
            day_rank = post_info['dailyRank']
        except:
            try:
                day_rank = product_info['dailyRank']
            except:
                day_rank = None

        try:
            week_rank = post_info['weeklyRank']
        except:
            try:
                week_rank = product_info['weeklyRank']
            except:
                week_rank = None
        try:
            price_type = soup.find('div', attrs={'data-test': 'pricing-type'}).text
        except:
            price_type = None

        try:
            tags = tuple([i.text for i in soup.find_all('a', class_='styles_blank__s17fb')])
        except:
            tags = None

        try:
            description = post_info['description'].replace("\n", "")
        except:
            description = None

        try:
            creation_date = post_info['createdAt'][0:10]
        except:
            creation_date = None

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

    get_csv_by_url(urls[0:1])

    finish_time = time.time() - start_time
    print(f"script execution time: {finish_time}")




if __name__ == "__main__":
    main()