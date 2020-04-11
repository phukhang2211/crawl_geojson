import json
import requests
import time

def get_data():
    k = int(input("Input number location you want to take: "))
    type = input("Input your Place Type: ")
    keyword = input("Input your keyword: ")
    radius = input("Input radius round: ")
    location = input("Input location around: ")
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    with open('API_google.txt','r') as f:
        api=f.read()
    if type == "":
        type = 'hospital'
    if radius == "":
        radius = '5000000'
    if location == "":
        location = '10.762318, 106.645470'
    if keyword == "":
        keyword = 'hospital, heath'
    if k == "":
        k = 50
    params = {
        'type': type,
        'radius': radius,
        'keyword': keyword,
        'location':location,
        'key': api
    }
    resp = requests.get(url, params).json()
    print(resp)
    total = {
   "type": "FeatureCollection",
   "features": []
    }
    for result in resp['results']:
        geo_data = {
            'type': 'Feature',
            'geometry' : { 
                'type': 'Point',
                'coordinates': [result['geometry']['location']['lng'],
                            result['geometry']['location']['lat']]
                
            },
            'properties': {'name': result['name'], 'Address': result['vicinity'] 
            }
        }
        total['features'].append(geo_data)

    while len(total['features']) < k:
        time.sleep(5) 
        if 'next_page_token' in resp:
            params['pagetoken'] = resp['next_page_token']
            print(params)
            resp = requests.get(url, params).json()
            print(resp)

            for result in resp['results']:
                geo_data = {
                        'type': 'Feature',
                        'geometry' : { 
                            'type': 'Point',
                            'coordinates': [result['geometry']['location']['lng'],
                                        result['geometry']['location']['lat']]
                                
                            },
                            'properties': {'name': result['name'], 'Address': result['vicinity'] 
                            }
                        }
                total['features'].append(geo_data)
        else:
            break

    print(len(total['features']))
    return total


def main():
    result = (get_data())
    name_file = input("Input name of your geojson :")
    with open(name_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(result, indent =4))
    pass



if __name__ == "__main__":
    main()
