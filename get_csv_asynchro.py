import json
import csv
import time
import asyncio
import aiohttp
from bs4 import BeautifulSoup


start_time = time.time()

WEB_HDRS = {
        "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
}


async def get_csv_by_url(session, url):
    url = 'https://www.producthunt.com' + url.strip()

    async with session.get(url) as resp:
        resp_text = await resp.text()
        soup = BeautifulSoup(resp_text, 'lxml')
        script = soup.find('script', {'id': '__NEXT_DATA__'})
        json_obj = json.loads(script.contents[0])
        product_id = [i for i in json_obj['props']['apolloState'].keys() if i[0:7] == 'Product'][0]
        product_info = json_obj['props']['apolloState'][product_id]
        post_id = [i for i in json_obj['props']['apolloState'].keys() if
                   i[0:4] == 'Post' and 'name' in json_obj['props']['apolloState'][i].keys()][0]
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
        tags = [i.text for i in soup.find_all('a', class_='styles_blank__s17fb')]
        description = post_info['description'].replace("\n", "")
        try:
            creation_date = post_info['createdAt'][0:10]
        except:
            creation_date = None
        print(title, creation_date)

        with open('ph_data_table_async.csv', 'a') as file:
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



async  def gather_data(url_list):
    async with aiohttp.ClientSession(headers=WEB_HDRS) as session:
        tasks = []

        for url in url_list:
            task = asyncio.create_task(get_csv_by_url(session, url))
            tasks.append(task)

            await asyncio.gather(*tasks)











def main():

    file = open('ph_items_urls', 'r')
    urls = file.readlines()
    with open('ph_data_table_async.csv', 'w') as file:
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
                "Created at",
            )
        )
    asyncio.run(gather_data(urls[0:5]))



    finish_time = time.time() - start_time
    print(f"script execution time: {finish_time}")




if __name__ == "__main__":
    main()