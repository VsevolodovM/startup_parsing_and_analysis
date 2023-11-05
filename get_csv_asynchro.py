from fake_useragent import UserAgent
import json
import csv
import time
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import brotli


start_time = time.time()
WEB_HDRS = {
        "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
}
data = {"operationName":"PostPage","variables":{"slug":"200-growth-marketing-resources"},"query":"query PostPage($slug:String!$badgeTypes:[BadgesTypeEnum!]){post(slug:$slug){id slug name trashedAt isArchived product{id slug passedOnePost ...ProductPageReviewSummaryFragment ...ReviewCardFragment __typename}targetedAd(kind:\"sidebar\"){id ...AdFragment __typename}redirectToProduct{id slug __typename}...PostPageHeaderFragment ...PostPageDescriptionFragment ...PostPageScheduledNoticeFragment ...PostPageLaunchDayNoticeFragment ...PostPageModerationReasonFragment ...PostPageModerationToolsFragment ...PostPageBreadcrumbFragment ...PostPageAboutFragment ...PostPageGalleryFragment ...PostPageBannerFragment ...PostPageCommentPromptFragment ...StructuredDataFromPost ...MetaTags __typename}}fragment MetaTags on SEOInterface{id meta{canonicalUrl creator description image mobileAppUrl oembedUrl robots title type author authorUrl __typename}__typename}fragment StructuredDataFromPost on Post{id structuredData __typename}fragment PostPageHeaderFragment on Post{id name tagline dailyRank createdAt ...PostThumbnail ...PostStatusIcons ...PostVoteButtonFragment ...PostPageGetItButtonFragment ...PostHeaderBadgesFragment ...PostPageActionsFragment __typename}fragment PostStatusIcons on Post{id name productState __typename}fragment PostThumbnail on Post{id name thumbnailImageUuid ...PostStatusIcons __typename}fragment PostVoteButtonFragment on Post{id featuredAt updatedAt createdAt product{id isSubscribed __typename}disabledWhenScheduled hasVoted ...on Votable{id votesCount __typename}__typename}fragment PostPageGetItButtonFragment on Post{id isAvailable productState links{id redirectPath storeName websiteName devices __typename}__typename}fragment PostHeaderBadgesFragment on Post{id badges(first:3 types:$badgeTypes){edges{node{...ProductBadgeFragment __typename}__typename}__typename}__typename}fragment ProductBadgeFragment on Badge{...on TopPostBadge{id ...ProductTopPostBadgeFragment __typename}...on GoldenKittyAwardBadge{id ...ProductGoldenKittyBadgeFragment __typename}...on TopPostTopicBadge{id ...ProductTopPostTopicBadgeFragment __typename}__typename}fragment ProductTopPostBadgeFragment on TopPostBadge{id post{id name __typename}position period date __typename}fragment ProductGoldenKittyBadgeFragment on GoldenKittyAwardBadge{id year position category post{id name __typename}__typename}fragment ProductTopPostTopicBadgeFragment on TopPostTopicBadge{id __typename}fragment PostPageActionsFragment on Post{id slug userId canManage __typename}fragment PostPageDescriptionFragment on Post{id slug tagline description pricingType isArchived createdAt featuredAt ...ShareModalSubjectFragment ...PostThumbnail ...PostPromoCodeFragment product{id slug name tagline logoUuid ...CollectionAddButtonFragment __typename}topics(first:3){edges{node{id slug name __typename}__typename}totalCount __typename}__typename}fragment PostPromoCodeFragment on Post{id promo{text code __typename}__typename}fragment ShareModalSubjectFragment on Shareable{id url ...FacebookShareButtonFragment __typename}fragment FacebookShareButtonFragment on Shareable{id url __typename}fragment CollectionAddButtonFragment on Product{id name description ...ProductItemFragment __typename}fragment ProductItemFragment on Product{id slug name tagline followersCount reviewsCount topics(first:2){edges{node{id slug name __typename}__typename}__typename}...ProductFollowButtonFragment ...ProductThumbnailFragment ...ProductMuteButtonFragment ...FacebookShareButtonV6Fragment ...ReviewStarRatingCTAFragment __typename}fragment ProductThumbnailFragment on Product{id name logoUuid isNoLongerOnline __typename}fragment ProductFollowButtonFragment on Product{id followersCount isSubscribed __typename}fragment ProductMuteButtonFragment on Product{id isMuted __typename}fragment FacebookShareButtonV6Fragment on Shareable{id url __typename}fragment ReviewStarRatingCTAFragment on Product{id slug name isMaker reviewsRating __typename}fragment PostPageScheduledNoticeFragment on Post{id slug name createdAt canCreateUpcomingEvent canViewUpcomingEventCreateBtn upcomingEvent{id canEdit approved __typename}product{id name slug canEdit ...TeamRequestCTAFragment __typename}__typename}fragment TeamRequestCTAFragment on Product{id slug name websiteUrl websiteDomain isClaimed isViewerTeamMember viewerPendingTeamRequest{id __typename}__typename}fragment PostPageLaunchDayNoticeFragment on Post{id slug createdAt isMaker isHunter product{id slug __typename}__typename}fragment PostPageModerationReasonFragment on Post{id moderationReason{reason moderator{id name headline username __typename}__typename}__typename}fragment PostPageModerationToolsFragment on Post{id name slug featuredAt createdAt product{id __typename}...ModerationChangeProductFormPostFragment __typename}fragment ModerationChangeProductFormPostFragment on Post{id name primaryLink{id url __typename}product{id ...ModerationChangeProductFormProductFragment __typename}__typename}fragment ModerationChangeProductFormProductFragment on Product{id name slug tagline cleanUrl websiteUrl ...ProductThumbnailFragment __typename}fragment PostPageBreadcrumbFragment on Post{id slug name product{id slug __typename}__typename}fragment PostPageAboutFragment on Post{id name slug votesCount commentsCount dailyRank weeklyRank createdAt featuredAt canManage product{id name slug tagline reviewersCount reviewsCount followersCount firstPost{id createdAt __typename}...ProductThumbnailFragment ...ProductFollowButtonFragment ...ReviewStarRatingCTAFragment __typename}user{id name username ...UserImage __typename}makers{id name username ...UserImage __typename}topics(first:3){edges{node{id name slug __typename}__typename}__typename}__typename}fragment UserImage on User{id name username avatarUrl __typename}fragment PostPageGalleryFragment on Post{id name primaryLink{id url __typename}media{id originalHeight originalWidth imageUuid mediaType metadata{url videoId interactiveDemoId platform __typename}__typename}__typename}fragment PostPageBannerFragment on Post{id isArchived featuredAt createdAt product{id slug name postsCount __typename}__typename}fragment AdFragment on Ad{id subject post{id slug name updatedAt commentsCount topics(first:3){edges{node{id slug __typename}__typename}__typename}...PostVoteButtonFragment __typename}ctaText name tagline thumbnailUuid url __typename}fragment PostPageCommentPromptFragment on Post{id name isArchived commentPrompt ...PostThumbnail __typename}fragment ProductPageReviewSummaryFragment on Product{id name slug postsCount reviewsCount reviewersCount reviewsRating isMaker reviewers(first:3){edges{node{id username name ...UserImage __typename}__typename}__typename}...ReviewCTAPromptFragment __typename}fragment ReviewCTAPromptFragment on Product{id isMaker viewerReview{id __typename}...ReviewCTASharePromptFragment __typename}fragment ReviewCTASharePromptFragment on Product{id name tagline slug ...ProductThumbnailFragment ...FacebookShareButtonFragment __typename}fragment ReviewCardFragment on Product{id name isMaker ...ReviewCTAPromptFragment __typename}"}

async def get_csv_by_url(session, url):
    # url = 'https://www.producthunt.com/products/' + url.strip()[7:] #+ '#' + url.strip()[7:]
    url = 'https://www.producthunt.com/frontend/graphql'
    print(url)

    async with session.post(url, json = data) as resp:
        await asyncio.sleep(0.05)
        # resp_text = await resp.text()
        # brotli.decompress(await resp.text())
        print(await resp.text())

        # soup = BeautifulSoup(resp_text, 'lxml')
        # print(resp_text )
        # script = soup.find('script', {'id': '__NEXT_DATA__'})
        # json_obj = json.loads(script.contents[0])
        # product_id = [i for i in json_obj['props']['apolloState'].keys() if
        #               i[0:7] == 'Product' and 'tagline' in json_obj['props']['apolloState'][i].keys()][0]
        # product_info = json_obj['props']['apolloState'][product_id]
        # post_id = [i for i in json_obj['props']['apolloState'].keys() if
        #            i[0:4] == 'Post' and 'name' in json_obj['props']['apolloState'][i].keys()][0]
        # post_info = json_obj['props']['apolloState'][post_id]
        #
        # title = post_info['name']
        # try:
        #     tag_line = post_info['tagline']
        # except:
        #     try:
        #         tag_line = product_info['tagline']
        #     except:
        #         tag_line = None
        #
        # try:
        #     link = product_info['websiteUrl']
        # except:
        #     try:
        #         link = post_info['websiteUrl']
        #     except:
        #         link = None
        #
        # try:
        #     upvotes = post_info['votesCount']
        # except:
        #     try:
        #         upvotes = product_info['votesCount']
        #     except:
        #         upvotes = None
        #
        # try:
        #     comments = post_info['commentsCount']
        # except:
        #     try:
        #         comments = product_info['commentsCount']
        #     except:
        #         comments = None
        #
        # try:
        #     reviews = product_info['reviewsCount']
        # except:
        #     try:
        #         reviews = post_info['reviewsCount']
        #     except:
        #         reviews = None
        #
        # try:
        #     reviews_rating = product_info['reviewsRating']
        # except:
        #     try:
        #         reviews_rating = post_info['reviewsRating']
        #     except:
        #         reviews_rating = None
        #
        # try:
        #     followers = product_info['followersCount']
        # except:
        #     try:
        #         followers = post_info['followersCount']
        #     except:
        #         followers = None
        #
        # try:
        #     day_rank = post_info['dailyRank']
        # except:
        #     try:
        #         day_rank = product_info['dailyRank']
        #     except:
        #         day_rank = None
        #
        # try:
        #     week_rank = post_info['weeklyRank']
        # except:
        #     try:
        #         week_rank = product_info['weeklyRank']
        #     except:
        #         week_rank = None
        #
        # price_type = soup.find('div', attrs={'data-test': 'pricing-type'}).text()
        #
        #
        # try:
        #     tags = tuple([i.text for i in soup.find_all('a', class_='styles_blank__s17fb')])
        # except:
        #     tags = None
        #
        # try:
        #     description = post_info['description'].replace("\n", "")
        # except:
        #     description = None
        #
        # try:
        #     creation_date = post_info['createdAt'][0:10]
        # except:
        #     creation_date = None
        #
        #
        # with open('ph_data_table_async.csv', 'a') as file:
        #     writer = csv.writer(file)
        #
        #     writer.writerow(
        #         (
        #             title,
        #             tag_line,
        #             link,
        #             upvotes,
        #             comments,
        #             reviews,
        #             reviews_rating,
        #             followers,
        #             day_rank,
        #             week_rank,
        #             price_type,
        #             tags,
        #             description,
        #             creation_date
        #         )
        #     )



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
    asyncio.run(gather_data(urls[0:1]))



    finish_time = time.time() - start_time
    print(f"script execution time: {finish_time}")




if __name__ == "__main__":
    main()