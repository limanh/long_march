# -*- coding:utf-8 -*-
# @Time : 2022/4/11 10:34
# @Author : huangmanli
# @File : shiyanshiyanshiyan.py
# @Software : PyCharm
#url="https://httpbin.org/ip"
import aiohttp
import asyncio



asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # 加上这一行

# proxy=auto.proxies, proxy_auth=auto.proxy_auth 这里的代理需要换成自己的
async def quest(url,headers,proxy):
    con = aiohttp.TCPConnector(ssl=False)
    try:
        async with aiohttp.ClientSession(connector=con, trust_env=True) as sess: # 加上trust_env=True
            async with sess.get(url=url, headers=headers, proxy=proxy,timeout=5) as res:
                print(proxy)
                return proxy
    except:
        pass



async def main():
    proxies = ['http://182.101.207.11:8080','http://47.101.153.1:80','http://223.96.90.216:8085','http://112.6.117.178:8085',
               'http://120.42.46.226:6666','http://113.31.118.22:80']

    proxies2=['219.246.65.55:80','36.133.223.22:7777','39.108.88.42:80','47.93.239.66:1080','183.173.178.126:7890','182.139.110.18:9000',
              '59.125.177.31:8080','221.122.91.65:80','218.106.61.5:21080']
    proxies3=['8.134.51.67:808','111.229.161.172:888','117.95.100.230:8089','165.16.66.93:8080','144.217.7.157:5566',
              '201.217.49.2:80','51.75.206.209:80','152.136.62.181:9999','112.6.117.135:8085','193.150.117.61:8000','120.42.46.226:6666',
              '157.245.110.145:80','218.78.54.149:8901','8.210.83.33:80','85.30.215.48:32946','175.106.10.227:7878','170.155.5.235:8080',
              '106.52.172.214:8088','54.217.76.59:80','188.235.130.50:8080','81.68.243.42:80','106.14.255.124:80','182.34.136.205:25624',
              '190.107.224.150:3128','185.82.99.11:9091','47.88.7.115:3129','77.68.12.217:80','77.68.12.217:80','77.68.12.217:80',
              '77.68.12.217:80','77.68.12.217:80']
    #小幻代理：https://ip.ihuan.me/ti.html
    ip_dic=[]
    tasks=[]
    for i in proxies:
        # proxy = "http://" + i
        proxy = i
        ip = await quest(url, headers, proxy)
        ip_dic.append(ip)
        task = asyncio.create_task(quest(url, headers, proxy))
        tasks.append(task)
    print(ip_dic)
    await asyncio.wait(tasks)


if __name__ == '__main__':
    url = "http://httpbin.org/ip"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.3"
    }

    asyncio.run(main())
    # 'http://47.101.153.1:80', 'http://223.96.90.216:8085', 'http://112.6.117.178:8085', 'http://120.42.46.226:6666'

