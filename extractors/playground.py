# -*- coding: utf-8 -*-

import requests
from lxml.html import fromstring
import pandas as pd
from time import sleep
from datetime import timedelta, date
from tqdm import tqdm

splash = "http://localhost:8050/render.html?url="
base_url = "http://maya.tase.co.il/"
page_url = "reports/company"
filters = {
    "start_date": "?q=%7B%22DateFrom%22:%22{start_date}%22,",
    "end_date": "%22DateTo%22:%22{end_date}%22",
    "page": ",%22Page%22:{page_num}",
    "events": ",%22events%22:%5B600%5D,%22subevents%22:%5B620,605,603,601,602,621,604,606,615,613,611,612,622,614,616%5D%7D"
    }
wait_time ='&timeout=10&wait={time}'


def daterange(d1, d2):
    for n in range(int((d2 - d1).days)):
        if n % 7 == 0:
            yield d1 + timedelta(n-7), d1 + timedelta(n)


def find_class(src, class_name):
    if src is None:
        return None
    cls = src.find_class(class_name)
    if len(cls):
        return cls[0]
    return None


def get_html_link(link):
    count = 0
    while count < 3:
        req = splash + link + wait_time.format(time=0.25+count*0.5)
        res = requests.get(req)
        if res.status_code != 200:
            count += 1
            sleep(0.5)
            continue

        doc = fromstring(res.text)
        msg = find_class(doc, "messageWrap")
        body = find_class(msg, 'messageBody')
        frame = find_class(body, "rptdoc ng-scope")
        if frame is not None:
            return frame.get('src')
        count += 1
        sleep(0.5)


def get_page_count(doc):
    pages = find_class(doc, 'feedItem feedPager')
    page_list = find_class(pages, "pagination")
    count = int(page_list[len(page_list) - 6].text_content())
    return count


def save_to_disk(ap, ca, ye, st_d,  ed_d  ):
    print "from {} to {} - current count: apps:{} , carrs: {}".format(st_d, ed_d, len(ap),len(ca))

    columns = ["date", "company_name", "action", "maya_link", "html_link"]
    appointments_df = pd.DataFrame(ap, columns=columns)
    appointments_df.drop_duplicates(subset=['html_link'])
    appointments_df.to_csv('appointment_{}.csv'.format(ye))

    carriers_df = pd.DataFrame(ca, columns=columns)
    carriers_df.drop_duplicates(subset=['html_link'])
    carriers_df.to_csv('carriers_{}.csv'.format(ye))


def scrap(start_date, end_date, page_num):
    apps = []
    cari = []
    req = splash + base_url + page_url + \
        filters["start_date"].format(start_date=start_date) + \
        filters["end_date"].format(end_date=end_date) + \
        filters["page"].format(page_num=page_num) + filters["events"] + wait_time.format(time=1)

    res = requests.get(req)

    # print req
    # print res.status_code
    if res.status_code != 200:
        sleep(1)
        return [], [], 0

    doc = fromstring(res.text)
    if page_num == 1:
        try:
            count = get_page_count(doc)
        except:
            count = 0
    else:
        count = 0

    items = doc.find_class("feedItem ng-scope")
    if items is None:
        return [], [], 0
    for item in items:
        tmp = find_class(item, "messageContent ng-binding")
        text = tmp.text_content()
        if any(title in text for title in [u'מינוי', u'הנהלה ונושאי משרה']):
            root = tmp.getparent()
            company = find_class(root, "feedItemCompany ng-scope")
            date_el = find_class(root, "feedItemDate")
            maya_link = base_url + tmp.get('href')
            item = {"date": date_el.text_content(),
                    "company_name": company[0][0].text_content().encode('utf-8'),
                    "action": tmp.get('title').encode('utf-8'),
                    "maya_link": maya_link,
                    "html_link": get_html_link(maya_link)}
            # print item
            if u'מצבת ליום' in text:
                cari.append(item)
            else:
                apps.append(item)

    sleep(0.01)
    return apps, cari, count


def main():
    for year in range(2015, date.today().year+1):
        start_d = date(year, 1, 1)
        end_d = date(year, 12, 31)
        if year is date.today().year:
            end_d = date.today()

        appointments = []
        carriers = []

        for st, ed in tqdm(daterange(start_d, end_d)):
            start = str(st).replace(' ', 'T')
            end = str(ed).replace(' ', 'T')
            appoints, carris, page_count = scrap(start, end, 1)
            appointments += appoints
            carriers += carris
            for p in range(2, page_count + 1):
                appoints, carris, _ = scrap(start, end, p)
                appointments += appoints
                carriers += carris
            save_to_disk(appointments, carriers, year, start_d, ed)


if __name__ == "__main__":
    main()
