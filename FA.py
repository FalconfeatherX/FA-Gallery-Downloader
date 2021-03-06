# -*- coding: utf-8 -*-
from Scraper import Scraper
from DATABASE import Database
from Download import Download
import argparse
import time
import Constant
if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog = 'Furaffinity Gallery Downloader',
                                    description = Constant.TEXT)
    parser.add_argument('-s','--scrape',action = 'store_true',help = 'Scrape only')
    parser.add_argument('-d','--download',action = 'store_true',help = 'Download from database')
    parser.add_argument('-m','--mix',action = 'store_true',help = 'Scrape and download，not recommended')
    parser.add_argument('-c','--check',action = 'store_true',help = 'Check how many pages')
    parser.add_argument('-u','--update',action = 'store_true',help = 'Update Gallery')
    args = parser.parse_args()

    spider = Scraper()
    db     = Database()
    Down   = Download()
    db.databaseCreate()

    if args.check:
        spider.page_check()

    if args.scrape:
        spider.page_check()
        for singleurl in spider.page_list:
            spider.get_post_url(singleurl)
            datum = spider.multi_crawler()
            db.databaseinsert(datum)
            if error:
                redatum,error = spider.multi_crawler(error)
                db.databaseinsert(redatum)
                print('reconnect ' + singleurl + ' done.')
            time.sleep(1)
            print(singleurl + ' done.')

    if args.download:
        print('Downloading start.')
        output = db.databaseoutput(spider.tag)
        datum = Down.multi_download(output)
        db.databasedownloaded(datum)
        print('Download finished')

    if args.mix:
        spider.page_check()
        for singleurl in spider.page_list:
            spider.get_post_url(singleurl)
            datum,error = spider.multi_crawler()
            db.databaseinsert(datum)
            if error:
                spider.multi_crawler(error)
                redatum,error = spider.multi_crawler(error)
                db.databaseinsert(redatum)
                
            print(singleurl + ' done.')
            print(singleurl + ' start downloading.')
            output = db.databaseoutput(spider.tag)
            datum = Down.multi_download(output)#not recommended
            db.databasedownloaded(datum)
            print(singleurl + ' downloading finished')
        print('Downloading all finished')

    if args.update:
        spider.page_check()
        for singleurl in spider.page_list:
            spider.get_post_url(singleurl)
            datum,error = spider.multi_crawler()
            ifupdate = db.databaseupdate(spider.tag,datum)
            if ifupdate >=0 and ifupdate <72:
                break        
