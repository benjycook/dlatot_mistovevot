from DirectorReportExtractor import DirectorReportExtractor
from carriers_urls import carriers_urls
import time
import csv

FOLDER_TO_SAVE = r''

def main():
    for url in carriers_urls.carriers_urls:
        #URL = 'http://mayafiles.tase.co.il/RHtm/1102001-1103000/H1102772.htm'
        b1 = DirectorReportExtractor(url)
        if b1.can_extract():
            b1.extract()
            filename = FOLDER_TO_SAVE = os.path.basename(url)[:-3]+'csv'
            with open(filename,'wb') as f:
                writer = csv.DictWriter(f, ['hebrew_name','english_passport_name','from_date','to_date',
                    'creation_date','publishment_date','document_type','organization','position',
                    'passport_hash','id_hash','url'])
                writer.writeheader()
                for i in b1.results:
                    writer.writerow(i)
        else:
            print "URL is not in the right format: {}".format(url)
        time.sleep(1)

if __name__ == '__main__':
    main()