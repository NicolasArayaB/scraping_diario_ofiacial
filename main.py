from bs4 import BeautifulSoup
import requests
import re
import os

# Url date & edition changes and if there is any second edition, append extension -B
edition = 42924
day = 8
month = 4
year = 2021

for i in range(2):
    url = f'https://www.diariooficial.interior.gob.cl/edicionelectronica/empresas_cooperativas.php?date={str(day).zfill(2)}-{str(month).zfill(2)}-{year}&edition={edition}'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    if soup.find('p', class_='nofound'):
        day = day + 1
    else:
        path = f'Files/{edition}'
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)

        container = soup.find('div', class_='wrapsection')
        #anchor = container.find('a', attrs={'href': re.compile("^http://")})
        for anchor in container.find_all('a', attrs={'href': re.compile("^http://")}, limit=3):
            file_url = anchor.get('href')
            file_name = anchor.text.split(" ")[2].replace("(", "").replace(")", "")
            r = requests.get(file_url)
            with open(f'{path}/{file_name}.pdf', "wb") as file:
                file.write(r.content)
            print(file_name)
        edition = edition + 1
        day = day + 1

#  to download all files, replace line 20 with this and indent
#for anchor in soup.find_all('a', attrs={'href': re.compile("^http://")}):

