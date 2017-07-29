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
# -*- coding: utf-8 -*-

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


def get_job_details(html, table_num, start_ind, title_ind, prior_ind):
    table = html.find_all('table')[table_num]
    try:
        job_start_at = table.contents[start_ind].find_all('span')[2].contents[0]
    except:
        job_start_at = table.contents[start_ind].find_all('span')[1].contents[0]

    try:
        job_title = table.contents[title_ind].find_all('span')[0].contents[0]
    except:
        job_title = table.contents[title_ind].find('textarea').contents[0]
    if prior_ind:
        prior_job = table.contents[prior_ind].find('span', {'id': 'Row0NewField21'}).contents[0]
    else:
        prior_job = '---'
    print job_title, job_start_at, prior_job
    return job_title, job_start_at, prior_job

def template_091_type_a(html):
    publish_date  = get_publish_date(html)

    fullname, table = get_fullname(html, 4)

    identifier_type, identifier_num = get_identifier_type(table, 5, 7)

    citizenship = table.contents[9].find_all('span')[1].contents[0]

    birth_date = get_birthday(html, 5)

    job_title, job_start_at, prior_job_here = get_job_details(html, 4, 17, 21, 27)


    academic_background = [
        (item.find_all('span')[0].contents[0], item.find_all('span')[1].contents[0], item.find('textarea').contents[0])
        for item in table4.contents[31].find_all('table')[1].find_all('tr')]

    for i in academic_background:
        for j in i:
            print j

    prior_jobs_last_5 = [
        (item.find_all('textarea')[0].contents[0], item.find_all('textarea')[1].contents[0], item.find_all('textarea')[2].contents[0])
        for item in table4.contents[39].find_all('table')[1].find_all('tr')]

    for i in prior_jobs_last_5:
        for j in i:
            print j


def template_091_type_b(html):
    publish_date = get_publish_date(html)

    fullname, table = get_fullname(html, 3)

    identifier_type, identifier_num = get_identifier_type(table, 3 ,5)

    citizenship = table.contents[7].find_all('span')[1].contents[0]

    birth_date = get_birthday(html, 5)

    job_title, job_start_at, prior_job_here = get_job_details(html, 3, 15, 19, 0)

    try:
        academic_background = [
            (item.find_all('span')[0].contents[0], item.find_all('span')[1].contents[0], item.find('textarea').contents[0])
            for item in table.contents[23].find_all('table')[1].find_all('tr')]

        for i in academic_background:
            for j in i:
                print j

        prior_jobs_last_5 = [
            (item.find_all('textarea')[0].contents[0], item.find_all('textarea')[1].contents[0],
             item.find_all('textarea')[2].contents[0])
            for item in table.contents[31].find_all('table')[1].find_all('tr')]

        for i in prior_jobs_last_5:
            for j in i:
                print j
    except:
        academic_background = [
            (item.find_all('span')[0].contents[0], item.find_all('span')[1].contents[0],
             item.find('textarea').contents[0])
            for item in table.contents[27].find_all('table')[1].find_all('tr')]

        for i in academic_background:
            for j in i:
                print j

        prior_jobs_last_5 = [
            (item.find_all('textarea')[0].contents[0], item.find_all('textarea')[1].contents[0],
             item.find_all('textarea')[2].contents[0])
            for item in table.contents[35].find_all('table')[1].find_all('tr')]

        for i in prior_jobs_last_5:
            for j in i:
                print j

def template_091(args):
    html, year = args
    if year in ['2008', '2011', '2012']:
        template_091_type_a(html)
    elif year in ['2004', '2005', '2006', '2007', '2017']:
        template_091_type_b(html)
    else:
        pass


def template_093(x):
    pass

def tempalte_304(args):
    html, year = args
    publish_date = get_publish_date(html)

    fullname, table = get_fullname(html, 5)

    identifier_type, identifier_num = get_identifier_type(table, 1, 1)

    citizenship = table.contents[1].find_all('span')[6].contents[0]

    birth_date = get_birthday(html, 12)

    job_title, job_start_at, prior_job_here = get_job_details(html, 3, 25, 11, 0)


    academic_background = [
        (item.find_all('span')[0].contents[0], item.find_all('span')[1].contents[0], item.find('textarea').contents[0])
        for item in table4.contents[31].find_all('table')[1].find_all('tr')]

    for i in academic_background:
        for j in i:
            print j

    prior_jobs_last_5 = [
        (item.find_all('textarea')[0].contents[0], item.find_all('textarea')[1].contents[0], item.find_all('textarea')[2].contents[0])
        for item in table4.contents[39].find_all('table')[1].find_all('tr')]

    for i in prior_jobs_last_5:
        for j in i:
            print j


def tempalte_306(x):
    pass

"""
90, 307
company name
report num 
date published
fullname
job title
job_start_date
"""


def template_090(x):
    pass
def tempalte_307(x):
    pass

