import urllib.request as ur
import urllib.parse as up
import re
from http.cookiejar import CookieJar


# 知乎post数据里有一个_xsrf，需要从原网页中提取
def xsrf():
    url = 'http://www.zhihu.com/login'
    zhihu = ur.urlopen(url).read().decode('utf-8')
    pattern = re.compile(r'name="_xsrf" value="(.*?)"/>')
    match = pattern.findall(zhihu)
    xsrf = match[0]
    return xsrf


# post数据
def post_data():
    data = dict()
    data['_xsrf'] = xsrf
    data['email'] = '394934353@qq.com'
    data['password'] = 'q123456'
    data['rememberme'] = 'y'

    post_data = up.urlencode(data).encode('utf-8')  # 编译post数据
    return post_data


hdr = {'Accept': '*/*',
       'Accept-Encoding': 'gzip, deflate',
       'Accept-Language': 'zh-CN,zh;q=0.8',
       # 'Connection':'keep-alive',
       # 'Content-Length':'95',
       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
       # 'Host':'www.zhihu.com',
       # 'Origin':'http://www.zhihu.com',
       # 'RA-Sid':'DEADFC42-20150104-093648-9e5c2d-88ba9a',
       # 'Referer':'http://www.zhihu.com/',
       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
       'X-Requested-With': 'XMLHttpRequest'}


# cookie上创建一个opener
def build_openner():
    cookie = CookieJar()
    cookie_handler = ur.HTTPCookieProcessor(cookie)
    opener = ur.build_opener(cookie_handler)
    return opener


xsrf = xsrf()
post_data = post_data()
opener = build_openner()
ur.install_opener(opener)  # 安装opener


def main():
    url = 'http://www.zhihu.com/login'
    req = ur.Request(url, post_data, hdr)
    response = opener.open(req)
    page = response.read()
    # print(page)
    # 测试成功与否
    testurl = 'http://www.zhihu.com/settings/account'
    req = ur.urlopen(testurl)
    print(req.read().decode('utf-8'))


main()
