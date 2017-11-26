from threading import Thread
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains


class AutoBatchProcess:
    pass

    def __init__(self, url, file, vendor):
        self.url = url
        self.file = file
        self.vendor = vendor
        self.lines = None

    def load_user(self):
        with open(self.file, 'r') as f:
            self.lines = f.readlines()

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

            while True:
                action.move_by_offset(10, 0).perform()
                if valid_msg.text == "验证通过":
                    action.release(slider).perform()
                    break

                    # for index in range(20):
                    #     try:
                    #         action.move_by_offset(10, 0).perform()
                    #         # 平行移动鼠标
                    #     except UnexpectedAlertPresentException:
                    #         break

        driver.implicitly_wait(1)

        if login_btn:
            login_btn.click()

    def process(self, driver, username, password):
        self.login(driver, username, password)

        # 登录成功之后还是当前页面
        financing = driver.find_element_by_xpath("//div[@class='nav']/a[1]")
        if financing:
            financing.click()

        handles = driver.window_handles
        if len(handles) > 1:
            driver.switch_to.window(handles[1])

        print("ng.....")

        timing_financing = driver.find_element_by_xpath("//div[@class='sub-nav-content']/a[3]")
        if timing_financing:
            timing_financing.click()
        handles = driver.window_handles
        if len(handles) > 2:
            driver.switch_to.window(handles[2])

        print("ng.....")

        bill = driver.find_element_by_xpath("//div[@id='tabCaiyunMain']/ul/li[2]")

        if bill:
            bill.click()

    def batch_process(self):
        self.load_user()
        threads = []
        for line in self.lines:
            kv_pair = line.split(",")
            driver = self.get_driver()
            t = Thread(target=self.process, args=(driver, kv_pair[0], kv_pair[1]))
            threads.append(t)
        for thr in threads:
            thr.start()

        input("\n\n Press the enter key to exit.")


if __name__ == '__main__':
    pass
    auto_batch_process = AutoBatchProcess("https://pay.suning.com/epp-epw/login/login.action", "erf.txt", "chrome")
    auto_batch_process.batch_process()
