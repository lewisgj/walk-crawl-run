import asyncio
from typing import Optional, Dict, Awaitable

from walkcrawlrun.crawl_page import crawl_page
from walkcrawlrun.crawlers.crawl_result import CrawlResult
from walkcrawlrun.logger import logger


class ConcurrentCrawler:
    def __init__(
        self,
        base_url: str,
        crawl_budget: Optional[int] = None,
        crawl_page_function=crawl_page,
    ):
        self.crawl_tasks: Dict[str, Awaitable] = {}
        self.crawl_result: CrawlResult = {}
        self.base_url = base_url
        self.crawl_budget_remaining = crawl_budget
        self.crawl_page_function = crawl_page_function
        self.logger = logger.bind(name="RecursiveCrawler", base_url=base_url)

    async def crawl(self):
        async with asyncio.TaskGroup() as tg:
            await self.do_crawl(self.base_url, tg)

        self.logger.info(
            "finished crawling", crawl_budget_remaining=self.crawl_budget_remaining
        )

        return self.crawl_result

    def has_crawl_budget(self):
        return self.crawl_budget_remaining is None or self.crawl_budget_remaining > 0

    async def do_crawl(self, url, task_group):
        if self.has_crawl_budget():
            if self.crawl_budget_remaining is not None:
                self.crawl_budget_remaining -= 1

            result = await crawl_page(url)
            for page, links in result.items():
                self.crawl_result[page] = links
                already_visited = self.crawl_tasks.keys()
                not_already_visited = links["urls"].difference(already_visited)
                for url in not_already_visited:
                    self.crawl_tasks[url] = task_group.create_task(
                        self.do_crawl(url, task_group)
                    )
