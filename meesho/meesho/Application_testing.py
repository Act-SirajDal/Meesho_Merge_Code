import json

import requests
import pymysql
db_name = 'meesho_master'
db_links_table = 'product_links_20241115'
pstart = ''
pend = ''

local_connect = pymysql.connect(
        host='localhost',
        user='root',
        password='actowiz',
        database=db_name
    )

local_cursor = local_connect.cursor()


dest_pin_list=[400001,560001,110001,700020]
product_id=344388183
supplier_id=73292
for dest_pin in dest_pin_list:
    query = f"select `meesho_pid` FROM {db_links_table} where status='Done' and id between {pstart} and {pend} and status_{dest_pin}='pending'"
    print(query)
    local_cursor.execute(query)
    meesho_pids = local_cursor.fetchall()

    url = f'https://prod.meeshoapi.com/api/1.0/anonymous/shipping?dest_pin={dest_pin}&product_id={product_id}&quantity=1&supplier_id={supplier_id}'

    headers = {
        'Accept-Encoding': 'gzip',
        'APP-CLIENT-ID': 'android',
        'APP-ISO-LANGUAGE-CODE': 'en',
        'APP-SDK-VERSION': '28',
        'App-Session-Id': '877dbf0c-bb00-4743-a465-e8e9d341aa63',
        'APP-USER-LOCATION': 'eyJsYXQiOiIxOC45NDc0IiwibG9uZyI6IjcyLjgxMzgiLCJwaW5jb2RlIjoiNDAwMDAxIiwiY2l0eSI6Ik11bWJhaSIsImFkZHJlc3NfaWQiOm51bGx9',
        'App-Version': '21.0',
        'App-Version-Code': '632',
        'Application-Id': 'com.meesho.supply',
        'Authorization': '32c4d8137cn9eb493a1921f203173080',
        'Connection': 'Keep-Alive',
        'Country-Iso': 'in',
        'Host': 'prod.meeshoapi.com',
        'Instance-Id': '3225712037ce488294a2460b24ef7cd3',
        'MEESHO-USER-CONTEXT': 'anonymous',
        'SHIELD-SESSION-ID': '',
        'User-Agent': 'okhttp/4.9.0',
        'Xo': 'eyJ0eXBlIjoiY29tcG9zaXRlIn0=.eyJqd3QiOiJleUpvZEhSd2N6b3ZMMjFsWlhOb2J5NWpiMjB2ZG1WeWMybHZiaUk2SWpFaUxDSm9kSFJ3Y3pvdkwyMWxaWE5vYnk1amIyMHZhWE52WDJOdmRXNTBjbmxmWTI5a1pTSTZJa2xPSWl3aVlXeG5Jam9pU0ZNeU5UWWlmUS5leUpwWVhRaU9qRTNNekU1T1RNME9Ua3NJbVY0Y0NJNk1UZzRPVFkzTXpRNU9Td2lhSFIwY0hNNkx5OXRaV1Z6YUc4dVkyOXRMMmx1YzNSaGJtTmxYMmxrSWpvaU16SXlOVGN4TWpBek4yTmxORGc0TWprMFlUSTBOakJpTWpSbFpqZGpaRE1pTENKb2RIUndjem92TDIxbFpYTm9ieTVqYjIwdllXNXZibmx0YjNWelgzVnpaWEpmYVdRaU9pSTJaRFE0T0RRNU15MWlZelkxTFRRNFltVXRPRFJqTVMwd1ltSTFZalF6T1RCa01EVWlmUS42TUJOSnhkbFVHWmEtR21xcDFjWWZ3YkNMVDNnVlF4dnhuMWdUQ2lKN0lBIiwieG8iOm51bGx9',
    }

    req = requests.get(url=url, headers=headers)
    print(req.text)
    print(req.status_code)





