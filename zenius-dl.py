#!/usr/bin/env python

import re
from requests import get
from bs4 import BeautifulSoup


def download_category(url):
    print('Fetching %s...' % url)
    soup = BeautifulSoup(get(url).content)

    # Get list of simfile IDs
    SIMFILE_REGEX = re.compile('viewsimfile\.php\?simfileid=(\d+)')
    hrefs = soup.find_all('a', href=SIMFILE_REGEX)
    ids = [SIMFILE_REGEX.search(href['href']).group(1) for href in hrefs]

    # Create simfile download URLS
    DL_PATTERN = 'https://zenius-i-vanisher.com/v5.2/download.php?type=ddrsimfilecustom&simfileid=%s'
    dl_urls = [DL_PATTERN % id for id in ids]

    # Download them!
    # XXX: EXTREMELY dirty shell call to wget. Should add an option to output
    # URLs only so user can pipe them to their downloader of choice.
    from subprocess import call
    for dl_url in dl_urls:
        print('> Downloading %s...' % dl_url)
        call(['wget',
              '--content-disposition',  # use filename in redirected URL
              '--directory-prefix', 'downloads',  # put files in downloads dir
              dl_url])


if __name__ == '__main__':
    import sys
    download_category(sys.argv[1])
