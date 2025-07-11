from datetime import datetime
import pytz


class TimeHelper:
    @staticmethod
    def vn_timezone():
        vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
        return datetime.now(vn_tz)

    @staticmethod
    def utc_timezone():
        utc_tz = pytz.timezone("UTC")
        return datetime.now(utc_tz)
