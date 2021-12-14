import time
import requests
from lxml import etree
order_url='https://www.kuke99.com/order/checkout?goods_id={}&goods_type=1'
oder_gen_url = 'https://www.kuke99.com/order/generate'
exam_market_url='https://www.kuke99.com/free/p0_1_p4_1'
import traceback

today_exam_id= set()
header = {

    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
    'Accept': ' application / json, text / plain, * / *',

}

buy_data = {
        'goods_num':
            "1",
        'coupon_id':
            "0",
        'goods_id':
            "",
        'goods_type':
            "1",
        'group_buy_goods_rule_id'
        : "",
        'group_token': "", 'seckill_goods_id': "",
        "dist_id": ''}

class access_market:
    def __init__(self,spider_main_execute,db_operation,cookie):
        self.spider_main_execute =spider_main_execute

        self.cookie=cookie
        self.db_operation = db_operation


    def exam_list_url_construct(self,page):
        return  exam_market_url+'?page='+ str(page)
    def id_to_set(self,tul):
        id_set=set()
        for item in tul:
            id=item[0]
            id_set.add(id)
        return id_set

    def max_page(self):
        resp_market = requests.get(exam_market_url, headers=header,
                                   cookies=self.cookie
                                   )
        # print(resp_market.text)
        market_html = etree.HTML(resp_market.text)

        pagination = market_html.xpath('/html/body/section/div[2]/div[3]/ul')[0]
        max_page_list = pagination.xpath('./li')
        max_page_num = len(max_page_list)

        return max_page_list[max_page_num - 2].xpath('./a/text()')[0]
    def buy_exam(self,id):
        buy_data['goods_id']=str(id)
        resp=requests.post(url=oder_gen_url, data=buy_data, cookies=self.cookie)
        # print(resp.text)


    def exam_market_spider(self):
        page_amount=self.max_page()

        #int(page_amount)+1
        for i in range(1,int(page_amount)+1):
            # print(i)
            resp_market = requests.get(self.exam_list_url_construct(i), cookies=self.cookie, headers=header
                                       )
            tree_market=etree.HTML(resp_market.text)

            a_href=tree_market.xpath('/html/body/section/div[2]/div[2]/a[@class="content-item"]/@href')

            # print(a_href)
            for href in a_href:
                item_num=str(href).split('.')[-2].split('/')[-1]
                today_exam_id.add(int(item_num))
        # print(today_exam_id)
        db_id_collection=self.db_operation.select_exam_id_collection()
        db_id_collection=self.id_to_set(db_id_collection)
        unique=today_exam_id.difference(db_id_collection)
        print('没进数据库试卷的id:',unique)
        for item in unique:
            self.buy_exam(item)
            print('买试卷完成:',item)
            time.sleep(1)
            self.spider_main_execute.data_exam_id=str(item)
            print('开始爬取')
            try:
                self.spider_main_execute.spider_exam()
            except Exception as  e:

                print('出现异常！！!',e)
                traceback.print_exc()

                self.db_operation.rollback()






        # for id in today_exam_id:
        #     is_find=db_operation.select_exam_id_count(id)
        #     print(is_find)
        #     if is_find==0:
        #         buy_exam(id)



        buy_data['goods_id'] = ''
        today_exam_id.clear()
        self.db_operation.close_db()












