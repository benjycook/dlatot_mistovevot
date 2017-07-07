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


def template_091_type_a(html):

    table0 = html.find_all('table')[0]
    publish_date = table0.contents[1].find('span', {'id': 'HeaderSendDate'}).parent.contents[-1]
    publish_date = publish_date.replace(u'\r\n\t\t\t\t', '').replace(u'\t\r\n\t\t\t', '')
    print publish_date
    table4 = html.find_all('table')[4]
    fullname = table4.contents[1].find('textarea').contents[0]
    print fullname
    identifier_type = table4.contents[5].find_all('span')[1].contents[0]
    print identifier_type
    identifier_num = table4.contents[7].find_all('span')[1].contents[0]
    print identifier_num
    citizenship = table4.contents[9].find_all('span')[1].contents[0]
    print citizenship
    birth_date = table4.contents[13].find_all('span')[2].contents[0]
    print birth_date
    job_start_at = table4.contents[17].find_all('span')[2].contents[0]
    print job_start_at
    job_title = table4.contents[21].find('textarea').contents[0]
    print job_title
    prior_job_here = table4.contents[27].find('span', {'id': 'Row0NewField21'}).contents[0]
    print prior_job_here

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
    table0 = html.find_all('table')[0]
    publish_date = table0.contents[1].find('span', {'id': 'HeaderSendDate'}).parent.contents[-1]
    publish_date = publish_date.replace(u'\r\n\t\t\t\t', '').replace(u'\t\r\n\t\t\t', '')
    print publish_date
    table3 = html.find_all('table')[3]
    fullname = table3.contents[1].find('textarea').contents[0]
    print fullname
    identifier_type = table3.contents[3].find_all('span')[1].contents[0]
    print identifier_type
    identifier_num = table3.contents[5].find_all('span')[1].contents[0]
    print identifier_num
    citizenship = table3.contents[7].find_all('span')[1].contents[0]
    print citizenship
    birth_date = table3.contents[11].find_all('span')[2].contents[0]
    print birth_date
    job_start_at = table3.contents[15].find_all('span')[2].contents[0]
    print job_start_at
    job_title = table3.contents[19].find('textarea').contents[0]
    print job_title
    prior_job_here = '---'
    print prior_job_here
    try:
        academic_background = [
            (item.find_all('span')[0].contents[0], item.find_all('span')[1].contents[0], item.find('textarea').contents[0])
            for item in table3.contents[23].find_all('table')[1].find_all('tr')]

        for i in academic_background:
            for j in i:
                print j

        prior_jobs_last_5 = [
            (item.find_all('textarea')[0].contents[0], item.find_all('textarea')[1].contents[0],
             item.find_all('textarea')[2].contents[0])
            for item in table3.contents[31].find_all('table')[1].find_all('tr')]

        for i in prior_jobs_last_5:
            for j in i:
                print j
    except:
        academic_background = [
            (item.find_all('span')[0].contents[0], item.find_all('span')[1].contents[0],
             item.find('textarea').contents[0])
            for item in table3.contents[27].find_all('table')[1].find_all('tr')]

        for i in academic_background:
            for j in i:
                print j

        prior_jobs_last_5 = [
            (item.find_all('textarea')[0].contents[0], item.find_all('textarea')[1].contents[0],
             item.find_all('textarea')[2].contents[0])
            for item in table3.contents[35].find_all('table')[1].find_all('tr')]

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

def tempalte_304(x):
    pass

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

