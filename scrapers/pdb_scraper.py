from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

# importing the requests library
import requests
import json

for i in range(10, 11):

    # api-endpoint
    base_url = "http://www.pedigreedatabase.com"

    URL = base_url + "/dog.html"

    # location given here
    id = "2831598"

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'id': id}
    # PARAMS = {'id': i}

    # sending get request and saving the response as response object
    r = requests.get(url=URL, params=PARAMS)
    # r = requests.get(item)
    # extracting data in json format
    # response = r.json()

    if r.status_code == 200:
        print('Success!')
        r.encoding = 'utf-8'
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, 'html.parser')
        data = soup.find(id='dogherounit')
        # print(data)

        picture = data.find(id="dogpic")

        # Main dog info
        a = data.find_all('a')
        breed = a[0].text

        name = data.find('h1', class_="page-header").text
        s = name.find('\xa0')
        name = name[0:s]

        b = data.find_all('b')
        gender = data.find('img').text
        s = gender.find('\n')
        gender = gender[0:s]

        title_p = ''
        title_s = b[0].text

        birthday = data.find('h4').text
        s = birthday.find(':') + 2
        birthday = birthday[s:]
        s = birthday.find('.')
        birthday = birthday[0:s] + birthday[s+1:]
        picture = URL + picture.find('img')['src']
        registry = data.find('i').text

        he = b[1].text
        s = he.find('Hip:') + 5
        hips = he[s:]
        s = hips.find(' -')
        hips = hips[0:s]
        s = he.find('Elbows:') + 8
        elbows = he[s:]
        microchip = data.find('strong').text

        # Linebreeding info
        linebreeding = soup.find(id='lbinfo').find('p')

        # Pedigree info
        data = soup.find(id='dogpedigree')
        pedigree = data.find_all('td')
        father = pedigree[0]
        mother = pedigree[7]

        father_id = father.find('a')['href']
        s = father_id.find('?id=') + 4
        father_id = father_id[s:]
        s = father_id.find('-')
        father_id = father_id[0:s]

        mother_id = mother.find('a')['href']
        s = mother_id.find('?id=') + 4
        mother_id = mother_id[s:]
        s = mother_id.find('-')
        mother_id = mother_id[0:s]

        x = {
            "id": id,
            "name": name,
            "breed": breed,
            "gender": gender,
            "title_p": title_p,
            "title_s": title_s,
            "birthday": birthday,
            "picture_url": picture,
            # "registries": [{"registry": registry, "id": registry_id}],
            "hips": hips,
            "elbows": elbows,
            "microchip": microchip,
            "linebreeding": linebreeding,
            "father_id": father_id,
            "mother_id": mother_id
        }
        # y = json.dumps(x)
        # print(y)
        with open('outfile.json', 'w') as outfile:  
            json.dump(x, outfile)


    elif r.status_code == 404:
        print('Not Found.')
