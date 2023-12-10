import unittest

from aioresponses import aioresponses

from walkcrawlrun.crawl_page import crawl_page


class TestSinglePageCrawl(unittest.IsolatedAsyncioTestCase):
    async def test_should_return_page_with_links(self):
        with aioresponses() as m:
            m.get(
                "https://example.com",
                body='<html><body><a href="https://example.com/about">About</a></body></html>',
            )
            m.get(
                "https://example.com/about",
                body='<html><body><a href="https://example.com">Home</a></body></html>',
            )

            actual = await crawl_page("https://example.com")

            expected = {"https://example.com": {"urls": {"https://example.com/about"}}}

            self.assertEqual(
                expected,
                actual,
            )

    async def test_should_ignore_links_on_different_subdomain(self):
        with aioresponses() as m:
            m.get(
                "https://example.com",
                body='<html><body><a href="https://ww2.example.com/about">About</a></body></html>',
            )

            actual = await crawl_page("https://example.com")

            self.assertEqual(
                {"https://example.com": {"urls": set()}},
                actual,
            )

    async def test_should_ignore_links_on_different_domain(self):
        with aioresponses() as m:
            m.get(
                "https://example.com",
                body='<html><body><a href="https://example.org/about">About</a></body></html>',
            )

            actual = await crawl_page("https://example.com")

            self.assertEqual(
                {"https://example.com": {"urls": set()}},
                actual,
            )

    async def test_should_ignore_fragments(self):
        with aioresponses() as m:
            m.get(
                "https://example.com",
                body='<html><body><a href="#home">Home</a></body></html>',
            )

            actual = await crawl_page("https://example.com")
            expected = {"https://example.com": {"urls": set()}}

            self.assertEqual(
                expected,
                actual,
            )

    async def test_should_make_relative_urls_absolute(self):
        with aioresponses() as m:
            m.get(
                "https://example.com",
                body='<html><body><a href="/about">About</a></body></html>',
            )

            actual = await crawl_page("https://example.com")

            self.assertEqual(
                {
                    "https://example.com": {"urls": {"https://example.com/about"}},
                },
                actual,
            )

    async def test_should_ignore_anchors_without_hrefs(self):
        with aioresponses() as m:
            m.get(
                "https://example.com",
                body='<html><body><a name="home">Home</a></body></html>',
            )

            actual = await crawl_page("https://example.com")

            self.assertEqual(
                {"https://example.com": {"urls": set()}},
                actual,
            )


if __name__ == "__main__":
    unittest.main()
