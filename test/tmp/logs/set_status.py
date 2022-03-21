# -*- coding:UTF-8 -*-

import loginAPI
import time


if __name__ == "__main__":
    login_check = loginAPI.noBBLogin('http://42.192.50.232/api/', 'xxx', "xxx")

    status_code, cdkeylogs = login_check.get_cdkeylogs(param="?status=0")
    with open('./status0logs.log', 'w') as f:
        f.write(str(cdkeylogs))
