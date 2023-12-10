from collections import deque
from typing import Optional

from walkcrawlrun.crawl_page import crawl_page
from walkcrawlrun.crawlers.crawl_result import CrawlResult
from walkcrawlrun.logger import logger


class SyncCrawler:
    def __init__(
        self,
        base_url: str,
        crawl_budget: Optional[int] = None,
        crawl_page_function=crawl_page,
    ):
        self.crawl_result: CrawlResult = {}
        self.base_url = base_url
        self.crawl_budget_remaining = crawl_budget
        self.to_visit = deque([base_url])
        self.crawl_page_function = crawl_page_function
        self.logger = logger.bind(name="RecursiveCrawler", base_url=base_url)

    async def crawl(self):
        while self.to_visit and self.has_crawl_budget():
            page = self.to_visit.popleft()
            if page not in self.crawl_result:
                self.logger.debug(
                    "about to crawl page",
                    page=page,
                    crawl_budget_remaining=self.crawl_budget_remaining,
                )
                result = await self.crawl_page_function(page)
                self.handle_result(result)

                if self.crawl_budget_remaining is not None:
                    self.crawl_budget_remaining -= 1
            else:
                self.logger.debug("already visited", page=page)

        self.logger.info(
            "finished crawling",
            crawl_budget_remaining=self.crawl_budget_remaining,
            num_urls_to_visit=len(self.to_visit),
        )

        return self.crawl_result

    def has_crawl_budget(self):
        return self.crawl_budget_remaining is None or self.crawl_budget_remaining > 0

    def handle_result(self, result: CrawlResult):
        for page, links in result.items():
            self.crawl_result[page] = links
            already_visited = self.crawl_result.keys()
            not_already_visited = links["urls"].difference(already_visited)
            self.to_visit.extend(not_already_visited)
