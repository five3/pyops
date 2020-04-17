import time
import datetime
import logging
import requests
import traceback

logger = logging.getLogger()


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


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def today():
    return f'{datetime.date.today()} 00:00:00'


def yesterday():
    _today = datetime.date.today()
    yest = _today - datetime.timedelta(days=1)

    return f'{yest} 00:00:00'


def tomorrow():
    _today = datetime.date.today()
    tomo = _today + datetime.timedelta(days=1)

    return f'{tomo} 00:00:00'


if __name__ == '__main__':
    pass
