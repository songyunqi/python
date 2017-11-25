import os
import unittest

from selenium import webdriver

dictInput = {}


class Test(unittest.TestCase):
    def setUp(self):
        self.chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"  # 将chromedriver.exe拷贝到你想要调用的chrome安装路径下即可
        os.environ["webdriver.chrome.driver"] = self.chromedriver
        self.browser = webdriver.Chrome(self.chromedriver)

    def test(self):
        self.browser.get('www.baidu.com')  # 此处xxxx为网页的url


if __name__ == '__main__':
    import sys;

    sys.argv = ['', 'Test.test']
    unittest.main()
