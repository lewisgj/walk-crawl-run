import argparse
import asyncio
import sys

from walkcrawlrun.crawlers.sync import SyncCrawler
from walkcrawlrun.crawlers.concurrent import ConcurrentCrawler


async def main():
    parser = argparse.ArgumentParser(
        description="Crawl a URL to find other links on that website."
    )
    parser.add_argument(
        "--start-url", type=str, required=True, help="the URL to start crawling from"
    )
    parser.add_argument(
        "--crawl-budget",
        type=int,
        required=False,
        default=10,
        help="the number of pages to crawl",
    )
    parser.add_argument(
        "--strategy",
        type=str,
        choices=["sync", "concurrent"],
        required=False,
        default="sync",
        help="the approach to crawling - do we crawl one page at a time (sync) or concurrently?",
    )

    args = parser.parse_args(sys.argv[1:])
    if args.strategy == "sync":
        crawler = SyncCrawler(args.start_url, crawl_budget=args.crawl_budget)
    else:
        crawler = ConcurrentCrawler(args.start_url, crawl_budget=args.crawl_budget)

    results = await crawler.crawl()
    pretty_print(results)


def pretty_print(crawl):
    for page, links in crawl.items():
        print(page)
        for link in links["urls"]:
            print(f"-- {link}")
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
