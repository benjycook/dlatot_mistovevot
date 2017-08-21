# -*- coding: utf-8 -*-

import sqlite3
from openpyxl import load_workbook
from tqdm import tqdm

sqlite_db_file = 'dlatot_db.sqlite'

conn = sqlite3.connect(sqlite_db_file)
cur = conn.cursor()

drop_if_exists = """
    DROP TABLE IF EXISTS {tbl}
    """

create_tbl = """
    CREATE TABLE {tbl}
    ({f1} {type1} PRIMARY KEY,
     {f2} {type2}
     )
    """

person_table = create_tbl.format(tbl='persons',
                                 f1='person_id', type1='INTEGER',
                                 f2='fullname', type2='NVARCHAR')

job_title_table = create_tbl.format(tbl='jobs',
                                    f1='job_id', type1='INTEGER',
                                    f2='job_desc', type2='NVARCHAR')

companies_table = create_tbl.format(tbl='companies',
                                    f1='company_id', type1='INTEGER',
                                    f2='company_name', type2='NVARCHAR')

pjc_table = """
    CREATE TABLE {tbl} 
    ({f1} {type1},
     {f2} {type1},
     {f3} {type1},
     {f4} {type2},
     {f5} {type2}
     )
    """.format(tbl='person_job_company',
               f1='person_id', type1='INTEGER',
               f2='job_id',
               f3='company_id',
               f4='start_date',
               f5='end_date', type2='TEXT'
               )

# create tables
cur.execute(drop_if_exists.format(tbl='persons'))
cur.execute(person_table)
cur.execute(drop_if_exists.format(tbl='jobs'))
cur.execute(job_title_table)
cur.execute(drop_if_exists.format(tbl='companies'))
cur.execute(companies_table)
cur.execute(drop_if_exists.format(tbl='person_job_company'))
cur.execute(pjc_table)

persons = []
jobs = []
companies = []

pjcs = []

filename = 'extractors/results/appointments_{year}.xlsx'
for year in range(2004, 2018):
    print year
    f = filename.format(year=year)
    wb = load_workbook(f)
    ws = wb[str(year)]
    rows = [row for row in ws]
    rows.pop(0)
    for row in rows:
        # tofes = unicode(row[7].value)
        # if tofes in [u'ת307', u'ת090']:
        #     continue
        fullname = unicode(row[0].value).replace(u'"', u'').replace(u"'", u'')
        job = unicode(row[1].value).replace(u'"', u'').replace(u"'", u'')
        if job == u'אחר':
            job = unicode(row[2].value).replace(u'"', u'').replace(u"'", u'')

        company = unicode(row[4].value).replace(u'"', u'').replace(u"'", u'')
        start_date = row[3].value
        end_date = None
        if fullname not in persons:
            persons.append(fullname)
        if job not in jobs:
            jobs.append(job)
        if company not in companies:
            companies.append(company)
        pjcs.append((fullname, job, company, start_date, end_date))


data = {
    'persons': persons,
    'jobs': jobs,
    'companies': companies
}

insert = u"""
    INSERT INTO {tbl} VALUES (?,?)
    """

for tbl in data.keys():
    d = [(x, i) for x, i in enumerate(data[tbl])]
    cur.executemany(insert.format(tbl=tbl), d)
    conn.commit()
    print 'inserted {x} lines into {tbl}'.format(x=len(d), tbl=tbl)

insert_pjc = u"""
    INSERT INTO person_job_company 
    VALUES (
    (select person_id from persons where fullname like "{fullname}"),
    (select job_id from jobs where job_desc like '{job}'),
    (select company_id from companies where company_name like '{company}'),
    '{start}', {end})
    """

for pjc in tqdm(pjcs):
    fullname = pjc[0]
    job = pjc[1]
    company = pjc[2]
    start = pjc[3]
    end = 'NULL'
    cur.execute(insert_pjc.format(fullname=fullname,
                                  job=job,
                                  company=company,
                                  start=start,
                                  end=end))

conn.commit()
print 'the end!'

