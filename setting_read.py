from lxml import etree

class setting:
    def __init__(self):
        setting = etree.parse('./setting.xml')

        self.access_token = str(setting.xpath('/setting/token/text()')[0]).strip()

        self.url=str(setting.xpath('/setting/db/url/text()')[0]).strip()
        self.db_user=str(setting.xpath('/setting/db/user/text()')[0]).strip()
        self.db_password=str(setting.xpath('/setting/db/password/text()')[0]).strip()

        self.acw_tc = str(setting.xpath('/setting/acw-tc/text()')[0]).strip()
        self.data_exam_id = str(setting.xpath('/setting/exam-id/text()')[0]).strip()

        self.cookie = {
            'access_token': self.access_token,
            'UM_distinctid': '17d73dda00b63a-0c1c1167014c88-b7a1a38-e1000-17d73dda00cd55'
            , 'acw_tc': self.acw_tc

        }