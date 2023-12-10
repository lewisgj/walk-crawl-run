import unittest

from aioresponses import aioresponses

from walkcrawlrun.crawlers.concurrent import ConcurrentCrawler


class TestConcurrentCrawl(unittest.IsolatedAsyncioTestCase):
    async def test_should_follow_links_but_not_loop_endlessly(self):
        with aioresponses() as m:
            m.get(
                "https://example.com",
                body='<html><body><a href="https://example.com/about">About</a></body></html>',
                repeat=True,  # https://github.com/pnuckowski/aioresponses/issues/205#issuecomment-1380360014
            )
            m.get(
                "https://example.com/about",
                body='<html><body><a href="https://example.com">Home</a></body></html>',
                repeat=True,
            )

            crawler = ConcurrentCrawler("https://example.com")
            actual = await crawler.crawl()

            self.assertEqual(
                {
                    "https://example.com": {"urls": {"https://example.com/about"}},
                    "https://example.com/about": {"urls": {"https://example.com"}},
                },
                actual,
            )

    async def test_given_crawl_budget_set_only_crawl_those_many_pages(self):
        with aioresponses() as m:
            m.get(
                "https://example.com",
                body='<html><body><a href="https://example.com/about">About</a></body></html>',
                repeat=True,
            )
            m.get(
                "https://example.com/about",
                body='<html><body><a href="https://example.com">Home</a></body></html>',
                repeat=True,
            )

            crawler = ConcurrentCrawler("https://example.com")
            actual = await crawler.crawl()

            self.assertEqual(
                {
                    "https://example.com": {"urls": {"https://example.com/about"}},
                    "https://example.com/about": {"urls": {"https://example.com"}},
                },
                actual,
            )
