# -*- coding:utf-8 -*-
# @Time : 2022/4/11 9:59
# @Author : huangmanli
# @File : get_author_detail.py
# @Software : PyCharm

import xlrd
import asyncio
import aiohttp
import hashlib
import re
import execjs
from lxml import etree
import json
from xlutils.copy import copy

def read_excel():
    tables = []
    # 打开文件
    workbook = xlrd.open_workbook(r'景点信息总表.xls')
    # 根据sheet索引或者名称获取sheet内容
    sheet = workbook.sheet_by_name('Sheet1')
    # 读取是从0开始，不是1 ！！！
    for row in range(sheet.nrows):
        table = {'author': sheet.cell_value(row, 0), 'link': sheet.cell_value(row, 1)}
        # 清楚link为0的目的地
        tables.append(table)
    del tables[0]
    return tables


async def getCookie(data):
    """
    通过加密对比得到正确cookie参数
    :param data: 参数
    :return: 返回正确cookie参数
    """
    chars = len(data['chars'])
    for i in range(chars):
        for j in range(chars):
            clearance = data['bts'][0] + data['chars'][i] + data['chars'][j] + data['bts'][1]
            encrypt = None
            if data['ha'] == 'md5':
                encrypt = hashlib.md5()
            elif data['ha'] == 'sha1':
                encrypt = hashlib.sha1()
            elif data['ha'] == 'sha256':
                encrypt = hashlib.sha256()
            encrypt.update(clearance.encode())
            result = encrypt.hexdigest()
            if result == data['ct']:
                return clearance


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
async def author_page(url,proxy):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.3",
        'Host': 'www.mafengwo.cn',
        'Referer': url,
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'sec-ch-ua-mobile': '?0',
        'ec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1'}
    con = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=con, trust_env=True) as session:  # 加上trust_env=True
        async with session.get(url=url, headers=headers,proxy=proxy) as resp1:  # 拿到第一次响应数据
            # print(await resp1.text())
            jsl_clearance_s = re.findall(r'cookie=(.*?);location', await resp1.text())[0]
            jsl_clearance = str(execjs.eval(jsl_clearance_s)).split('=')[1].split(';')[0]  # js解密，拿到需要的第一次cookie值
            async with session.get(url=url, headers=headers,proxy=proxy, cookies={'__jsl_clearance': jsl_clearance}) as resp2:
                # print(await resp2.text())
                data = json.loads(re.findall(r';go\((.*?)\)', await resp2.text())[0])  # 提取go函数
                jsl_clearance = await getCookie(data)  # 拿到第二次cookie值
                # print(jsl_clearance)
                async with session.get(url=url, headers=headers,proxy=proxy,cookies={'__jsl_clearance': jsl_clearance}) as resp3:
                    try:
                        # 居住地
                        tree = etree.HTML(await resp3.text())
                        citys = tree.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[4]/span[2]/text()')[0]
                        # 现居：忻州
                        city = re.compile(r'现居：(.*)').findall(citys)[0]
                    except:
                        city = ''
                    try:
                        # 性别
                        gender = re.compile(r'<i class="MGender(.*?) mfw-acc-hide"></i>').findall(await resp3.text())[0]
                    except:
                        gender = ''
                    try:
                        # 个性签名
                        introduction = tree.xpath('//*[@id="_j_profilearea"]/div/pre/text()')[0]
                    except:
                        introduction = ''
                    author_dic = {'city': city, 'gender': gender, 'introduction': introduction}
                    # print(author_dic)
    return author_dic

async def zhuijia(datalist,name,index):
    # 读取原表格
    workbook = xlrd.open_workbook("景点信息总表.xls")
    # 拷贝新的excel,并从rows行开始追加写入
    new_workbook = copy(workbook)
    new_sheet = new_workbook.get_sheet(0)

    print("写入第%d条······" % (index + 1))
    city = datalist['city']
    gender = datalist['gender']
    introduction = datalist['introduction']
    print(city, gender, introduction)
    new_sheet.write(index + 1, 2, city)
    new_sheet.write(index + 1, 3, gender)
    new_sheet.write(index + 1, 7, introduction)
    new_sheet.write(index + 1, 9, name)

    new_workbook.save("景点信息总表.xls")
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~追加完成~~~~~~~~~~~~~~~~~~~~~~~~~~·')
    return index+1

async def main(tables):
    ip_dic = ['http://106.75.25.83:80', 'http://112.6.117.178:8085', 'http://112.6.117.135:8085', 'http://120.220.220.95:8085',
              'http://223.96.90.216:8085', 'http://218.106.61.5:21080','http://219.246.65.55:80','http://39.108.88.42:80',
              'http://47.93.239.66:1080','http://221.122.91.65:80', 'http://218.106.61.5:21080','http://120.42.46.226:6666',
              'http://221.7.197.248:8000', 'http://180.97.34.35:80', 'http://112.80.248.73:80']
    tasks=[]
    # print(len(ip_dic))   # 11
    # data=['3','6','10','16','20']
    for i in range(6501,6647):  # 6647  5很不错
        proxy=ip_dic[3]  # 'http://120.220.220.95:8085';'http://223.96.90.216:8085'# 6可以,10很不错第二个，17
        author=tables[i]['author']
        url = tables[i]['link']
        task=asyncio.create_task(zhuijia(await author_page(url,proxy),author,i))
        tasks.append(task)
    await asyncio.wait(tasks)

# async def main():
#     proxes=


if __name__ == '__main__':
    tables = read_excel()
    asyncio.run(main(tables))





