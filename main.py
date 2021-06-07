from bs4 import BeautifulSoup
import requests
import re

# Url date & edition changes and if there is any second edition, append extension -B
edition = 42924
day = 8
month = 4
year = 2021

for i in range(5):
    url = f'https://www.diariooficial.interior.gob.cl/edicionelectronica/empresas_cooperativas.php?date={str(day).zfill(2)}-{str(month).zfill(2)}-{year}&edition={edition}'

    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    if soup.find('p', class_='nofound'):
        day = day + 1
    else:
        anchor = soup.find('a', attrs={'href': re.compile("^http://")})
        file_url = anchor.get('href')
        file_name = anchor.text.split(" ")[2].replace("(", "").replace(")", "")
        r = requests.get(file_url)
        with open(f'Files/{file_name}.pdf', "wb") as file:
            file.write(r.content)
        edition = edition + 1
        day = day + 1

# Download all files
#for anchor in soup.find_all('a', attrs={'href': re.compile("^http://")}):
#    file_url = anchor.get('href')
#    file_name = anchor.text.split(" ")[2].replace("(", "").replace(")", "")
#    r = request.get(file_url)

#    with open(f'Files/{file_name}.pdf', "wb") as file:
#       file.write(r.content)
#    edition = edition + 1
#    day = day + 1
