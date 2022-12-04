import pickle
import logging
import email
import email.utils
import time
import datetime
import pytz
import os
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.blocking import BlockingScheduler

from conf.settings import BASE_DIR,PROJECT_DIR,FILES_DIR
from libs.line import lineNotify

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


logger = logging.getLogger(__name__)

scheduler = BlockingScheduler()

class Email:
    savePath = os.path.join(FILES_DIR, 'bkrecord.pkl')
    debug = False

    def __init__(self):
        self.msgs = []
        self.filter_subject_text = '通知'

    def loaditems(self):
        if os.path.exists(self.savePath):
            with open(self.savePath, 'rb') as file:
                lstItems = pickle.load(file)
        else:
            lstItems = []
        return lstItems

    def saveItems(self, lstItems):
        file = open(self.savePath, 'wb')
        pickle.dump(lstItems, file)
        file.close()


    def clean_date(self,datetext):
        """
        :param datetext: 'Tue, 13 Oct 2020 14:02:44 +0800 (CST)'
        :return: datetime.datetime(2020, 10, 13, 22, 40, 18, 441335, tzinfo=<DstTzInfo 'Asia/Taipei' LMT+8:06:00 STD>)
        """
        date = datetime.datetime.fromtimestamp(time.mktime(email.utils.parsedate(datetext)))
        return date.replace(tzinfo=pytz.timezone('Asia/Taipei'))

    def get_message_all(self, num=10):
        messages = []
        return messages

    def filter_email(self):
        for m in self.ret:
            if self.filter_subject_text in m.get('Subject'):
                self.msgs.append(m)

    def send_line(self):
        """發送TG"""
        print('發送TG')
        for i in self.msgs:
            print(i)

    def run(self):
        # 檢查有沒有新出現的
        items_old = self.loaditems()

        msgs = self.get_message_all()

        self.saveItems(msgs)

        print("收到的信件 %s" % [i['Subject'] for i in msgs])
        #     # items_old = []
        # 去除重複 字典跟字典
        diff_items = msgs.copy()
        # print(len(diff_items))
        for e in items_old:
            if e in diff_items:
                diff_items.remove(e)

        print("過濾的信件 %s" % [i['Subject'] for i in diff_items])

        self.ret = diff_items
        logger.debug(self.ret)
        return self.ret

    def main(self):
        self.run()
        self.filter_email()  # 符合"過濾條件"
        self.send_line()


def mail():
    Email().main()

if __name__ == '__main__':
    logger.info("mail is start")
    scheduler.add_job(mail, CronTrigger.from_crontab('*/1 * * * *'), id='mail_run')
    scheduler.start()