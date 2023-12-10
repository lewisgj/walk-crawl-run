from urllib.parse import urlsplit, urljoin

import aiohttp
from bs4 import BeautifulSoup

from walkcrawlrun.crawlers.crawl_result import CrawlResult
from walkcrawlrun.logger import logger


async def crawl_page(url: str) -> CrawlResult:
    logger.debug("page crawl start", url=url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            all_anchors = soup.find_all("a", href=True)

            normalised_hrefs = [normalise_url(url, a["href"]) for a in all_anchors]

            filtered_urls = [
                href for href in normalised_hrefs if should_include_href(url, href)
            ]

            logger.debug("urls found", url=url, found_urls=filtered_urls)
            return {url: {"urls": set(filtered_urls)}}


def normalise_url(url, href):
    return urljoin(url, href)


def should_include_href(base_url, anchor_url) -> bool:
    base_url_split = urlsplit(base_url)
    anchor_split = urlsplit(anchor_url)

    scheme_does_not_match = (
        anchor_split.scheme and anchor_split.scheme != base_url_split.scheme
    )
    if scheme_does_not_match:
        return False

    hostname_does_not_match = (
        anchor_split.hostname and anchor_split.hostname != base_url_split.hostname
    )
    if hostname_does_not_match:
        return False

    only_differs_by_fragment = (
        base_url_split.path == anchor_split.path
        and base_url_split.query == anchor_split.query
        and anchor_split.fragment
    )
    if only_differs_by_fragment:
        return False

    return True
