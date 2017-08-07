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
import requests
from bs4 import BeautifulSoup



class Tofes(object):
    def __init__(self, link_info):

        self._type1_reports = [u'ת091', u'ת093', u'ת304', u'ת306']
        self._type2_reports = [u'ת090', u'ת307']

        self._action_title = link_info['action']
        self._company_name = link_info['company_name']
        self._maya_link = link_info['maya_link']
        self._tofes_link = link_info['tofes_link']
        self._status = True

        self._html = None
        self.html = None

        self._report_num = None
        self.report_num = None

        self._date_published = None
        self.date_published = None

        self._fullname = None
        self.fullname = None

        self._job_title = None
        self.job_title = None

        self._job_desc = None
        self.job_desc = None

        self._starting_date = None
        self.starting_date = None

        self._education = None
        self.education = None

        self._prior_jobs = None
        self.prior_jobs = None

    @property
    def status(self):
        return self._status

    @property
    def html(self):
        return self._html

    @html.setter
    def html(self, value):
        if value is None:
            res = requests.get(self._tofes_link)

            if res.status_code != 200:
                print(res.status_code)
                self._status = False
            else:
                page_text = res.content
                self._html = BeautifulSoup(page_text, 'html.parser')
        else:
            self._html = value

    @property
    def report_num(self):
        return self._report_num

    @report_num.setter
    def report_num(self, value):
        if value is None:
            self._report_num = self._html.find('span', {'fieldalias': 'MisparTofes'}).contents[0]
        else:
            self._report_num = value

    @property
    def date_published(self):
        return self._date_published

    @date_published.setter
    def date_published(self, value):
        if value is None:
            self._date_published = self._html.find('span', {'fieldalias': 'HeaderSendDate'}).parent.contents[-1]\
                                                        .replace('\r', '').replace('\n', '').replace('\t', '')
        else:
            self._date_published = value

    @property
    def fullname(self):
        return self._fullname

    @fullname.setter
    def fullname(self, value):
        if self._report_num not in self._type1_reports+self._type2_reports:
            self._fullname = None
        elif value is None:
            for shem in ['Shem', 'ShemPratiVeMishpacha', 'ShemPriatiVeMishpacha', 'ShemMishpahaVePrati',
                         'ShemRoeCheshbon', 'ShemRoehHeshbon']:
                try:
                    self._fullname = self._html.find('textarea', {'fieldalias': shem}).contents[0]
                    break
                except:
                    pass
        else:
            self._fullname = value

    @property
    def job_title(self):
        return self._job_title

    @job_title.setter
    def job_title(self, value):
        if self.report_num in self._type2_reports:
            self._job_title = u'רואה חשבון'
        elif self._report_num not in self._type1_reports:
            self._job_title = None
        elif value is None:
            job_titles = ['Tafkid', 'Misra', 'HaTafkidLoMuna']
            for job_ttl in job_titles:
                try:
                    self._job_title = self._html.find('span', {'fieldalias': job_ttl}).contents[0]
                    break
                except:
                    pass
        else:
            self._job_title = value

    @property
    def job_desc(self):
        return self._job_desc

    @job_desc.setter
    def job_desc(self, value):
        if self.report_num in [u'ת090', u'ת307']:
            self._job_desc = u''
        elif self._report_num not in self._type1_reports:
            self._job_desc = None
        elif value is None:
            job_descs = ['TeurTafkid', 'LeloTeur', 'TeurHaTafkidLoMuna']
            for desc in job_descs:
                try:
                    self._job_desc = self._html.find('textarea', {'fieldalias': desc}).contents[0]
                    break
                except:
                    pass
        else:
            self._job_desc = value

    @property
    def starting_date(self):
        return self._job_desc

    @starting_date.setter
    def starting_date(self, value):
        if self._report_num not in self._type1_reports+self._type2_reports:
            self._starting_date = None
        elif value is None:
            starting_dates = ['TaarichTchilatHaCehuna', 'TaarichTchilatCehuna', 'TaarichTehilatCehuna',
                              'TaarichTchilatHaKehuna', 'TaarichTchilatKehuna', 'TaarichTehilatKehuna']
            for date in starting_dates:
                try:
                    self._starting_date = self._html.find('span', {'fieldalias': date}).contents[0]
                    break
                except:
                    pass
        else:
            self._starting_date = value

    @property
    def education(self):
        return self._education

    @education.setter
    def education(self, value):
        if self._report_num not in self._type1_reports+self._type2_reports:
            self._education = []
        elif value is None:
            education = ['Toar', 'ToarAcademi']
            kind = ['Tehum', 'Tchum']
            institute = ['ShemHamosadHaakademi', 'ShemHamosadHaacademi', 'ShemHaMosadHaAkademi', 'ShemHaMosadHaAcademi',
                         'ShemMosadAcademy', 'ShemMosadAcademi', 'ShemMosadAkademi', 'ShemMosadAkademy',
                         'ShemHamosadHaakademy', 'ShemHamosadHaacademy', 'ShemHaMosadHaAkademy', 'ShemHaMosadHaAcademy']
            degrees = []
            for ed in education:
                try:
                    toars = self._html.find_all('span', {'fieldalias': ed})
                    for x, t in enumerate(toars):
                        toar = t.contents[0]
                        toar_type = ''
                        for k in kind:
                            for tag in ['span', 'textarea']:
                                try:
                                    toar_type = self._html.find_all(tag, {'fieldalias': k})[x].contents[0]
                                except:
                                    pass
                        mosad = ''
                        for i in institute:
                            try:
                                mosad = self._html.find_all('textarea', {'fieldalias': i})[x].contents[0]
                            except:
                                pass
                        degrees.append((toar, toar_type, mosad))
                except:
                    pass
            self._education = degrees
        else:

            self._education = value if type(value) is list else [value]

    @property
    def prior_jobs(self):
        return self._education

    @prior_jobs.setter
    def prior_jobs(self, value):
        if self._report_num not in self._type1_reports + self._type2_reports:
            self._prior_jobs = []
        elif value is None:
            job_titles = ['Tapkid', 'HaTafkidSheMila', 'Tafkid']
            job_places = ['MekomHaAvoda', 'MekomAvoda', 'MekomAvodah']
            job_periods = ['MeshechZmanSheMilaBaTafkid', 'MeshechZman', 'MeshechHaZmanSheMilaTafkid']
            jobs = []
            for job in job_titles:
                try:
                    prior_jobs = self._html.find_all('textarea', {'fieldalias': job})
                    for x, prior in enumerate(prior_jobs):
                        job = prior.contents[0]
                        job_place = ''
                        for p in job_places:
                            for tag in ['span', 'textarea']:
                                try:
                                    job_place = self._html.find_all(tag, {'fieldalias': p})[x].contents[0]
                                except:
                                    pass
                        job_period = ''
                        for z in job_periods:
                            for tag in ['span', 'textarea']:
                                try:
                                    job_period = self._html.find_all(tag, {'fieldalias': z})[x].contents[0]
                                except:
                                    pass

                        jobs.append((job, job_place, job_period))
                except:
                    pass
            self._prior_jobs = jobs
        else:

            self._prior_jobs = value if type(value) is list else [value]

def extras(html):

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






