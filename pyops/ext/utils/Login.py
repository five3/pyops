import re
import requests


LOGIN_URL = "http://10.168.0.187:8080/login?service=http://dealerterminal.autohome.com.cn/clues-terminal/cas"
IDENTIFY_URL = "http://dealerterminal.autohome.com.cn/clues-terminal/user-center/getCurrentUser"
USER = 'xxxt6'
PASSWD = r"?Mcecs@'CGqB*"


class LeadLogin:
    def __init__(self, user=USER, passwd=PASSWD):
        self.user = user
        self.passwd = passwd
        self.uid = ''

    def get_uid(self):
        if self.uid and self._identify_uid(self.uid):
            return self.uid
        else:
            return self._request_uid(LOGIN_URL)

    def _request_uid(self, login_url=LOGIN_URL):
        session = requests.session()
        html = session.get(login_url)
        pattern = re.compile('name="lt" value="(.*?)".*?name="execution" value="(.*?)"', re.S)
        items = re.findall(pattern, html.text)
        lt, execution = items[0]

        post_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': login_url,
            'Connection': 'keep-alive',
        }
        post_data = {
            'username': USER,
            'password': PASSWD,
            'lt': lt,
            'execution': execution,
            'systemname': 'Autohome',
            '_eventId': 'submit'
        }

        session.post(LOGIN_URL, data=post_data, headers=post_headers)
        self.uid = session.cookies.get('shiro2sesssion')
        self._identify_uid(self.uid)
        return self.uid

    def _identify_uid(self, uid, identify_url=IDENTIFY_URL):
        session = requests.session()
        headers = {
            "Cookie": "shiro2sesssion=%s" %(uid)
        }
        resp = session.get(identify_url, headers=headers)
        if resp.status_code != 200:
            raise Exception("Failed to get url when identify UID: %s" % (identify_url))

        # print(resp.text)
        return True if resp.json()['status'] in (0, 1) else False


if __name__ == "__main__":
    login = LeadLogin()
    uid = login.get_uid()
    print(uid)
