# coding: utf-8

from selenium import webdriver
import datetime
import pandas as pd


THE_MARKER_URL = 'http://www.themarker.com/career/1.2577328'
driver = webdriver.Firefox()
nom_df = pd.DataFrame(columns=['Date','Name','Position','Company','Description'])

driver.get(THE_MARKER_URL)

nominations = driver.find_elements_by_class_name("miny_item")
index = 0
for nom in nominations:
    if nom.find_element_by_class_name('date_txt').text:
        date = nom.find_element_by_class_name('date_txt').text
    else:
        date = ''
    new_line = pd.Series({
            'Date':        date,
            'Name':        nom.find_element_by_class_name('minuy_name').text,
            'Position':    nom.find_element_by_class_name('title').text.split('\n')[0],
            'Company':     nom.find_element_by_class_name('company').text,
            'Description': nom.find_element_by_class_name('details').text,
    })
nom_df.loc[index] = new_line
index += 1
nom_df['Source'] = THE_MARKER_URL


nom_df.to_csv("TheMarker.csv")

driver.close()