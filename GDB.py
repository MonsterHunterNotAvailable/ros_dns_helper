# -*- coding: utf-8 -*-

import pymysql

class GDB:

    def __init__(self, database):
        self.database = database
        if len(self.database) == 0:
            self.database = ""

        self.conn = None
        self.cursor = None
        pass

    def connectDB(self,host, user, password, port ):
        print("CONNECT DB:", host, user,password,port)
        self.conn = pymysql.connect(host=host, port=int(port), user=user,
                          password=password, database=self.database, charset='utf8mb4', autocommit=True,
                          local_infile=True)

        self.cursor = self.conn.cursor()


    #单个
    def query(self, sql):
        try:
            ret = self.queryList(sql)
            if ret:
                return ret[0]
        except Exception as e:
            print("query err", e)

        return None

    #多个
    def queryList(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()

            list = []

            for tmpOne in result:
                idx = 0
                one = {}

                tmpLen = len(tmpOne)

                for column in tmpOne:
                    keyName = self.cursor.description[idx][0]
                    one[keyName] = column
                    idx += 1


                list.append(one)
            # print(list)

            return list
        except Exception as e:
            print("query err", e)

        return None



    #多个
    def queryMapForUid(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()

            map = {}

            for tmpOne in result:
                idx = 0
                one = {}

                # tmpLen = len(tmpOne)

                for column in tmpOne:
                    keyName = self.cursor.description[idx][0]
                    one[keyName] = column
                    idx += 1


                # list.append(one)
                map[one["uid"]] = one
            # print(list)

            return map
        except Exception as e:
            print("query err", e)

        return None

    #批量插入
    def multiInsert(self,sql,valList):
        if len(valList) == 0:
            return -1
        ret = self.cursor.executemany(sql,valList)
        return ret

    #execute
    def execute(self, sql, tryCache=False):
        # print("[DB EXECUTE CMD] %s" % (sql))


        ret = 0
        if tryCache == False:
            ret = self.cursor.execute(sql)
        else:
            try:
                ret = self.cursor.execute(sql)
            except Exception as ee:
                print("execute err", ee)

        return ret

    #explain
    def explain(self, sql):
        ret = self.cursor.execute("explain %s " % (sql))
        return ret

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print("close err", e)

