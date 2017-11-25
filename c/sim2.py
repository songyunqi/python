from time import sleep

from selenium import webdriver
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver import ActionChains


def read_(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        return lines


def prepare_driver(vendor):
    if vendor == "ie":
        driver = webdriver.Ie()
        return driver
    elif vendor == "firefox":
        driver = webdriver.Firefox()
        return driver
    elif vendor == "chrome":
        driver = webdriver.Chrome()
        return driver
    else:
        exit()


def pre_login(driver):
    iframe = driver.find_element_by_xpath("//div/iframe")
    driver.switch_to.frame(iframe)


def login(driver):
    username = driver.find_element_by_id('username')
    password = driver.find_element_by_id('password')
    slider = driver.find_element_by_xpath("//div[@id='J_StaticForm']/div/div[3]")
    login_btn = driver.find_element_by_xpath("//form[@id='login-form']/div[@class='login-btn']/a")

    login_box = driver.find_element_by_xpath("//body/div[@class='login-box']")

    if username:
        username.send_keys('15080822103')
    else:
        print("username not found")
    if password:
        password.send_keys('xxxxxxxxxx')
    else:
        print("password not found")

    # click
    if username:
        username.click()

    if slider:
        print("get slider")
        action = ActionChains(driver)
        action.click_and_hold(slider).perform()  # 鼠标左键按下
        for index in range(200):
            try:
                action.move_by_offset(50, 0).perform()  # 平行移动鼠标
            except MoveTargetOutOfBoundsException:
                break
        action.reset_actions()
        # enalbe
        slider.click()

    driver.implicitly_wait(1)

    if login_btn:
        login_btn.click()


def quit(driver):
    driver.quit()


def main():
    driver = prepare_driver("chrome")
    driver.get("https://pay.suning.com/epp-epw/login/login.action?res_code=4&res_message=NOT_LOGIN")
    driver.implicitly_wait(1)
    pre_login(driver)
    driver.implicitly_wait(1)
    login(driver)
    # quit(driver)


def batch_login(url):
    lines = read_("erf.txt")

    for line in lines:
        if line:
            splits = line.split(",")
            driver = prepare_driver("chrome")
            driver.get(url)

        quit(driver)


if __name__ == '__main__':
    pass
    main()
    # batch_login("https://pay.suning.com/epp-epw/login/login.action?res_code=4&res_message=NOT_LOGIN")

"""


"""
