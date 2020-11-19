import requests
import json
import sys

auth_token = "your_secret_api_token"

def get_zone_id():
    try:
        response = requests.get(
            url="https://dns.hetzner.com/api/v1/zones",
            headers={
                "Auth-API-Token": auth_token,
            },
        )
        json_object = json.loads(response.content)
        return json_object['zones'][0]['id']
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def update_dns(zone_id, record_id, address, record_name, dns_type):
    try:
        response = requests.put(
            url="https://dns.hetzner.com/api/v1/records/"+record_id,
            headers={
                "Content-Type": "application/json",
                "Auth-API-Token": auth_token,
            },
            data=json.dumps({
                "value": address,
                "ttl": 120,
                "type": dns_type,
                "name": record_name,
                "zone_id": zone_id
            })
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def get_record_id(zone_id, record_name):
    try:
        response = requests.get(
            url="https://dns.hetzner.com/api/v1/records",
            params={
                "zone_id": zone_id,
            },
            headers={
                "Auth-API-Token": auth_token,
            }
        )s
        json_response = json.loads(response.content)['records']
        for i in range(len(json_response)):
            name = json_response[i]['name']
            if name.lower() in [record_name.lower()]:
                return json_response[i]['id']
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

#send_request(sys.argv[1])
zone_id = get_zone_id()
update_dns(zone_id, get_record_id(zone_id, sys.argv[1]), sys.argv[3], sys.argv[1], sys.argv[2])