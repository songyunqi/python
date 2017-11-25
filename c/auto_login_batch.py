from threading import Thread

from selenium import webdriver
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver import ActionChains


class AutoLoginBatch:
    """ init """

    def __init__(self, url, file, vendor):
        self.url = url
        self.file = file
        self.vendor = vendor
        self.lines = None

    """ read file """

    def read_(self):
        with open(self.file, 'r') as f:
            self.lines = f.readlines()

    """ pre_login """

    def pre_login(self, driver):
        iframe = driver.find_element_by_xpath("//div/iframe")
        driver.switch_to.frame(iframe)

    # single login
    def login(self, driver, username, password):
        driver.get(self.url)
        driver.implicitly_wait(1)
        self.pre_login(driver)
        driver.implicitly_wait(1)
        e_username = driver.find_element_by_id('username')
        e_password = driver.find_element_by_id('password')
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

        if slider:
            print("get slider")
            action = ActionChains(driver)
            action.click_and_hold(slider).perform()  # 鼠标左键按下
            for index in range(10):
                try:
                    action.move_by_offset(50, 0).perform()  # 平行移动鼠标
                except MoveTargetOutOfBoundsException:
                    break
            action.reset_actions()

        """ slide ok """
        slider.click()

        driver.implicitly_wait(1)

        if login_btn:
            login_btn.click()

    def process(self, driver, username, password):
        self.login(driver, username, password)
        handles = driver.window_handles
        # driver.find_element_by_xpath("//form[@id='login-form']/div[@class='login-btn']/a")
        driver.switch_to.window(handles[1])

    # quit
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

    # batch login
    def batch_login(self):
        self.read_()
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
    auto_login_batch = AutoLoginBatch("https://pay.suning.com/epp-epw/login/login.action", "erf.txt", "chrome")
    auto_login_batch.batch_login()
