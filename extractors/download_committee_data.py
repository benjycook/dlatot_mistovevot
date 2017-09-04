import requests
import bs4
from time import sleep
import os
from tqdm import tqdm
import pathlib

base_dir = os.getcwd()+'/data/committees_parsed/{type}/{committee_id}/'
base_url = 'https://knesset-data-pipelines.uumpa.net/data/'

#  connect to https://knesset-data-pipelines.uumpa.net/data/committee-meeting-protocols/ and get all committee ids
protocols_url = 'committee-meeting-protocols-parsed/{committee_id}/{meeting_id_file}'
req = requests.get(base_url+protocols_url.format(committee_id='', meeting_id_file=''))
parsed_content = bs4.BeautifulSoup(req.text, 'lxml')
committee_ids = [a['href'][:-1] for a in parsed_content.find_all('a') if a['href'][:-1].isdigit()]

for cid in committee_ids:
    try:
        pathlib.Path(base_dir.format(type='csv', committee_id=cid)).mkdir(parents=True)
        pathlib.Path(base_dir.format(type='txt', committee_id=cid)).mkdir(parents=True)
        req = requests.get(base_url + protocols_url.format(committee_id=cid, meeting_id_file=''))
        parsed_content = bs4.BeautifulSoup(req.text, 'lxml')
        meetings = [a['href'] for a in parsed_content.find_all('a')
                       if a['href'].split('.')[0].isdigit()]
        # download all links
        for meeting_link in tqdm(meetings):
            url = base_url + protocols_url.format(committee_id=cid, meeting_id_file=meeting_link)
            save_path = base_dir.format(type=meeting_link.split('.')[1], committee_id=cid)+meeting_link
            doc = requests.get(url)
            with open(save_path, 'w') as f:
                f.write(doc.content)
            sleep(0.5)
    except Exception as e:
        print e
        print('downloading committee id {} faild'.format(cid))
    sleep(1)
