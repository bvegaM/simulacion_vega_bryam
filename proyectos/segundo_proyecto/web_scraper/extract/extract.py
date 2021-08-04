import argparse
import csv
import coloredlogs
import datetime
import logging
logging.basicConfig(level=logging.INFO)
import page_object as pg
import pandas as pd

from common import config

logger = logging.getLogger(__name__)
coloredlogs.install()

def new_scrapper(site_uid):
    host = config()['sites'][site_uid]['url']
    logger.info('Start scrapper from site: {}'.format(host))

    new_site = pg.NewSite(site_uid,host)
    new_site.visit_search()
    
    logger.info('get links of articles from site: {}'.format(host))
    links = new_site.get_links()
    
    logger.info('find: {} articles'.format(len(links)))
    articles=[]
    urls=[]
    for article in links:
        logger.info('Start fetching article at {}'.format(article))
        article_url = pg.ArticlePage(site_uid,article)
        abstract    = article_url.get_abstract
        if abstract:
            articles.append(abstract)
            urls.append(article)
    
    save_articles(articles,urls,site_uid)

def save_articles(articles,links,site_uid):
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name = '{news_site_uid}_{datetime}_articles.csv'.format(news_site_uid=site_uid,datetime=now)
    logger.info('Save data in ../data/{}'.format(out_file_name))
    
    df = pd.DataFrame(links,articles).reset_index()
    df.columns = ['abstract','url']
    df.to_csv('../data/{}'.format(out_file_name),index=False)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    new_sites_choices = list(config()['sites'].keys())
    parser.add_argument('sites',
                        help='The sites that you want to scrape',
                        type=str,
                        choices=new_sites_choices)
    
    args = parser.parse_args()
    new_scrapper(args.sites)
