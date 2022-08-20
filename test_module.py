import interval_access_free
import kuke_spider
import db_connect
import setting_read

if __name__=='__main__':
    db=db_connect.db_mysql()
    setting=setting_read.setting()
    spider_main_execute = kuke_spider.spider(db_operation=db, cookie=setting.cookie)
    spider_main_execute.data_exam_id=setting.data_exam_id
    spider_main_execute.spider_exam()
    # print(op.select_exam_id_count(641))
    # interval_access_free.buy_exam()