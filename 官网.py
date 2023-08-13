import urllib.request
from lxml import etree

def get_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67'
    }
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    return content

# 新闻里面的content
def get_content2(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'
    }
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')

    return content

def down_load1(content): #新闻快递
    tree = etree.HTML(content)
    name_list = tree.xpath('//div[@id="Ncenterlist"]/ul/ul/li/a/@title')
    src_list = tree.xpath('//div[@id="Ncenterlist"]/ul/ul/li/a/@href')

    for i in range(len(name_list)):
        url = src_list[i]
        name = name_list[i]
        content = get_content2(url)
        tree = etree.HTML(content)
        neirong = tree.xpath('//*[@id="vsb_content"]/div/p/span/text()')
        str = "".join(neirong)

        for a in str:
            with open(name+".txt", "w", encoding='gbk') as code:
                code.write(str)
        print(name+" 下载完成")

    print("新闻快递已下载完毕")

def down_load2(content):# 通知公告和学术报告
    tree = etree.HTML(content)
    name_tree = ['//*[@id="NewContent"]/div[1]/div[2]/div/div/div/div[1]/ul/li/div/div[3]/a/@title', '//*[@id="NewContent"]/div[2]/div[2]/div/div/div/div[1]/ul/li/a[1]/@title']
    href_tree = ['//*[@id="NewContent"]/div[1]/div[2]/div/div/div/div[1]/ul/li/div/div[3]/a/@href', '//*[@id="NewContent"]/div[2]/div[2]/div/div/div/div[1]/ul/li/a[1]/@href']
    neirong_tree = ['//*[@id="vsb_content"]/div/div/descendant-or-self::span/text()', '//*[@id="vsb_content"]/div/p/span/text()']
    encode = ['utf-8-sig', 'gbk']
    for j in range(len(name_tree)):
        name_list = tree.xpath(name_tree[j])
        href_list = tree.xpath(href_tree[j])

        for i in range(len(name_list)):
            name = name_list[i]
            url = 'https://www.swpu.edu.cn/'+href_list[i]
            content = get_content2(url)
            tree = etree.HTML(content)
            neirong = tree.xpath(neirong_tree[j])
            if neirong == []:
                print(name+" 无权限，无法读取")
            else:
                str = ''.join(neirong)
                for a in str:
                    with open(name + ".txt", "w", encoding=encode[j]) as code:
                        code.write(str)
                print(name+" 下载完成")

    print("通知公告和学术报告下载完成")

# 科技成果
def down_load3(content):
    tree = etree.HTML(content)
    name_list = tree.xpath('//*[@id="SixCenterC"]/ul/li/div/a/@title')
    href_list = tree.xpath('//*[@id="SixCenterC"]/ul/li/div/a/@href')

    for i in range(len(name_list)):
        name = name_list[i]
        url = 'https://www.swpu.edu.cn/'+href_list[i]
        content = get_content2(url)
        tree = etree.HTML(content)
        neirong = tree.xpath('//*[@id="vsb_content"]/div/p/descendant-or-self::span/text()')
        if neirong == []:
            print(name + " 无权限，无法读取")
        else:
            # 文档下载
            str = ''.join(neirong)
            name_str = ''.join(name)
            a = list(name_str)
            # 判断特殊符号并删除
            x = name_str.find('/')
            if x >= 0:
                a[x : x + 1] = "o"
                name = ''.join(a)
            for a in str:
                with open(name + ".txt", "w", encoding='utf-8-sig') as code:
                    code.write(str)
            # 图片下载
            src_list = tree.xpath('//*[@id="vsb_content"]/div/p/img/@src')
            pname_list = tree.xpath('//*[@id="vsb_content"]/div/p[@style="text-align: center;"]/text()')
            if pname_list == []:
                pname_list = tree.xpath('//*[@id="vsb_content"]/div/p[@style="text-align: center;"]/span/text()')
            if pname_list == []:
                print(name + " 没有找到图片")
            else:
                for j in range(len(src_list)):
                    url = 'https://www.swpu.edu.cn/' + src_list[j]
                    urllib.request.urlretrieve(url=url, filename=name + ' ' + pname_list[j] + '.jpg')

            print(name + " 下载完成")
    print("科技成果发布下载完毕")


if __name__ == '__main__':
    url = 'https://www.swpu.edu.cn/'
    # 获取content
    content = get_content(url)
    # 下载文件
    down_load1(content) #新闻快递
    down_load2(content) #通知公告和学术报告
    down_load3(content) #科技成果发布