import random
import time
import requests
from lxml import etree
import json

do_test_url = 'https://www.kuke99.com/do_test'
domain = 'https://www.kuke99.com'


class spider():

    def __init__(self, db_operation, cookie):
        self.cookie = cookie
        self.db_operation = db_operation
        self.data_exam_id = ''
        self.cookie_exam = {

            'do_exam_source_url ': 'https%3A%2F%2Fwww.kuke99.com%2Fucenter%2Fexam_detail%2Fid%2F'

            , 'access_token': self.cookie['access_token'],
            'UM_distinctid': '17d73dda00b63a-0c1c1167014c88-b7a1a38-e1000-17d73dda00cd55'
        }

    exam_info = {
        'id': 9529,
        'result': 0,
        'exam_id': 1327
    }

    def spider_exam(self):
        exam_list_url = 'https://www.kuke99.com/ucenter/exam_detail/id/' + self.data_exam_id

        print()

        print(self.data_exam_id)

        header = {

            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
            'Accept': ' application / json, text / plain, * / *',

        }
        # exam_url='https://www.kuke99.com/testing?result=0&exam_id=1327&id=9557'

        #
        # cookie = {
        #     'access_token': self.access_token,
        #     'UM_distinctid': '17d73dda00b63a-0c1c1167014c88-b7a1a38-e1000-17d73dda00cd55'
        #     , 'acw_tc': self.acw_tc
        #
        # }

        resp_exam_list_page = requests.get(exam_list_url,
                                           headers=header, cookies=self.cookie)
        print(resp_exam_list_page.status_code)
        # print(resp_exam_list_page.text)
        list_tree = etree.HTML(resp_exam_list_page.text)
        ul = list_tree.xpath('/html/body/section/div[4]/div[1]/div[3]')
        title = list_tree.xpath('/html/head/title/text()')[0]
        # if len(title)==0:
        #     title=''
        # else:
        #     title=title[0]
        print('标题', title)

        self.db_operation.insert_exam_list(exam_list_url=exam_list_url
                                           , data_exam_id=int(self.data_exam_id)
                                           , exam_list_name=title
                                           )

        for node in ul[0].xpath('./div'):
            time_sleep = 5 * random.random() + 2
            time.sleep(time_sleep)
            print('睡眠时间:', time_sleep)
            data_id = node.xpath('./@data-id')[0]
            data_exam_id = node.xpath('./@data-exam-id')[0]
            print(node.xpath('./@data-exam_url'), data_id, data_exam_id)

            self.cookie_exam['do_exam_source_url '] = 'https%3A%2F%2Fwww.kuke99.com%2Fucenter%2Fexam_detail%2Fid%2F' + \
                                                      data_exam_id[0]

            exam_info_inter = {
                'id': data_id,
                'result': 0,
                'exam_id': data_exam_id
            }
            header_exam = {

                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
                'Accept': ' application / json, text / plain, * / *',
                'Content - Type': ' application / x - www - form - urlencoded'
            }

            resp = requests.post(do_test_url, headers=header_exam, cookies=self.cookie_exam,
                                 data=exam_info_inter
                                 )
            print(resp)
            # print(resp.text, resp.content)
            json_info = resp.json()

            # print(json_info['data']['main'])

            print(json_info['data']['main']['testpaper_name'], data_id)
            info = json_info['data']['info']
            question_type = dict(info).keys()
            print('题目类型:', question_type)
            self.db_operation.insert_testpaper(
                testpaper_name=json_info['data']['main']['testpaper_name'],
                data_exam_id=int(data_exam_id),
                data_id=int(data_id)
            )
            for name_type in question_type:
                # print(name_type)
                # print(info[name_type])
                for question in info[name_type]:
                    # print(name_type,'题目:')
                    # print('stem:',question['stem'])
                    # print('metas:',question['metas'])
                    # print('analysis',question['analysis'])
                    # print('answer',question['answer'])
                    temp_item = 'null'

                    if dict(question).__contains__('items'):
                        temp_item = question['items']
                        temp_item = json.dumps(temp_item, ensure_ascii=False)

                    self.db_operation.create_question(
                        analysis=question['analysis'],
                        question_type_name=name_type,
                        stem=question['stem'],
                        data_id=int(data_id),
                        metas=question['metas'],
                        answer=question['answer'], item=temp_item

                    )

            print('---------------------------这张试卷爬完了---------------------------------------\n\n')
        self.db_operation.commit()
        print('提交事务!')
