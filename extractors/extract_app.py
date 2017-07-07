# -*- coding: utf-8 -*-
import copy
import datetime
import hashlib
from abc import abstractmethod
import time

import requests
from bs4 import BeautifulSoup
import pandas as pd
# import urls
import os


class BaseHtmlDataExtractor(object):
    DATE_FORMAT = '%d-%m-%y'
    ID_INDICATORS = [u'\u05e1\u05d5\u05d2 \u05de\u05e1\u05e4\u05e8 \u05d6\u05d9\u05d4\u05d5\u05d9: ',
                     u'\u05de\u05e1\u05e4\u05e8 \u05ea.\u05d6.']

    def __init__(self, html_text):
        self.soup = BeautifulSoup(html_text, 'html.parser')

    @staticmethod
    def sha256(text):
        hasher = hashlib.sha256()
        hasher.update(text)
        return hasher.hexdigest()

    def _get_value_from_row_field(self, field_template, row):
        element_id = field_template.format(row=row)
        elements = self.soup.find_all(id=element_id)
        return elements[0].text

    def _get_value_form_field_id(self, field_id):
        elements = self.soup.find_all(id=field_id)
        if not elements:
            return None
        return elements[0].text

    def fill_identification(self, doc_info, identification_type, identification_number):
        if identification_type == u'\u05de\u05e1\u05e4\u05e8 \u05d3\u05e8\u05db\u05d5\u05df':  # 'מספר דרכון':
            doc_info['passport_hash'] = self.sha256(identification_number)
            doc_info['id_hash'] = None
        elif identification_type in self.ID_INDICATORS:  # מספר ת.ז.
            doc_info['passport_hash'] = None
            doc_info['id_hash'] = self.sha256(identification_number)
        else:
            raise Exception('not implement for {} identification_type'.format(identification_type))

    def get_number_of_elements_by_class_name(self, container_id, class_name):
        table = self.soup.find_all(id=container_id)[0]
        return len(table.findAll(attrs={'class': class_name}))

    @abstractmethod
    def extract(self):
        pass


class AppointmentExtractor(BaseHtmlDataExtractor):
    PROP_NAME_TO_FIELD_ID = {
        'heb_name': 'HeaderFormSubject',
        'eng_passport_name': 'Field89',
        'identification_type': 'Field6',
        'identification_number': 'Field8',
    }

    MAIN_JOBS_NAME_TO_FIELD_TEMPLATE = {
        'job_name': 'Row{row}Field44'
    }
    JOBS_PROP_NAME_TO_FIELD_TEMPLATE = {
        'job_name': 'Row{row}Field44'
    }

    def extract(self):
        title = self._get_value_form_field_id('Field1')
        print (title)
        # דוח מיידי על מינוי דירקטור (שאינו תאגיד) או יחיד המכהן מטעם תאגיד שהוא דירקטור בחברה פרטית
        # if title != u'\u05d3\u05d5\u05d7 \u05de\u05d9\u05d9\u05d3\u05d9 \u05e2\u05dc \u05de\u05d9\u05e0\u05d5\u05d9 \u05d3\u05d9\u05e8\u05e7\u05d8\u05d5\u05e8 (\u05e9\u05d0\u05d9\u05e0\u05d5 \u05ea\u05d0\u05d2\u05d9\u05d3) \u05d0\u05d5 \u05d9\u05d7\u05d9\u05d3 \u05d4\u05de\u05db\u05d4\u05df \u05de\u05d8\u05e2\u05dd \u05ea\u05d0\u05d2\u05d9\u05d3 \u05e9\u05d4\u05d5\u05d0 \u05d3\u05d9\u05e8\u05e7\u05d8\u05d5\u05e8 \u05d1\u05d7\u05d1\u05e8\u05d4 \u05e4\u05e8\u05d8\u05d9\u05ea ':
        #     return None
        rows = []
        row_base = {'source': 'mayafiles.tase',
                    'document_type': 'appointment',
                    'create_date': datetime.datetime.now().strftime(self.DATE_FORMAT),
                    'heb_name': self._get_value_form_field_id('HeaderFormSubject'),
                    'eng_passport_name': self._get_value_form_field_id('Field89'),
                    'from_date': None,
                    'to_date': None,
                    }
        identification_type = self._get_value_form_field_id('Field6')
        identification_number = self._get_value_form_field_id('Field8')
        self.fill_identification(row_base, identification_type, identification_number)
        for row in range(self.get_number_of_elements_by_class_name('Table3', 'clsFirstRow')):
            new_row = copy.copy(row_base)
            new_row['job'] = self._get_value_from_row_field('Row{row}Field45', row)
            new_row['job_position'] = self._get_value_from_row_field('Row{row}Field44', row)
            rows.append(new_row)
        return rows

def get_urls(argv):
    action = argv[1]
    year = argv[2]
    filename = os.path.dirname(os.getcwd())+'{}{}_{}.{}'.format('/data/scraped_data/',action,year,'csv')
    df = pd.read_csv(filename)
    urls = df.html_link
    return urls[:15]

for url in get_urls(['', 'appointment', '2004']):#urls.moshe_urls:
    page = requests.get(url).content
    doc_info = AppointmentExtractor(page).extract()
    print(doc_info)
    time.sleep(2)
