from typing import TypedDict, Set, Dict

PageResult = TypedDict("PageResult", {"urls": Set[str]})
CrawlResult = Dict[str, PageResult]
