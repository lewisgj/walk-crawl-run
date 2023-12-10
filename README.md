# Walk Crawl Run Webcrawler

An example web crawler written using Python 3.12.

## Getting started

### Prerequisites

- Python 3.12
- poetry

### Running

1. Run `poetry install` to install the dependencies
1. Run `poetry run python -m walkcrawlrun --start-url https://en.wikipedia.org/wiki/Special:Random` to run the
   webcrawler

Once finished, the program will output the results to the console.
You will also notice debug logging in the console. See [Logging](#logging) for more information.

#### Arguments

* `--start-url`: the URL to start crawling from. Required.
* `--crawl-budget`: the number of pages to crawl before stopping. Defaults to 10.

#### Docker Alternative

If you don't have a recent version of python and poetry installed, you might prefer to build and run the docker image.

1. Run `docker build -t walkcrawlrun .` to build the image
1. Run `docker run walkcrawlrun --start-url https://en.wikipedia.org/wiki/Special:Random` to run the webcrawler

> We might run this somewhere else in "production". Putting it in a container makes it somewhat easy to run anywhere.

### Testing

The program is tested using `pytest` with some additional plugins:

* Pass `-n auto` to run tests across multiple processes, though on a small project like this it will likely take longer.
* Pass `--cov` to get a coverage report.

> In general, I tried to follow a TDD approach where it made sense. Code coverage overall is great - however, we don't
> necessarily have every behaviour well-specified.

### Local development

This project uses pre-commmit hooks. You can install them with `pre-commit install`. It runs some of the formatting and
linting checks locally, but won't run the tests.

### Linting, formatting

This project uses `ruff` for both linting and formatting. You can run `ruff --fix` to run the linter in fix mode ,
and `ruff format` to automatically format the code.

## Design choices and approach

On the whole, I've prioritised something that was easy to change over something that was fast. That includes plenty of
tests and a focus on the dev-experience.

I spent about 3-4 hours on this project to get to the 'sync' version of the crawler, plus a bit more time on this
README.

I've also included a 'concurrent' crawler but in the interest of transparency, this was after the initial 4 hours.

I've not written lots of Python lately, and I've used some new language features and tools, so it might not be the most
idiomatic code.

### Logical next steps

There's some things I de-prioritised but would be logical next steps:

* Error cases
    * Today, the program will crash if it encounters an error such as being able to fetch a page.
    * There's a number of things we might do here:
        * Retries - we might want to retry a few times before giving up
        * Timeouts - if the page takes too long to load, we might want to give up
        * Reporting on errors
* Following redirects better (or not following them)
    * Today, it follows redirects, but the final URL is not included in the results
* Concurrency: Before taking this further (or any performance work), I'd really want to have a benchmark to see / prove
  if it's actually faster.

### Logging

Today, the program will output logs to the console before printing the final output.
However, there's a distinction between the output of the program (`print` statements) and the logging.
In production, the logs would likely be sent to a log aggregator or similar to make them searchable - and likely only
errors would be reported.
Logging is done using `structlog` so we can easily switch to a different logging format if needed.
