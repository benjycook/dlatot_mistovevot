from BaseHtmlDataExtractor import BaseHtmlDataExtractor
import datetime

class DirectorReportExtractor(BaseHtmlDataExtractor):
    _TABLE_NAME = 'tblNames1'
    _ROW_CLASS_NAME = 'clsFirstRow'
    _APPLIED_FIELDS_DICT = {\
                        'hebrew_name' : 'Row{row}Field4' , \
                        'english_passport_name' : 'Row{row}Field11' , \
                        'from_date' : 'Row{row}Field34' , \
                        'to_date' : 'Row{row}Field36' , \
                        }
    PUBLISHMENT_DATE_TEMPLATE = 'NewField3'
    PASSPORT_ID_TEMPLATE = 'Row{row}Field9'
    PASSPORT_TYPE_TEMPLATE = 'Row{row}Field6'
    ORGANIZATION_ID_TEMPLATE = 'HeaderEntityNameEB'
    POSITION_TEMPLATE = 'Row{row}NewField10'
    POSITION_TEMPLATE_2 = 'Row{row}NewField1'
    TITLE_TEMPLATE = 'Field1'
    EXCLUDE_POSITIONS = [u'\u05D0\u05D7\u05E8']
    _NOT_TO_DICT =      { \
                        'is_financial_expert' : 'Row{row}Field13' , \
                        'is_inspection_comitee' : 'Row{row}Field15' , \
                        'is_of_the_audit_committee' : 'Row{row}Field28' , \
                        'compensation_committee' : 'Row{row}Field40' , \
                        'other_committees' : 'Row{row}Field30' \
                        }

    def extract(self):
        num_of_elements = self._get_number_of_elements_by_class_name(self._TABLE_NAME,self._ROW_CLASS_NAME)
        creation_date = datetime.datetime.strftime(datetime.datetime.now(),self.DATE_FORMAT)
        publishment_date = self._get_value_form_field_id(self.PUBLISHMENT_DATE_TEMPLATE)
        self.results = []
        for i in range(num_of_elements):
            row_dict = {}
            for f in self._APPLIED_FIELDS_DICT:
                value = self._get_value_from_row_field(self._APPLIED_FIELDS_DICT[f], i)
                row_dict[f] = value.encode('utf-8') if value else None
            row_dict['creation_date'] = creation_date
            row_dict['publishment_date'] = publishment_date
            row_dict['document_type'] = 'carriers'
            row_dict['url'] = self.url
            row_dict['organization'] = self._get_value_form_field_id(self.ORGANIZATION_ID_TEMPLATE).encode('utf-8')
            passport_value = self._get_value_from_row_field(self.PASSPORT_ID_TEMPLATE, i)
            passport_type = self._get_value_from_row_field(self.PASSPORT_TYPE_TEMPLATE, i)
            self._fill_identification(row_dict,passport_type,passport_value)
            position_main = self._get_value_from_row_field(self.POSITION_TEMPLATE, i)
            position_sub = self._get_value_from_row_field(self.POSITION_TEMPLATE_2, i)
            self._fill_position(row_dict, position_main, position_sub)
            self.results.append(row_dict)

    def _fill_date(self, row_dict, date_1, date_2):
        if not '___' in date_1:
            row_dict['from_date'] = date_1.encode('utf-8')
        elif not '___' in date_2:
            row_dict['from_date'] = date_2.encode('utf-8')
        else:
            row_dict['from_date'] = None

    def _fill_position(self, row_dict, first_position, second_position):
        if first_position in self.EXCLUDE_POSITIONS:
            row_dict['position'] = second_position.encode('utf-8')
        else:
            row_dict['position'] = first_position.encode('utf-8')

    def can_extract(self):
        print self._get_value_form_field_id(self.TITLE_TEMPLATE).encode('utf-8')
        return self._get_value_form_field_id(self.TITLE_TEMPLATE) == '\u05d3\u05d5\u05d7 \u05de\u05d9\u05d9\u05d3\u05d9 \u05e2\u05dc \u05de\u05e6\u05d1\u05ea \u05e0\u05d5\u05e9\u05d0\u05d9 \u05de\u05e9\u05e8\u05d4 \u05d1\u05db\u05d9\u05e8\u05d4 '
