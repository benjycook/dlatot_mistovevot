# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from abc import abstractmethod
import hashlib

class BaseHtmlDataExtractor(object):
    DATE_FORMAT = '%d-%m-%Y'
    ID_INDICATORS = [u'\u05e1\u05d5\u05d2 \u05de\u05e1\u05e4\u05e8 \u05d6\u05d9\u05d4\u05d5\u05d9: ',\
                     u'\u05de\u05e1\u05e4\u05e8 \u05ea.\u05d6.',\
                     u'\u05de\u05e1\u05e4\u05e8 \u05ea\u05e2\u05d5\u05d3\u05ea \u05d6\u05d4\u05d5\u05ea']  # Only Teudat Zehut

    def __init__(self, url, extracted_html_text=None):
        self.url = url
        if not extracted_html_text:
            extracted_html_text = requests.get(url).content
        self.soup = BeautifulSoup(extracted_html_text, 'html.parser')

    @staticmethod
    def sha256(text):
        hasher = hashlib.sha256()
        hasher.update(text)
        return hasher.hexdigest()

    def _get_value_from_row_field(self, field_template, row):
        element_id = field_template.format(row=row)
        return self._get_value_form_field_id(element_id)

    def _get_value_form_field_id(self, field_id):
        return self.soup.find_all(id=field_id)[0].text

    def _fill_identification(self, doc_info, identification_type, identification_number):
        if identification_type == u'\u05de\u05e1\u05e4\u05e8 \u05d3\u05e8\u05db\u05d5\u05df':  # Darkon ID
            doc_info['passport_hash'] = self.sha256(identification_number)
            doc_info['id_hash'] = None
        elif identification_type in self.ID_INDICATORS:  # Teudat Zehut ID
            doc_info['passport_hash'] = None
            doc_info['id_hash'] = self.sha256(identification_number)
        else:
            raise Exception('not implement for {} identification_type'.format \
                                (identification_type.encode('utf-8')))

    def _get_number_of_elements_by_class_name(self, container_id, class_name):
        table = self.soup.find_all(id=container_id)
        if table:
            return len(table[0].findAll(attrs={'class': class_name}))
        return None

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def can_extract(self):
        pass
