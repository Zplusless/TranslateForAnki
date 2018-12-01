import http.client
import hashlib
import json
import urllib
import random
import csv
import time
import os


def baidu_translate(content):
    appid = '20151113000005349'
    secretKey = 'osubCEzlGjzvw8qdQc41'
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = content
    fromLang = 'en'  # 源语言
    toLang = 'zh'   # 翻译后的语言
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        jsonResponse = response.read().decode("utf-8")  # 获得返回的结果，结果为json格式
        js = json.loads(jsonResponse)  # 将json格式的结果转换字典结构
        # dst = str(js["trans_result"][0]["dst"])  # 取得翻译后的文本结果
        dst = js["trans_result"][0]["dst"]  # 取得翻译后的文本结果
        # print(isinstance(dst,str),':',dst)  # 打印结果
        return dst
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()


def run(infile, outfile):
    pairs = []
    with open(infile, 'r', encoding='utf-8') as fin:
        for line in fin:
            # print(line=='\n' or '='in line,'---->',line.strip())
            if not (line == '\n' or '='in line):
                en = line.strip()#.encode('gbk', 'ignore').decode('gbk')
                # print(isinstance(en,str),':',en)
                zh = baidu_translate(en)
                time.sleep(1)
                print(zh)
                pairs.append([zh, en])  # 第一个字段是正面，第二个是背面
    with open(outfile, 'w', newline='', encoding='utf8') as fout:
        csv_writer = csv.writer(fout)
        csv_writer.writerows(pairs)

if __name__ == '__main__':

    default_path = 'input.txt'
    default_csv = r'output.csv'

    run(infile=default_path, outfile=default_csv)

    time = time.strftime(r'%y-%m-%d',time.localtime())
    newname = '文献好句子_'+time+'.txt'
    os.rename(default_path, newname)
    print('原文件已经更名为：', newname)

