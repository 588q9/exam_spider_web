import interval_access_free
import kuke_spider
import db_connect
import setting_read
if __name__=='__main__':

    setting=setting_read.setting()
    db=db_connect.db_mysql(setting=setting)

    market_free_spider=interval_access_free.access_market(

        spider_main_execute=kuke_spider.spider(db_operation=db,cookie=setting.cookie)

        ,db_operation=db,
       cookie=setting.cookie
    )

    market_free_spider.exam_market_spider()
