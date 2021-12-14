import pymysql


class db_mysql:

    def __init__(self,setting):
        self.__conn = pymysql.connect(
            host=setting.url,
            port=3306,
            user=setting.db_user,
            passwd=setting.db_password,
            db='kuke_info',
            charset='utf8'
        )
        self.__cursor = self.__conn.cursor()

    def insert_exam_list(self, data_exam_id, exam_list_url, exam_list_name):
        # 插入数据
        sql = "INSERT INTO exam_list (data_exam_id, exam_list_url, exam_list_name) VALUES ( '%d', '%s', '%s' )"
        data = (data_exam_id, exam_list_url, exam_list_name)
        self.__cursor.execute(sql % data)
        # self.__conn.commit()

        # print('成功插入exam_list', cursor.rowcount, '条数据')

    def create_question(self, question_type_name,
                        data_id, stem, metas, analysis,
                        answer,item):
        # 插入数据
        # print('转义前  :',stem)

        stem = pymysql.converters.escape_string(str(stem))
        analysis = pymysql.converters.escape_string(str(analysis))
        answer = pymysql.converters.escape_string(str(answer))
        metas = pymysql.converters.escape_string(str(metas))

        if item=='null':
            sql = "INSERT INTO question (question_type_name,data_id,stem,metas,analysis,answer,item) VALUES ( '%s','%d', '%s', '%s' ,'%s','%s',%s)"
        else:
            sql = "INSERT INTO question (question_type_name,data_id,stem,metas,analysis,answer,item) VALUES ( '%s','%d', '%s', '%s' ,'%s','%s','%s')"
            item = pymysql.converters.escape_string(str(item))

        # print(item)
        # print('转义后',stem)
        # print(item)
        data = (question_type_name, data_id, stem, metas, analysis, answer,item)
        sql=sql % data



        self.__cursor.execute(sql)

        # self.__conn.commit()
        # print('成功插入question', cursor.rowcount, '条数据')

    def insert_testpaper(self, testpaper_name, data_id, data_exam_id):
        # 插入数据
        sql = "INSERT INTO testpaper (testpaper_name,data_id,data_exam_id) VALUES ('%s','%d','%d')"
        data = (testpaper_name, data_id, data_exam_id)
        self.__cursor.execute(sql % data)
        # self.__conn.commit()
        # print('成功插入question', cursor.rowcount, '条数据')
    def select_exam_id_count(self,id):
        sql="select count(data_exam_id) from exam_list where data_exam_id='%d'"%(id,)
        rs=self.__cursor.execute(sql)
        return self.__cursor.fetchall()[0][0]
    def select_exam_id_collection(self):
        sql="select data_exam_id from exam_list "
        rs=self.__cursor.execute(sql)
        return self.__cursor.fetchall()

    def commit(self):
        self.__conn.commit()
    def rollback(self):
        self.__conn.rollback()
    def close_db(self):
        self.__cursor.close()
        self.__conn.close()
