# -*- coding:UTF-8 -*-

import loginAPI
import time

if __name__ == "__main__":
    login_check = loginAPI.noBBLogin('http://42.192.50.232/api/', 'xxxxx', "test")
    # login_check = loginAPI.noBBLogin('http://127.0.0.1:8000/api/', 'xxx', "xxx")

    login_check.log_params = {
        "id": 9999999999999,
        "cdkey_id": 999,
        "login_time": login_check.get_current_time(),
        "logout_time": login_check.get_current_time(),
        "temp_link_code": "test",
        "status": 0,
    }
    status_code, cdkey = login_check.put_cdkeylogs(login_check.log_params)
    if status_code == -1 or status_code != 200:

        print(status_code, 'no')
    # time.sleep(60 * 60)
