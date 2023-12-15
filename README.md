# Substack downloader

This package consists of a simple script for downloading an archive of posts for the configured Substack domain.

## Installation
Note: This package was developed using Python 3.11.5 on MacOS 13.5.1 (22G90) and has not been tested in other environments, but it should probably work on any platform with Python 3.

Create a virtual environment in the project root: `python -m venv venv`

Assuming you have [pip](https://pip.pypa.io/en/stable/installation/) installed, activate the project's virtual environment:
(with project root as the working directory) `. venv/bin/activate` 

Install the project requirements: `pip install -r requirements.txt`

## Configuration
There are several variables that require configuration before you can run the downloader script.

`DOMAIN` must be replaced with the domain of the site you want to archive, for instance `read.substack.com`.

`OUTPUT_PATH` defaults to a subdirectory titled as the domain name within the working directory. Change it if you want the files to go elsewhere. This script will attempt to create the necessary folders for a new path but may encounter permissions errors.

The final value that needs configuration is the `'cookie'` field on the `HEADERS` object. It can be extracted from the browser dev tools by copying a network request to the Substack domain you're interested in. [Relevant Stack Overflow post.](https://stackoverflow.com/questions/55414344/chrome-network-request-does-not-show-cookies-tab-some-request-headers-copy-as)

The usage of the remaining configuration values can be readily understood by reference to the code.

Configuration section of the script:
```
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
```

## Running the script
(with project root as the working directory) `python downloader.py`

## Limitations
This script has only been tested on sites with text-based articles. It does not attempt to download podcast audio or videos or any other media.
