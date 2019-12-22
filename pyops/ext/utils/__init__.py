import json
import time
import datetime
import logging
import requests
import traceback
from .Login import LeadLogin
from .DataLib import DataManager

logger = logging.getLogger()


def get_config(req, k):
    config = req.config
    return config.get_class_config(config, k)


def set_config(req, k, v):
    config = req.config
    return config.set_class_config(config, k, v)


def del_config(req, k):
    config = req.config
    return config.del_class_config(config, k)


def get_user_token():
    try:
        ll = LeadLogin()
        return ll.get_uid()
    except Exception as e:
        logger.error(e)
        traceback.print_exc()


def post_common(data):
    logger.info(f'request data "{data}"')
    try:
        if data['method'] == 'GET':
            rep = requests.get(data['url'], data=data['body'], headers=data['headers'])
        elif data['method'] == 'POST':
            content_type = [v for k, v in data['headers'].items() if k.lower() == 'content_type']
            if content_type and 'json' in content_type[0]:
                rep = requests.post(data['url'], json=data['body'], headers=data['headers'])
            else:
                rep = requests.post(data['url'], data=data['body'], headers=data['headers'])
        else:
            logger.info(f'NOT support method "{data["method"]}"')
            raise ValueError(f'NOT support method "{data["method"]}"')

        if rep.status_code != 200:
            logger.error(f'FAIL with http code "{rep.status_code}"')
            logger.error(f'http body "{rep.text}"')
            return None
    except Exception as e:
        logger.error(f'FAIL with Exception "{e}"')
        traceback.print_exc()
        return None

    return rep


def db_query_common(data):
    logger.debug(f'query db data: {json.dumps(data)}')
    conn = DataManager.get_connection(data['db_host'], data['db_port'],data['db_user'],
                       data['db_passwd'], data['db_name'],  data['charset'], logger)

    return conn.query(data['sql'], data['param'], data['key'])


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def today():
    return f'{datetime.date.today()} 00:00:00'


def yesterday():
    today = datetime.date.today()
    yest = today - datetime.timedelta(days=1)

    return f'{yest} 00:00:00'


def tomorrow():
    today = datetime.date.today()
    tomo = today + datetime.timedelta(days=1)

    return f'{tomo} 00:00:00'


if __name__ == '__main__':
    data = {
        'url': 'http://dealerterminal.autohome.com.cn//clues-handler/api/pushclues',
        'method': 'POST',
        'headers': {
            'Content_Type': 'application/json',
            'Cookie': 'shiro2sesssion=03e97d00-f3fa-436e-bfa9-eed979108363'
        },
        'body':
        {
            "pushAppKey": "eb3a9c9ebd7ba7398d76ee345c801307",
            "keyInsideLinkidId": "7890123456789012345678901234567890",
            "keyOutsidePvareaidId": "4567890123456789012345678901234567890123456789022",
            "keyIsSubstitution": 0,
            "keyPrivateFlag": 0,
            "keyTypeId": 2,
            "splitCode": 1,
            "keyName": "clues_auto_testing",
            "keyPhone": "18681662603",
            "keySupplyBusinessId": 26,
            "keyDistributorId": "129193,127130,127120",
            "keyCarImgUrl": "",
            "keyOrderCityId": 110100,
            "keyReleaseId": "",
            "keyOrderTime": "2019-12-12 16:47:33",
            "keyPurposeBrandId": 33,
            "keyPurposeFactoryId": 79,
            "keyCarAudiId": 146,
            "keyCarTypeId": 467,
            "keyCardCityId": 110100,
            "keyFirstCardTime": "2016-05-08 09:12:00",
            "keyCarSourceType": 35848,
            "keyCarMileage": 1000,
            "keyPurposePrice": 10000,
            "keyPurposeBuyingTime": 1,
            "keyUserid": 2000,
            "keyIsLoan": 0,
            "keyClientOrderIp": "10.167.175.8",
            "keyUsedCarSourceCityId": 110100,
            "keyUsedCarSourceId": 110100,
            "keyUsedCarBusinessId": "",
            "keyAutoTesting": True
        }
    }
    rep = post_common(data)
    print(rep.text)
