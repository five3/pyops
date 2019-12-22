import logging
import requests

logger = logging.getLogger()


class DataConnection(object):
    """
    表示一个数据连接；通过该连接获取远程的DB数据
    """
    def __init__(self, id, db_host, db_port, db_user, db_passwd, db_name, db_charset, logger):
        self.id = id
        self.db_host = str(db_host)
        self.db_port = int(db_port) or 80
        self.db_user = str(db_user)
        self.db_passwd = str(db_passwd)
        self.db_name = str(db_name)
        self.db_charset = str(db_charset)
        self.conn = None
        self.logger = logger
        self.url = 'http://atmp.corpautohome.com/datasource/query'

        if self.logger is None:
            raise Exception("DataConnection[id:%d]的logger为空" % id)

    def __inner_execute__(self, sql, param, key='all'):
        param = {} if param is None else param
        self.logger.debug("sql: %s, param: %s" % (sql, param))
        reps = requests.post(self.url, json={
            "db_host": self.db_host,
            "db_port": self.db_port,
            "db_name": self.db_name,
            "db_user": self.db_user,
            "db_passwd": self.db_passwd,
            "charset": self.db_charset,
            "sql": sql,
            "param": param,
            "key": key
        })
        self.logger.debug(f'DataSource Response: {reps.text}')
        rep = reps.json() if reps.status_code == 200 else {}
        self.logger.info('Request DataSource %s ' % (rep.get('success') and "success" or "failed with code: %s" % reps.status_code))

        if rep:
            self.last_rowcount = len(rep['data'])
            if rep['type'] == 'INSERT':
                self.insert_id = rep['insert_id']
            return rep['data']
        else:
            self.last_rowcount = 0
            self.insert_id = None
            return rep

    def execute(self, sql, param=None):
        """执行一条sql语句"""
        self.__inner_execute__(sql, param)

    def query(self, sql, param=None, key='first'):
        """用于执行查询；返回查询后的多行结果，每一行是key-value格式，key为列名"""
        return self.__inner_execute__(sql, param, key)

    def query_one(self, sql, param=None):
        """用于查询出一行记录，每一行是key-value格式，key为列名"""
        return self.__inner_execute__(sql, param, key='first')
    
    def is_exist(self, table_name, key_name, key_value):
        """
        判断指定字段值是否存在
        """
        sql = f"select count(*) as n from {table_name} where {key_name}='{key_value}'"
        data = self.__inner_execute__(sql, {}, key='first')

        return True if data else False

    def get_insert_id(self):
        return self.insert_id

    def get_last_rowcount(self):
        return self.last_rowcount


class DataManager(object):
    conn_id = 0
    conns = {}

    def __init__(self):
        raise NotImplementedError("Class DataManager can not be init")

    @classmethod
    def get_connection(cls, host, port, user, passwd, db, charset, logger):
        """获取mysql连接"""
        key = f'{host}.{port}.{db}'
        if key not in cls.conns:
            logger.info(f"new mysql connect with key [{key}]")
            cls.conn_id += 1
            cls.conns[key] = DataConnection(cls.conn_id, host, port, user,
                               passwd, db, charset, logger)

        return cls.conns[key]


if __name__ == '__main__':
    data = {"db_host": "10.27.12.50", "db_port": 3306, "db_name": "auto_pmo_leadssys", "db_user": "autoax", "db_passwd": "autoax", "charset": "utf-8", "sql": "SELECT a.push_id, a.key_unique_id, b.task_id, d.task_name, d.priority, d.customized_dealer, b.deliver_status, c.clues_content, c.des_info\n        FROM clues_publicpush_succ a LEFT JOIN clues_distribute_detail b ON a.key_unique_id=b.key_unique_id\n        LEFT JOIN clues_unable_distribute c ON a.key_unique_id=c.clues_unique_id\n        LEFT JOIN ad_task d ON b.task_id=d.id\n        WHERE a.push_id=\"1069305811115720704\";", "param": {}, "key": "first"}

    conn = DataManager.get_connection(data['db_host'], data['db_port'], data['db_user'],
                                      data['db_passwd'], data['db_name'], data['charset'], logger)

    ret = conn.query(data['sql'], data['param'], data['key'])
    print(ret)
