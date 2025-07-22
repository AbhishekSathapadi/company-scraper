import logging
import azure.functions as func
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from company_scraper.company_scraper.spiders.company_spider import CompanySpider

def main(mytimer: func.TimerRequest) -> None:
    logging.info('Starting Scrapy spider...')
    process = CrawlerProcess(get_project_settings())
    process.crawl(CompanySpider)
    process.start()
    logging.info('Scrapy spider finished.')
