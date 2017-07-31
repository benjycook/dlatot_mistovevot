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


def type1(args):
    html, year = args

    report_num = html.find('span', {'fieldalias': 'MisparTofes'}).contents[0]
    print report_num

    date_publish = html.find('span', {'fieldalias': 'HeaderSendDate'}).parent.contents[-1]\
        .replace('\r', '').replace('\n', '').replace('\t', '')
    print date_publish

    for shem in ['Shem', 'ShemPratiVeMishpacha', 'ShemPriatiVeMishpacha',  'ShemMishpahaVePrati']:
        try:
            fullname = html.find('textarea', {'fieldalias': shem}).contents[0]
            break
        except:
            pass
    print fullname

    birth_date = html.find('span', {'fieldalias': 'TaarichLeida'}).contents[0]
    print birth_date

    mispar = ['MisparZihuy', 'MisparZihui']
    posts = ['1', '']
    for misparzihui in product(mispar, posts):
        query_num = ''.join(list(misparzihui))
        try:
            identifier_num = html.find('span', {'fieldalias': query_num}).contents[0]
            query_type = 'Sug{}'.format(query_num)
            identifier_type = html.find('span', {'fieldalias': query_type}).contents[0]
            break
        except:
            pass
    print identifier_type, identifier_num

    ezrachut = ['Ezrachut', 'EzrahutSlashEretz1', 'EzrahutSlashEretz']

    for ezrach in ezrachut:
        try:
            citizenship = html.find('span', {'fieldalias': ezrach}).contents[0]
            break
        except:
            pass
    print citizenship

    job_titles = ['Tafkid', 'Misra','HaTafkidLoMuna']
    for job_ttl in job_titles:
        try:
            job_title = html.find('span', {'fieldalias': job_ttl}).contents[0]
            break
        except:
            pass

    job_descs = ['TeurTafkid', 'LeloTeur','TeurHaTafkidLoMuna']
    for desc in job_descs:
        try:
            job_title_desc = html.find('textarea', {'fieldalias': desc}).contents[0]
            break
        except:
            pass

    print job_title
    print job_title_desc

    starting_dates = ['TaarichTchilatHaCehuna', 'TaarichTchilatCehuna', 'TaarichTehilatCehuna',
                      'TaarichTchilatHaKehuna', 'TaarichTchilatKehuna', 'TaarichTehilatKehuna']
    for date in starting_dates:
        try:
            job_starting_date = html.find('span', {'fieldalias': date}).contents[0]
            break
        except:
            pass

    print job_starting_date

    education = ['Toar','ToarAcademi']
    kind = ['Tehum', 'Tchum']
    institute = ['ShemHamosadHaakademi', 'ShemHamosadHaacademi','ShemHaMosadHaAkademi', 'ShemHaMosadHaAcademi',
                 'ShemMosadAcademy', 'ShemMosadAcademi', 'ShemMosadAkademi', 'ShemMosadAkademy',
                 'ShemHamosadHaakademy', 'ShemHamosadHaacademy','ShemHaMosadHaAkademy', 'ShemHaMosadHaAcademy']
    degrees = []
    for ed in education:
        try:
            toars = html.find_all('span', {'fieldalias': ed})
            for x,t in enumerate(toars):
                toar = t.contents[0]
                toar_type = ''
                for k in kind:
                    for tag in ['span', 'textarea']:
                        try:
                            toar_type = html.find_all(tag, {'fieldalias': k})[x].contents[0]
                        except:
                            pass
                mosad = ''
                for i in institute:
                    try:
                        mosad = html.find_all('textarea', {'fieldalias': i})[x].contents[0]
                    except:
                        pass
                degrees.append((toar, toar_type, mosad))
        except:
            pass

    for degree in degrees:
        print degree[0], degree[1], degree[2]

    job_titles = ['Tapkid', 'HaTafkidSheMila', 'Tafkid']
    job_places = ['MekomHaAvoda', 'MekomAvoda', 'MekomAvodah']
    job_periods = ['MeshechZmanSheMilaBaTafkid', 'MeshechZman','MeshechHaZmanSheMilaTafkid']
    jobs = []
    for job in job_titles:
        try:
            prior_jobs = html.find_all('textarea', {'fieldalias': job})
            for x, prior in enumerate(prior_jobs):
                job = prior.contents[0]
                job_place = ''
                for p in job_places:
                    for tag in ['span', 'textarea']:
                        try:
                            job_place = html.find_all(tag, {'fieldalias': p})[x].contents[0]
                        except:
                            pass
                job_period =''
                for z in job_periods:
                    for tag in ['span', 'textarea']:
                        try:
                            job_period = html.find_all(tag, {'fieldalias': z})[x].contents[0]
                        except:
                            pass

                jobs.append((job, job_place, job_period))
        except:
            pass

    for j in jobs:
        print j[0], j[1], j[2]




