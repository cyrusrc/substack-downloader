import json
import os
import random
import requests
import time
import argparse

from bs4 import BeautifulSoup

DOMAIN = None
FULL_URL = None
OUTPUT_PATH = None

PAGE_SIZE = 12
SLEEP_SECONDS = 5
BEGIN_OFFSET = 0

HEADERS = {
    'authority': DOMAIN,
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '',
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

        print('Writing "{}" to {}'.format(slug, full_path))

        with open(full_path, 'w') as file:
            file.write(str(soup))

        randomized_sleep()


# Get a list of all posts for the given domain.
def get_posts(domain, full_url, page_size, begin_offset):
    offset = begin_offset
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


def parse_args():
    parser = argparse.ArgumentParser(
        description="Substack Downloader",
        epilog="See README.md for more information"
    )
    parser.add_argument('domain', help="domain of the site you want to archive, for instance `read.substack.com`")
    parser.add_argument('cookie', help="path to a cookie file")
    parser.add_argument('-o', '--output-path', dest='output', help="output path, defaults to ./{domain}")
    parser.add_argument('-u', '--full-url', dest='url', help="full URL of the substack, defaults to https://{domain}")
    parser.add_argument('-p', '--page-size', type=int, dest='page_size', default=PAGE_SIZE, help="page size for HTTP requests")
    parser.add_argument('-s', '--sleep-time', type=int, dest='sleep_time', default=SLEEP_SECONDS, help="sleep time in seconds between requests")
    parser.add_argument('-b', '--begin-offset', type=int, dest='begin_offset', default=BEGIN_OFFSET, help="the beginning offset of articles to include")
    return parser.parse_args()
    
    
if __name__ == '__main__':
    args = parse_args()

    DOMAIN = args.domain
    FULL_URL = args.url if args.url else 'https://{}'.format(args.domain)
    OUTPUT_PATH = args.output if args.output else './{}'.format(args.domain)
    with open(args.cookie, 'r') as cookie_file:
        cookie = cookie_file.read().strip()
        HEADERS['cookie'] = cookie

    PAGE_SIZE = args.page_size
    SLEEP_SECONDS = args.sleep_time
    BEGIN_OFFSET = args.begin_offset

    # Ensure output directory exists before continuing.
    make_output_directory(OUTPUT_PATH)

    posts = get_posts(DOMAIN, FULL_URL, PAGE_SIZE, BEGIN_OFFSET)
    download_posts(posts, OUTPUT_PATH)
