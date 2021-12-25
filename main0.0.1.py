import math
import requests
import random
from bs4 import BeautifulSoup as BS
# import schedule         # 定时
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os
import logging          # 日志
from public.color import *
# import threading


# 初始化日志
logs = os.path.exists('logs')
if not logs:
    os.mkdir('logs')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    filename='logs/log.txt',
                    filemode="a")


# 定义类
class HealthPunch(object):

    def __init__(self):
        self.msg_from = ''     # 替换成你发邮件的邮箱，可以QQ直接申请
        self.passwd = ''       # 替换成 这个密码是在邮箱里申请的
        self.msg_to = ''     # 替换成接收打卡完成提醒
        self.url1 = 'http://et.ynau.edu.cn/yjsmis2/Query/StudentPost.asp'
        self.url2 = 'http://et.ynau.edu.cn/yjsmis2/Query/Student.asp'
        #   'ASP.NET_SessionId=5ql12ndj0klflqb1rdojg; ASPSESSIONIDCSTASBQD=FNHHBCGKFGECGILDNABCI'
        self.cookie = ''  # 这个值需要通过抓包获取，一定要点进填报健康去，不然有微信验证绕不过去，cookie无效
        self.headers = {
            'Host': 'et.ynau.edu.cn',
            'Origin': 'http://et.ynau.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi K20 Pro Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2899 MMWEBSDK/20210601 Mobile Safari/537.36 MMWEBID/1381 MicroMessenger/8.0.11.1980(0x28000B59) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
            'Referer': 'http://et.ynau.edu.cn/yjsmis2/Query/StudentPost.asp',
            'Cookie': self.cookie
        }
        self.headers1 = {
            'Host': 'et.ynau.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi K20 Pro Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2899 MMWEBSDK/20210601 Mobile Safari/537.36 MMWEBID/1381 MicroMessenger/8.0.11.1980(0x28000B59) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
            'Referer': 'http://et.ynau.edu.cn/yjsmis2/Query/StudentPost.asp',
            'Cookie': self.cookie
        }
        self.headers2 = {
            'Host': 'et.ynau.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi K20 Pro Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2899 MMWEBSDK/20210601 Mobile Safari/537.36 MMWEBID/1381 MicroMessenger/8.0.11.1980(0x28000B59) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
            'Referer': 'http://et.ynau.edu.cn/yjsmis2/Query/student.asp',
            'Cookie': self.cookie
        }
        self.session = requests.Session()

    # 发送修改数据
    def send_data(self):
        tem = round(random.uniform(36.2, 36.7), 1)
        logging.info('获得随机时间:' + str(tem))
        data = {
            'go': 1,
            't1': 0,
            't2': tem,
            't4': 1,
            'bz': '',
            'addr': '%E4%BA%91%E5%8D%97%E7%9C%81%E6%98%86%E6%98%8E%E5%B8%82%E7%9B%98%E9%BE%99%E5%8C%BA7204%E5%85%AC%E8%B7%AF',
            'nation': '%E4%B8%AD%E5%9B%BD',
            'city': '%E6%98%86%E6%98%8E%E5%B8%82',
            'province': '%E4%BA%91%E5%8D%97%E7%9C%81',
            'district': '%E7%9B%98%E9%BE%99%E5%8C%BA',
            'street': '7204%E5%85%AC%E8%B7%AF',
            'lat': 25.129738,
            'lon': 102.746315
        }
        self.session.post(url=self.url1, data=data, headers=self.headers)
        logging.info('发送填报健康数据成功')
        return tem

    # 发送邮件
    def send_email(self, subject, text):
        global s
        msg = MIMEMultipart()
        text = MIMEText(text)
        msg.attach(text)
        msg['Subject'] = subject
        msg['From'] = self.msg_from
        msg['To'] = self.msg_to
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465, 'utf-8')
            s.login(self.msg_from, self.passwd)
            s.sendmail(self.msg_from, self.msg_to, msg.as_string())
            logging.info('邮件发送成功')
            print(green("发送成功"))
        except smtplib.SMTPException as e:
            print(red("发送失败"))
            logging.warning('邮件发送失败！' + str(e))
        finally:
            s.quit()

    # 获取数据
    def get_data(self):
        get_date_list = []
        res = self.session.get(url=self.url2, headers=self.headers1)
        print(res.status_code)
        res.encoding = 'utf-8'
        if str(res) != '<Response [200]>':
            print(red('获取健康数据失败！'))
            logging.warning('获取健康数据失败！' + str(res.status_code))
            return get_date_list
        else:
            print('获取健康数据get请求成功')

        soup = BS(res.text, 'lxml')
        for i in range(len(soup.select('.media-body'))):
            list = []
            date = str(soup.select('.media-body')[i]).split('\n')[1][54:64]
            data_time = str(soup.select('.media-body')[i]).split('\n')[1][65:73]
            state = str(soup.select('.media-body')[i]).split('\n')[2][37:39]
            list.append(date)
            list.append(data_time)
            list.append(state)
            get_date_list.append(list)
        print(yellow(str(get_date_list)))
        return get_date_list

    # 刷新数据
    def fresh_cookie(self):
        res = self.session.get(url=self.url1, headers=self.headers2)
        res.encoding = 'utf-8'
        if str(res) == '<Response [200]>':
            return True
        else:
            return False


def main():
    title_list = ['主人今日打卡成功！', '主人打卡任务已经完成啦！', '健康打卡小的已经报了！',
                  '打卡助手前来报到！', '主人健康打卡不必操劳了！',]
    app = HealthPunch()
    while True:
        now_time_h = int(time.strftime('%H'))
        if now_time_h >= 8:
            # 2021-12-04 08:47:29 健康
            now_date = time.strftime('%Y-%m-%d')  # 获取当前年月日
            request_data = app.get_data()
            if len(request_data) != 0:
                if now_date != request_data[0][0]:  # 当获取到的数据没有今天的时
                    tem = app.send_data()  # 发送数据填报体温,返回所填报体温，以便发送邮件
                    # 死循环再获取一次最新数据
                    while True:
                        data = app.get_data()
                        if len(data) != 0:
                            break
                        time.sleep(5)
                    text = ''
                    for i in data:
                        text += '\n\n'.join(i) + '\n\n'
                    send_text = '自动填报体温为:' + str(tem) + '\n\n\n' + text
                    app.send_email(random.choice(title_list), send_text)
                else:
                    time.sleep(900)
                    print(blue('维持cookie中.....'))
            else:
                i = 0
                while i < 10:
                    time.sleep(5)
                    print('正在尝试get填报健康页面刷新！')
                    boo = app.fresh_cookie()
                    time.sleep(5)
                    print('正在尝试get将康数据页面刷新！')
                    boo1 = app.get_data()
                    if boo == True or len(boo1) == 0:
                        i += 1
                        if i == 10:
                            print('刷新失败！，程序即将退出！')
                            app.send_email('程序cookie刷新失败！', '两个请求均尝试10次后，cookie刷新失败！')
                            return
                        continue
                    break
        else:
            i = 0
            while i < 10:
                time.sleep(5)
                print('正在尝试get填报健康页面刷新！')
                boo = app.fresh_cookie()
                time.sleep(5)
                print('正在尝试get将康数据页面刷新！')
                boo1 = app.get_data()
                if boo == True or len(boo1) != 0:
                    break
                i += 1
                if i == 10:
                    print('刷新失败！，程序即将退出！')
                    app.send_email('程序cookie刷新失败！', '两个请求均尝试10次后，cookie刷新失败！')
                    return
            time.sleep(900)


if __name__ == '__main__':
    start_time = time.time()
    logging.info('程序开始运行')
    main()
    seconds_used = int(time.time() - start_time)
    logging.info('程序运行总时间为:' + str(math.floor(seconds_used / 60)) +
                 " 分 " + str(seconds_used % 60) + " 秒")


