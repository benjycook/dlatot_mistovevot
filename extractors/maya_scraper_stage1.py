# -*- coding: utf-8 -*-

import requests
from lxml.html import fromstring
from time import sleep
from datetime import timedelta, date
from tqdm import tqdm
# from datapackage_pipelines.wrapper import ingest, spew
#
# parameters, datapackage, res_iter = ingest()

# URL FORMAT
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


# DATE GENERATOR
def daterange(d1, d2):
    for n in range(int((d2 - d1).days)):
        if n % 7 == 0:
            yield d1 + timedelta(n-7), d1 + timedelta(n)


def find_class_wrapper(src, class_name):
    if src is None:
        return None
    cls = src.find_class(class_name)
    if len(cls):
        return cls[0]
    return None


def get_page_count(doc):
    pages = find_class_wrapper(doc, 'feedItem feedPager')
    page_list = find_class_wrapper(pages, "pagination")
    count = int(page_list[len(page_list) - 6].text_content())
    return count


def scrape(start_date, end_date, page_num):

    items = []
    req = splash + base_url + page_url + \
        filters["start_date"].format(start_date=start_date) + \
        filters["end_date"].format(end_date=end_date) + \
        filters["page"].format(page_num=page_num) + filters["events"] + wait_time.format(time=1)

    res = requests.get(req)

    if res.status_code != 200:
        sleep(1)
        return [], 0, True

    doc = fromstring(res.text)
    if page_num == 1:
        try:
            count = get_page_count(doc)
        except:
            count = 0
    else:
        count = 0

    feedItems = doc.find_class("feedItem ng-scope")

    for feedItem in feedItems:
        tmp = find_class_wrapper(feedItem, "messageContent ng-binding")
        text = tmp.text_content()
        if any(title in text for title in [u'מינוי', u'הנהלה ונושאי משרה']):
            root = tmp.getparent()
            company = find_class_wrapper(root, "feedItemCompany ng-scope")
            date_el = find_class_wrapper(root, "feedItemDate")
            maya_link = base_url + tmp.get('href')
            item = {"date": date_el.text_content(),
                    "company_name": company[0][0].text_content().encode('utf-8'),
                    "action": tmp.get('title').encode('utf-8'),
                    "maya_link": maya_link}
            items.append(item)

    sleep(0.01)
    return items, count, False


def main():
    # verify dates
    for year in range(2007, date.today().year+1):
        start_d = date(year, 1, 1)
        end_d = date(year, 12, 31)
        if year is date.today().year:
            end_d = date.today()

        item_list = []
        failed_list = []

        for st, ed in tqdm(daterange(start_d, end_d)):
            start = str(st).replace(' ', 'T')
            end = str(ed).replace(' ', 'T')
            items, page_count, failed = scrape(start, end, 1)
            if failed:
                failed_list.append({'start':start, 'end': end})
            item_list += items
            for p in range(2, page_count + 1):
                items, _, failed = scrape(start, end, p)
                if failed:
                    failed_list.append({'start': start, 'end': end})
                item_list += items
            save_to_disk(items, failed_list, year, start_d, ed)


if __name__ == "__main__":
    main()