# Substack downloader

This package consists of a simple script for downloading an archive of posts for the configured Substack domain.

## Installation
Note: This package was developed using Python 3.11.5 on MacOS 13.5.1 (22G90) and has not been tested in other environments, but it should probably work on any platform with Python 3.

Create a virtual environment in the project root: `python -m venv venv`

Assuming you have [pip](https://pip.pypa.io/en/stable/installation/) installed, activate the project's virtual environment:
(with project root as the working directory) `. venv/bin/activate` 

Install the project requirements: `pip install -r requirements.txt`

## Running the script
 (with project root as the working directory) `python downloader.py <command-line-arguments>`

To get help on command line parameters:

 (with project root as the working directory) `python downloader.py --help`

There are two required positional arguments:

The first positional argument is the domain of the site you want to archive, for instance `read.substack.com`.

The second positional argument is a path to the cookie file. The cookie can be extracted from the browser dev tools by copying it from a network request to the Substack domain you're interested in into the cookie file. [Relevant Stack Overflow post.](https://stackoverflow.com/questions/55414344/chrome-network-request-does-not-show-cookies-tab-some-request-headers-copy-as)

The usage of the remaining optional parameters can be readily understood from the help information and by reference to the code.


## Limitations
This script has only been tested on sites with text-based articles. It does not attempt to download podcast audio or videos or any other media.
