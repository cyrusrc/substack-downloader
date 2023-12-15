import json
import os
import random
import requests
import time

from bs4 import BeautifulSoup

DOMAIN = '<FILL THIS IN>'
FULL_URL = 'https://{}'.format(DOMAIN)
OUTPUT_PATH = './{}'.format(DOMAIN)
PAGE_SIZE = 12
SLEEP_SECONDS = 5

HEADERS = {
    'authority': DOMAIN,
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '<FILL THIS IN>',
    'dnt': '1',
    'referer': '{}/archive?sort=new'.format(FULL_URL),
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}


# Download the list of posts to the output path.
def download_posts(posts, output_path):
    for post in posts:
        date = post['post_date'][:len('YYYY-MM-DD')]
        slug = post['slug']

        file_name = '{}-{}.html'.format(date, slug)
        full_path = '{}/{}'.format(output_path, file_name)

        response = requests.get(post['canonical_url'], headers=HEADERS)

        # Discard extracted <script> tags to ditch things like analytics
        # and to prevent the page from hiding the post text on load.
        soup = BeautifulSoup(response.content, 'html.parser')
        _ = [tag.extract() for tag in soup.findAll('script')]

        print('Writing "{} to {}'.format(slug, full_path))

        with open(full_path, 'w') as file:
            file.write(str(soup))

        randomized_sleep()


# Get a list of all posts for the given domain.
def get_posts(domain, full_url, page_size):
    offset = 0
    posts = []

    while True:
        print('Getting posts {}-{} for {}'.format(
            offset,
            offset + PAGE_SIZE,
            DOMAIN)
        )

        response = requests.get(
            '{}/api/v1/archive'.format(FULL_URL),
            params={
                'sort': 'new',
                'search': '',
                'offset': offset,
                'limit': PAGE_SIZE,
            },
            headers=HEADERS
        )

        next_posts_batch = response.json()
        posts += next_posts_batch

        if len(next_posts_batch) == 0:
            break
        else:
            offset += PAGE_SIZE
            randomized_sleep()

    return posts


def make_output_directory(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)


# Sleep between 0 and `SLEEP_SECONDS` seconds to avoid rate limiting
# and to be nice to Substack's API.
def randomized_sleep():
    sleep_length = random.random() * SLEEP_SECONDS

    print('...sleeping {} seconds'.format(round(sleep_length, 2)))
    time.sleep(sleep_length)


if __name__ == '__main__':
    # Ensure output directory exists before continuing.
    make_output_directory(OUTPUT_PATH)

    posts = get_posts(DOMAIN, FULL_URL, PAGE_SIZE)
    download_posts(posts, OUTPUT_PATH)
