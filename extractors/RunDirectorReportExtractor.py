# -*- coding: utf-8 -*-

from DirectorReportExtractor import DirectorReportExtractor
from carriers_urls import carriers_urls
import time
import csv
import sys
import os
import pandas as pd

FOLDER_TO_SAVE = r''

def get_urls(argv):
    action = argv[1]
    year = argv[2]
    filename = os.path.dirname(os.getcwd())+'{}{}_{}.{}'.format('/data/scraped_data/',action,year,'csv')
    df = pd.read_csv(filename)
    urls = df.html_link
    return urls[:5]

def main(argv):
    for url in get_urls(argv):
        #URL = 'http://mayafiles.tase.co.il/RHtm/1102001-1103000/H1102772.htm'
        b1 = DirectorReportExtractor(url)
        if b1.can_extract():
            b1.extract()
            print (b1.results)
            # filename = FOLDER_TO_SAVE = os.path.basename(url)[:-3]+'csv'
            # with open(filename,'wb') as f:
            #     writer = csv.DictWriter(f, ['hebrew_name','english_passport_name','from_date','to_date',
            #         'creation_date','publishment_date','document_type','organization','position',
            #         'passport_hash','id_hash','url'])
            #     writer.writeheader()
            #     for i in b1.results:
            #         writer.writerow(i)
        else:
            print ("URL is not in the right format: {}".format(url))
        time.sleep(1)

if __name__ == '__main__':
    a = ['','carriers', '2004']
    main(a)