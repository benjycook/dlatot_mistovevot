# -*- coding: utf-8 -*-
"""
91, 93, 304, 306
info needed :
company name
report num 
date published
fullname
job title
job_start_date
jobs in the last five years
    job  title, company name , duration
"""
from itertools import product


def get_publish_date(html):
    table0 = html.find_all('table')[0]
    publish_date = table0.contents[1].find('span', {'id': 'HeaderSendDate'}).parent.contents[-1]
    publish_date = publish_date.replace(u'\r\n\t\t\t\t', '').replace(u'\t\r\n\t\t\t', '')
    print publish_date
    return publish_date


def get_fullname(html, table_num):
    table = html.find_all('table')[table_num]
    fullname = table.contents[1].find('textarea').contents[0]
    print fullname
    return  fullname, table


def get_identifier_type(table, content_idx1, content_idx2):
    span_idx1 = span_idx2 = 1
    if content_idx1 == content_idx2:
        span_idx1 = 2
        span_idx2 = 4
    identifier_type = table.contents[content_idx1].find_all('span')[span_idx1].contents[0]
    identifier_num = table.contents[content_idx2].find_all('span')[span_idx2].contents[0]
    print identifier_type, identifier_num
    return identifier_type, identifier_num


def get_birthday(html, table_num):
    table = html.find_all('table')[table_num]
    birthday = table.find_all('span')[1].contents[0]
    print birthday
    return birthday


def get_citizenshop(table, content_index, span_index=1):
    citizenship = table.contents[content_index].find_all('span')[span_index].contents[0]
    print citizenship
    return citizenship


def get_job_details(html, table_num, start_ind, title_ind, prior_ind):
    table = html.find_all('table')[table_num]
    try:
        job_start_at = table.contents[start_ind].find_all('span')[2].contents[0]
    except:
        job_start_at = table.contents[start_ind].find_all('span')[1].contents[0]

    try:
        job_title = table.contents[title_ind].find_all('span')[0].contents[0]
        if job_title == u'אחר':
            raise Exception
    except:
        job_title = table.contents[title_ind].find('textarea').contents[0]

    if prior_ind:
        prior_job = table.contents[prior_ind].find('span', {'id': 'Row0NewField21'}).contents[0]
    else:
        prior_job = '---'
    print job_title, job_start_at, prior_job
    return job_title, job_start_at, prior_job


def get_academic_background(table):
    academic_background = []
    for content_index, table_index in product([23, 27, 31, 3], [1, 0]):
        try:
            tr = table.contents[content_index].find_all('table')[table_index].find_all('tr')
            for item in tr:
                spans = item.find_all('span')
                txtareas = item.find_all('textarea')
                aca_bk = [i.contents[0] for i in spans+txtareas]
                academic_background.append(tuple(aca_bk))
        except Exception:
            pass
        else:
            break

    for i in academic_background:
        for j in i:
            print j
    return academic_background


def get_prior_jobs(table, html=None):
    prior_jobs_last_5 = []
    for content_index, table_index in product([29, 31, 35, 3], [1, 0]):
        try:
            # prior_jobs_last_5 = [
            #     (item.find_all('textarea')[0].contents[0], item.find_all('textarea')[1].contents[0],
            #      item.find_all('textarea')[2].contents[0])
            #     for item in table.contents[content_index].find_all('table')[table_index].find_all('tr')]
            tr = table.contents[content_index].find_all('table')[table_index].find_all('tr')
            for item in tr:
                spans = item.find_all('span')
                txtareas = item.find_all('textarea')
                aca_bk = [i.contents[0] for i in txtareas+ spans]
                prior_jobs_last_5.append(tuple(aca_bk))
        except Exception:
            pass
        else:
            break

    for i in prior_jobs_last_5:
        for j in i:
            print j

    return prior_jobs_last_5


def template_091_type_a(html):
    publish_date  = get_publish_date(html)

    fullname, table = get_fullname(html, 4)

    identifier_type, identifier_num = get_identifier_type(table, 5, 7)

    citizenship = get_citizenshop(table, content_index=9)

    birth_date = get_birthday(html, 5)

    job_title, job_start_at, prior_job_here = get_job_details(html, 4, 17, 21, 27)

    academic_background = get_academic_background(table)

    prior_jobs = get_prior_jobs(table)


def template_091_type_b(html):
    publish_date = get_publish_date(html)

    fullname, table = get_fullname(html, 3)

    identifier_type, identifier_num = get_identifier_type(table, 3 ,5)

    citizenship = get_citizenshop(table, content_index=7)

    birth_date = get_birthday(html, 5)

    job_title, job_start_at, prior_job_here = get_job_details(html, 3, 15, 19, 0)

    academic_background = get_academic_background(table)

    prior_jobs = get_prior_jobs(table)


def template_091(args):
    html, year = args
    if year in ['2008', '2011', '2012']:
        template_091_type_a(html)
    elif year in ['2004', '2005', '2006', '2007', '2017']:
        template_091_type_b(html)
    else:
        pass


def template_093(args):
    html, year = args
    publish_date = get_publish_date(html)

    fullname, table = get_fullname(html, 3)

    identifier_type, identifier_num = get_identifier_type(table, 1, 1)

    citizenship = get_citizenshop(table, content_index=1, span_index=6)

    table = html.find_all('table')[3]
    birth_date = table.find_all('span')[10].contents[0]

    job_title = table.find_all('span')[13].contents[0]
    job_start_at = table.find_all('span')[25].contents[0]

    print job_start_at, job_title

    table = html.find_all('table')[9]
    academic_background = get_academic_background(table)

    table = html.find_all('table')[11]
    prior_jobs = get_prior_jobs(table, html)


def template_304(args):
    html, year = args
    publish_date = get_publish_date(html)

    fullname, table = get_fullname(html, 5)

    identifier_type, identifier_num = get_identifier_type(table, 1, 1)

    citizenship = get_citizenshop(table, content_index=1, span_index=6)

    birth_date = get_birthday(html, 12)

    job_title, job_start_at, prior_job_here = get_job_details(html, 3, 25, 11, 0)

    table = html.find_all('table')[19]
    academic_background = get_academic_background(table)

    table = html.find_all('table')[21]
    prior_jobs = get_prior_jobs(table, html)


def template_306(args):
    html, year = args
    publish_date = get_publish_date(html)

    fullname, table = get_fullname(html, 5)
    table = html.find_all('table')[6]
    identifier_type = table.contents[1].find_all('span')[1].contents[0]
    table = html.find_all('table')[7]
    identifier_num = table.contents[1].find_all('span')[1].contents[0]

    print  identifier_type, identifier_num
    table = html.find_all('table')[8]
    citizenship = get_citizenshop(table, content_index=1, span_index=1)

    table = html.find_all('table')[9]
    birthday = table.find_all('span')[1].contents[0]
    birth_date = get_birthday(html, 10)

    table = html.find_all('table')[12]
    job_start_at = table.contents[1].find_all('span')[1].contents[0]

    table = html.find_all('table')[15]
    try:
        job_title = table.contents[1].find_all('span')[0].contents[0]
        if job_title == u'אחר':
            raise Exception
    except:
        job_title = table.contents[1].find('textarea').contents[0]

    print job_start_at, job_title

    table = html.find_all('table')[16]
    academic_background = get_academic_background(table)

    table = html.find_all('table')[18]
    prior_jobs = get_prior_jobs(table, html)

"""
90, 307
company name
report num 
date published
fullname
job title
job_start_date
"""


def template_090(args):
    html, year = args
    publish_date = get_publish_date(html)

    fullname, table = get_fullname(html, 3)

    job_title = table.contents[1].find_all('span')[0].contents[0].replace(':', '').replace('1.', '')[3:]

    job_start_at = table.contents[3].find_all('span')[1].contents[0]

    print job_title, job_start_at


def tempalte_307(args):
    html, year = args
    publish_date = get_publish_date(html)

    fullname, table = get_fullname(html, 4)

    job_title = table.contents[1].find_all('span')[0].contents[0].replace(':', '').replace('1.', '')[3:]
    table = html.find_all('table')[5]
    job_start_at = table.contents[1].find_all('span')[1].contents[0]

    print job_title, job_start_at

