from CONSTANT import mkdir
import os
import requests
import CONSTANT3
from lxml import etree
import time
import copy
from tqdm import tqdm

urls = {
    "Iran2000": "https://www.worldpop.org/geodata/summary?id=11871",
    "Iran2005": "https://www.worldpop.org/geodata/summary?id=13116",
    "pakistan2000": "https://www.worldpop.org/geodata/summary?id=11908",
    "pakistan2005": "https://www.worldpop.org/geodata/summary?id=13153",
    "egypt2000": "https://www.worldpop.org/geodata/summary?id=11851",
    "egypt2005": "https://www.worldpop.org/geodata/summary?id=13096",
    "india2000": "https://www.worldpop.org/geodata/summary?id=12021",
    "india2005": "https://www.worldpop.org/geodata/summary?id=13266",
    "maldives2000": "https://www.worldpop.org/geodata/summary?id=11891",
    "maldives2005": "https://www.worldpop.org/geodata/summary?id=13136",
    "uzbekistan2000": "https://www.worldpop.org/geodata/summary?id=11998",
    "uzbekistan2005": "https://www.worldpop.org/geodata/summary?id=13243",
    "turkey2000": "https://www.worldpop.org/geodata/summary?id=11937",
    "turkey2005": "https://www.worldpop.org/geodata/summary?id=13182",
    "greece2000": "https://www.worldpop.org/geodata/summary?id=11801",
    "greece2005": "https://www.worldpop.org/geodata/summary?id=13046",
    "malaysia2000": "https://www.worldpop.org/geodata/summary?id=11901",
    "malaysia2005": "https://www.worldpop.org/geodata/summary?id=13146",
    "srilanka2000": "https://www.worldpop.org/geodata/summary?id=11806",
    "srilanka2005": "https://www.worldpop.org/geodata/summary?id=13051",
    "belarus2000": "https://www.worldpop.org/geodata/summary?id=11833",
    "belarus2005": "https://www.worldpop.org/geodata/summary?id=13078",
    "poland2000": "https://www.worldpop.org/geodata/summary?id=12028",
    "poland2005": "https://www.worldpop.org/geodata/summary?id=13273",
    "indonesia2000": "https://www.worldpop.org/geodata/summary?id=11870",
    "indonesia2005": "https://www.worldpop.org/geodata/summary?id=13115",
    "spain2000": "https://www.worldpop.org/geodata/summary?id=11797",
    "spain2005": "https://www.worldpop.org/geodata/summary?id=13042",
    "russia2000": "https://www.worldpop.org/geodata/summary?id=11792",
    "russia2005": "https://www.worldpop.org/geodata/summary?id=13037",
    "kazakhstan2000": "https://www.worldpop.org/geodata/summary?id=11876",
    "kazakhstan2005": "https://www.worldpop.org/geodata/summary?id=13121",
    "djibouti2000": "https://www.worldpop.org/geodata/summary?id=11954",
    "djibouti2005": "https://www.worldpop.org/geodata/summary?id=13199",
}


def formatFloat(num):
    return '{:.2f}'.format(num)


for i in urls:
    # id 需要换
    otfpath = fr"E:\a\{i[:4]}"
    mkdir(otfpath)
    url = url[i]

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = resp.apparent_encoding
    html_tree = etree.HTML(resp.text)
    download_url = html_tree.xpath("//tbody//tr/td[1]/a/@href")

    for url in download_url:
        print(url)
        name = url.split('/')[-1]
        try:
            r = requests.get(url, stream=True)
            length = float(r.headers['content-length'])
            f = open(os.path.join(otfpath, name), 'wb')
            count = 0
            count_tmp = 0
            time1 = time.time()
            with tqdm(r.iter_content(chunk_size=512)) as t:
                for chunk in t:
                    t.total = 100
                    if chunk:
                        f.write(chunk)
                        count += len(chunk)
                        # if time.time() - time1 > 2:
                        #     # p = count / length * 100
                        #     # speed = (count - count_tmp) / 1024 / 1024 / 2
                        #     count_tmp = count

                        #     time1 = time.time()
            f.close()

        except Exception as e:
            print(e)
            with open(os.path.join(otfpath, 'fail.txt'), 'a') as f:
                f.write(url)
                f.write('\n')
            continue

        with open(os.path.join(otfpath, 'fail.txt'), 'r') as f:
            wrong = f.readlines()
        file = open(os.path.join(otfpath, 'fail.txt'), 'w').close()
        wrongchange = copy.deepcopy(wrong)
        i = 0
        while 1:
            url = wrong[i]
            if url in wrongchange:
                print(url)
                name = url.split('/')[-1]
                try:
                    r = requests.get(url, stream=True)
                    length = float(r.headers['content-length'])
                    f = open(os.path.join(otfpath, name), 'wb')
                    count = 0
                    count_tmp = 0
                    time1 = time.time()
                    for chunk in r.iter_content(chunk_size=512):
                        if chunk:
                            f.write(chunk)
                            count += len(chunk)
                            if time.time() - time1 > 2:
                                p = count / length * 100
                                speed = (count - count_tmp) / 1024 / 1024 / 2
                                count_tmp = count
                                print(name + ': ' + formatFloat(p) + '%' +
                                      ' Speed: ' + formatFloat(speed) + 'M/S')
                                time1 = time.time()
                    f.close()

                except Exception as e:
                    print(e)
                    if os.path.exists(os.path.join(otfpath, name)):
                        os.remove(os.path.join(otfpath, name))
                    i = i + 1
                    continue

                finally:
                    wrongchange.remove(url)
                    if len(wrongchange) == 0:
                        break
            i = i + 1
            if i % len(wrong) == 0:
                i = 0
