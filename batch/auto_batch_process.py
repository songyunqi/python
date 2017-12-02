import json
from threading import Thread
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains


class UserInfo:
    pass

    def __init__(self, username, password, pin):
        self.username = username
        self.password = password
        self.pin = pin


class AutoBatchProcess:
    pass

    def __init__(self, url, file, vendor):
        self.url = url
        self.file = file
        self.vendor = vendor
        self.lines = None
        self.users = []

    def load_user(self):
        with open(self.file, 'r') as f:
            self.lines = f.readlines()

        for line in self.lines:
            kv_pair = line.split(",")
            t_user = UserInfo(kv_pair[0], kv_pair[1], kv_pair[2])
            self.users.append(t_user)

    def load_buy_info(self):
        with open(self.file, 'r') as f:
            setting = json.load(f)

    def load_sell_info(self):
        print("")

    def quit(self, driver):
        driver.quit()

    # get driver
    def get_driver(self):
        if self.vendor == "ie":
            driver = webdriver.Ie()
            return driver
        elif self.vendor == "firefox":
            driver = webdriver.Firefox()
            return driver
        elif self.vendor == "chrome":
            driver = webdriver.Chrome()
            return driver
        else:
            exit(0)

    def pre_login(self, driver):
        iframe = driver.find_element_by_xpath("//div/iframe")
        driver.switch_to.frame(iframe)

    def login(self, driver, username, password):
        driver.get(self.url)
        driver.implicitly_wait(1)
        self.pre_login(driver)
        driver.implicitly_wait(1)
        e_username = driver.find_element_by_id('username')
        e_password = driver.find_element_by_id('password')

        # text msg
        valid_msg = driver.find_element_by_xpath("//div[@id='J_StaticForm']/div/div[2]")

        slider = driver.find_element_by_xpath("//div[@id='J_StaticForm']/div/div[3]")

        login_btn = driver.find_element_by_xpath("//form[@id='login-form']/div[@class='login-btn']/a")

        if e_username:
            e_username.send_keys(username)
        else:
            print("element username not found")
        if e_password:
            e_password.send_keys(password)
        else:
            print("element password not found")

        driver.implicitly_wait(1)

        # click remove autocomplete
        if e_username:
            e_username.click()

        if e_password:
            e_password.click()

        # 等待滑块
        sleep(0.1)  # 等待停顿时间

        if slider:
            print("get slider")
            action = ActionChains(driver)
            action.click_and_hold(slider).perform()

            loop_time = 0
            expected_times = 10

            while True:
                action.move_by_offset(10, 0).perform()
                sleep(0.1)
                if loop_time >= expected_times:
                    e_username.click()

                if valid_msg.text == "验证通过":
                    break
                else:
                    print("继续滑动")
                    print("loop_time:" + str(loop_time))

                loop_time = loop_time + 1

        driver.implicitly_wait(1)

        if login_btn:
            login_btn.click()

    def process(self, driver, user):
        self.login(driver, user.username, user.password)

        # 登录成功之后还是当前页面
        financing = driver.find_element_by_xpath("//div[@class='nav']/a[1]")
        if financing:
            financing.click()

        handles = driver.window_handles
        if len(handles) > 1:
            driver.switch_to.window(handles[1])

        print("continue....")

        timing_financing = driver.find_element_by_xpath("//div[@class='sub-nav-content']/a[3]")
        if timing_financing:
            timing_financing.click()
        handles = driver.window_handles
        if len(handles) > 2:
            driver.switch_to.window(handles[2])

        print("continue....")

        bill = driver.find_element_by_xpath("//div[@id='tabCaiyunMain']/ul/li[1]")
        if bill:
            bill.click()

        # quit
        # self.quit(driver)

    def batch_process(self):
        self.load_user()
        threads = []
        for t_user in self.users:
            # kv_pair = line.split(",")
            driver = self.get_driver()
            t = Thread(target=self.process, args=(driver, t_user))
            threads.append(t)
        for thr in threads:
            thr.start()

        input("\n\n Press the enter key to exit.")


if __name__ == '__main__':
    pass
    auto_batch_process = AutoBatchProcess("https://pay.suning.com/epp-epw/login/login.action", "erf.txt", "chrome")
    auto_batch_process.batch_process()
