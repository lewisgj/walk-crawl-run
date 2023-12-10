import unittest

from aioresponses import aioresponses

from walkcrawlrun.crawlers.sync import SyncCrawler


class TestSyncCrawl(unittest.IsolatedAsyncioTestCase):
    async def test_should_follow_links_but_not_loop_endlessly(self):
        with aioresponses() as m:
            m.get(
                "https://example.com",
                body='<html><body><a href="https://example.com/about">About</a></body></html>',
            )
            m.get(
                "https://example.com/about",
                body='<html><body><a href="https://example.com">Home</a></body></html>',
            )

            crawler = SyncCrawler("https://example.com")
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
            )
            m.get(
                "https://example.com/about",
                body='<html><body><a href="https://example.com">Home</a></body></html>',
            )

            crawler = SyncCrawler("https://example.com")
            actual = await crawler.crawl()

            self.assertEqual(
                {
                    "https://example.com": {"urls": {"https://example.com/about"}},
                    "https://example.com/about": {"urls": {"https://example.com"}},
                },
                actual,
            )

    # There's no specified way we should crawl - but we originally implemented `pop` on a set which is non-deterministic
    async def test_should_crawl_breadth_first(self):
        with aioresponses() as m:
            m.get(
                "https://example.com",
                body="<html><body>"
                '<a href="https://example.com/about">About</a>'
                '<a href="https://example.com/browse">About</a>'
                "</body></html>",
            )
            m.get(
                "https://example.com/about",
                body='<html><body><a href="https://example.com/contact">Contact</a></body></html>',
            )
            m.get(
                "https://example.com/browse",
                body="<html><body></body></html>",
            )
            m.get(
                "https://example.com/contact",
                body="<html><body></body></html>",
            )

            crawler = SyncCrawler("https://example.com", crawl_budget=3)
            actual = await crawler.crawl()

            self.assertEqual(
                {
                    "https://example.com": {
                        "urls": {
                            "https://example.com/about",
                            "https://example.com/browse",
                        }
                    },
                    "https://example.com/about": {
                        "urls": {"https://example.com/contact"}
                    },
                    "https://example.com/browse": {"urls": set()},
                },
                actual,
            )
