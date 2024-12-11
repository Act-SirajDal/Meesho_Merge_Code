# import time
#
# import requests
#
# cookies = {
#     'ANONYMOUS_USER_CONFIG': 'j%3A%7B%22clientId%22%3A%229f141fa9-9639-4470-9dd1-fd5e9d11%22%2C%22instanceId%22%3A%229f141fa9-9639-4470-9dd1-fd5e9d11%22%2C%22xo%22%3A%22eyJ0eXBlIjoiY29tcG9zaXRlIn0%3D.eyJqd3QiOiJleUpvZEhSd2N6b3ZMMjFsWlhOb2J5NWpiMjB2ZG1WeWMybHZiaUk2SWpFaUxDSm9kSFJ3Y3pvdkwyMWxaWE5vYnk1amIyMHZhWE52WDJOdmRXNTBjbmxmWTI5a1pTSTZJa2xPSWl3aVlXeG5Jam9pU0ZNeU5UWWlmUS5leUpwWVhRaU9qRTNNamt4TlRJd01EUXNJbVY0Y0NJNk1UZzROamd6TWpBd05Dd2lhSFIwY0hNNkx5OXRaV1Z6YUc4dVkyOXRMMmx1YzNSaGJtTmxYMmxrSWpvaU9XWXhOREZtWVRrdE9UWXpPUzAwTkRjd0xUbGtaREV0Wm1RMVpUbGtNVEVpTENKb2RIUndjem92TDIxbFpYTm9ieTVqYjIwdllXNXZibmx0YjNWelgzVnpaWEpmYVdRaU9pSXhPV1psTVRNMk5pMWlaRGszTFRRM056VXRPVFprWWkwMk5EQTJNbVl3TUdOa00ySWlmUS5PQ3g0R0Z2RGxQbzJMX0lrVDYtTXhESDk0R3VkaEF3V3BvZll5TUFxMHJVIiwieG8iOm51bGx9%22%2C%22createdAt%22%3A%222024-10-17T08%3A00%3A04.691Z%22%7D',
#     '__connect.sid__': 's%3A8aoPdDZq83t9bJy1BZl770LBJl4YP9f5.coidu8NQNa1ARLYJXXUfrrsVnfOrIXZe6te8DUbhdDs',
#     'location-details': '%7B%22city%22%3A%22Bengaluru%22%2C%22lat%22%3A%2213.2257%22%2C%22long%22%3A%2277.575%22%2C%22pincode%22%3A%22560001%22%7D',
#     'CAT_NAV_V2_COOKIE': '0.03879405040671546',
#     '_is_logged_in_': '1',
#     'isWG': 'true',
#     'bm_mi': '5DECA718C6E9F91C6505EC69BC655A58~YAAQ5hghFyrjg0STAQAApkb+TBm0EKt/+rRO0yZLvrOpn8d+YhbHNDITk+LTyL7XmhhFzvnneOPny34WFxSiWJhFEkZe+/SINnfEUV1DHJj/MTlGEFoNw7o+vq/Cqi4ojqAPMx7NuMVDpUGlQRiAPA6b3ilnrPLcGHiAPejkBLYuMaLhEeDqmC6R866e+bjzG9LggCrZr5aAUldMWxuwibcKL3ge+RxkRE+ByQd3nTLZMq+fKJMFc/WB8F3pJFGja20i+m8Mzt/ayQBifMZieYKQvy6GNjYFUa7DqYImhuND04kj8ivKrBYmc6jd~1',
#     'bm_sz': 'B90D295F0483388C359AFA13279E2E30~YAAQ5hghFyzjg0STAQAApkb+TBmbX93quaiFLxZoFTDDfY+ShdpQ39xddF5o+XresqdkzZAtlnQLEULiIyaqQB2+fhe6DIg0TFeBl37ymTlAMP8nVJrXMrD8r3QG8zO05jx8b+82wH7BcHCp3caO1tUw4LE4DcvtI4RiR5S53JSvSly+PyyWMa1w9dJdLiCWY8e81Ae9VpFGcom8qJpW46WMbjFFBR8t6ts86apyDDU35K0o5RVdPrDWn7mU0TpmOVhxtQlP2tdxdXGWEzlUZ5bccFA9GV/muPGWGuZ0KVld1aZ2RMzr/v7iHmTGx2VCMFcwIpwvw4Sr93Fo7mw88Y9sOqY5Ci7+FN1CegH8FtVzgJzt9pz8deepbaPbpLxGyVyBXF6t2GaiegrGMacNgr86~3355462~4470577',
#     '_abck': 'DD221DEC201BA06B0FD2857C9EABB415~0~YAAQ5hghF6Tkg0STAQAARUn+TAxPZqxShZ1RAzVBaSWtbIcLChL7wdRZewlVBlsofxFMcohaEu4V/dvAJyh6igowgPPWoOE75pehCxYb5VZGlWEy8ZlUMXvlK1cdzcryOwe/vhk4J9sEK63a2ma+TZSfnwrdsLCNTecpblWW4vCce0dcuEJSeSObUffHCI8sgPjJSKGL9c6To7bG8f1valYPjCCU8Re6gqdjHEgPDyarpfvbKCZKkQR2hzpR1uogEaxsaHHoWqmU/zXW8b5agFzgG49CegNlFpN4oiWsal7BMSKSBCQOGQERKU+XJt+T020TJqs9h3uHj9ZiUb4wNpDuBM6TohiTdYN5byEZU0xuBXUv1aLDs8MFAX1+G9VbLs690B4xgKrtVbsv3l5fIPxI3XoukWVJDexzV0LjTWkvl1Dg3g7th1XPpGv7KFagkE9dr+4KzH+o6o+4XGs/7JXDKX8tQWFMUVpcTA+BNtGU/3E41JezjzPkiB2txUrmcttmHQ85JZFrfi8guyh55kAQ/06HZu8AXQKD3vxczJcSHG+gu4wmKf3GUuzldRsPK6nKX+LOxv+Fl1vcjx8MlPjOKsJl+EyKp78F8ETTJmVkFkSzd4Tq0jXGKilMUn54bdS6uLZQP1pHNsnumGgPrcPyTjfc16HpD5cWARacnQYTDteAtWyI1m05ZBifwD+J~-1~-1~1732167148',
#     'ak_bmsc': '3E59F138696E5F4321D8684C9B5BEF6D~000000000000000000000000000000~YAAQ5hghF4fog0STAQAAQVD+TBnVCVW/I7YllnAAj+EvaOc8aPMRQP3FD+uewYqlteA98Be6ihfmKpQfWbN2s/8wVO/X7xMa1ADXVyKWgi5FDOtrQs7YeGQBptHBVTVTPIgHHJgtKUBWQSzpxQKtCEvR5n3fD5ahfe/ksDiep6SZ1Vk48R5SmhBi3kUBm3c7SpeVynsQEq+7IjV41rxTAAuu1BdbPGjBeuc/eDIPDJxW3c4Lt9zUyhYaO8fPZM5nVYS+fx0JeOKhYWhjdCTxjCCELjO3k7Jhdqm7vcd/+PCt/m6Pd6iJeaoyMYYnE+VxqFnGI4HrFVICkoJHCppmvLcBnVQpt+uZ4cF7ZsLVRK3ZTezk840P4TRg0V5HCVi1n3504JmUzN7/w1LCgV0NzGvIWXxV2Sn/ASF7qslA7QWZSy9LJlvJ2Oegik+2Q7d2zYpsw1By9CZ1CL12u7Vs/y84uOB3UdwPeQsBils=',
#     'INP_POW': '0.5590092492353755',
#     'bm_sv': '7B0604FB5097F7D5AC6080758A051918~YAAQ5hghF8lUhESTAQAAH/7+TBlY7AGutDyiFltyHvwTV9YmSxjUyT5oy5D/UFicyPst/bbK9Smx2N/0yzPh9ESBPUFxQZ6qKeV72gnQy3IxGZYfuaSWY6IOs9SOtV13kK5InLEtYwp/Nf/5nPXjVuBXT1IeQbQwfwj9/zS0eIWRQ86chXU4gHWbLzmmv+u8GQ2197ixvw9s2Z5H1OA9idff8nMO87VCcY9sP83AyKAAKVlWTDNnBmI1rpC3ApWFEA==~1',
#     'mp_60483c180bee99d71ee5c084d7bb9d20_mixpanel': '%7B%22distinct_id%22%3A%20%22122190837%22%2C%22%24device_id%22%3A%20%22192997db928158-0967c31e8a697-26001051-100200-192997db92981b%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22%24user_id%22%3A%20%22122190837%22%2C%22Is%20Anonymous%22%3A%20%22False%22%2C%22Instance_Id%22%3A%20%229f141fa9-9639-4470-9dd1-fd5e9d11%22%2C%22Session%20ID%22%3A%20%22fd064182-bbb7-4ef7-94b9-bf264eb3%22%2C%22V2%20Cat-Nav%20Exp%20Enabled%22%3A%20true%2C%22last%20event%20time%22%3A%201732163605220%2C%22%24search_engine%22%3A%20%22google%22%7D',
# }
#
# headers = {
#     'accept': 'application/json, text/plain, */*',
#     'accept-language': 'en-US,en;q=0.9',
#     'content-type': 'application/json',
#     # 'cookie': 'ANONYMOUS_USER_CONFIG=j%3A%7B%22clientId%22%3A%229f141fa9-9639-4470-9dd1-fd5e9d11%22%2C%22instanceId%22%3A%229f141fa9-9639-4470-9dd1-fd5e9d11%22%2C%22xo%22%3A%22eyJ0eXBlIjoiY29tcG9zaXRlIn0%3D.eyJqd3QiOiJleUpvZEhSd2N6b3ZMMjFsWlhOb2J5NWpiMjB2ZG1WeWMybHZiaUk2SWpFaUxDSm9kSFJ3Y3pvdkwyMWxaWE5vYnk1amIyMHZhWE52WDJOdmRXNTBjbmxmWTI5a1pTSTZJa2xPSWl3aVlXeG5Jam9pU0ZNeU5UWWlmUS5leUpwWVhRaU9qRTNNamt4TlRJd01EUXNJbVY0Y0NJNk1UZzROamd6TWpBd05Dd2lhSFIwY0hNNkx5OXRaV1Z6YUc4dVkyOXRMMmx1YzNSaGJtTmxYMmxrSWpvaU9XWXhOREZtWVRrdE9UWXpPUzAwTkRjd0xUbGtaREV0Wm1RMVpUbGtNVEVpTENKb2RIUndjem92TDIxbFpYTm9ieTVqYjIwdllXNXZibmx0YjNWelgzVnpaWEpmYVdRaU9pSXhPV1psTVRNMk5pMWlaRGszTFRRM056VXRPVFprWWkwMk5EQTJNbVl3TUdOa00ySWlmUS5PQ3g0R0Z2RGxQbzJMX0lrVDYtTXhESDk0R3VkaEF3V3BvZll5TUFxMHJVIiwieG8iOm51bGx9%22%2C%22createdAt%22%3A%222024-10-17T08%3A00%3A04.691Z%22%7D; __connect.sid__=s%3A8aoPdDZq83t9bJy1BZl770LBJl4YP9f5.coidu8NQNa1ARLYJXXUfrrsVnfOrIXZe6te8DUbhdDs; location-details=%7B%22city%22%3A%22Bengaluru%22%2C%22lat%22%3A%2213.2257%22%2C%22long%22%3A%2277.575%22%2C%22pincode%22%3A%22560001%22%7D; CAT_NAV_V2_COOKIE=0.03879405040671546; _is_logged_in_=1; isWG=true; bm_mi=5DECA718C6E9F91C6505EC69BC655A58~YAAQ5hghFyrjg0STAQAApkb+TBm0EKt/+rRO0yZLvrOpn8d+YhbHNDITk+LTyL7XmhhFzvnneOPny34WFxSiWJhFEkZe+/SINnfEUV1DHJj/MTlGEFoNw7o+vq/Cqi4ojqAPMx7NuMVDpUGlQRiAPA6b3ilnrPLcGHiAPejkBLYuMaLhEeDqmC6R866e+bjzG9LggCrZr5aAUldMWxuwibcKL3ge+RxkRE+ByQd3nTLZMq+fKJMFc/WB8F3pJFGja20i+m8Mzt/ayQBifMZieYKQvy6GNjYFUa7DqYImhuND04kj8ivKrBYmc6jd~1; bm_sz=B90D295F0483388C359AFA13279E2E30~YAAQ5hghFyzjg0STAQAApkb+TBmbX93quaiFLxZoFTDDfY+ShdpQ39xddF5o+XresqdkzZAtlnQLEULiIyaqQB2+fhe6DIg0TFeBl37ymTlAMP8nVJrXMrD8r3QG8zO05jx8b+82wH7BcHCp3caO1tUw4LE4DcvtI4RiR5S53JSvSly+PyyWMa1w9dJdLiCWY8e81Ae9VpFGcom8qJpW46WMbjFFBR8t6ts86apyDDU35K0o5RVdPrDWn7mU0TpmOVhxtQlP2tdxdXGWEzlUZ5bccFA9GV/muPGWGuZ0KVld1aZ2RMzr/v7iHmTGx2VCMFcwIpwvw4Sr93Fo7mw88Y9sOqY5Ci7+FN1CegH8FtVzgJzt9pz8deepbaPbpLxGyVyBXF6t2GaiegrGMacNgr86~3355462~4470577; _abck=DD221DEC201BA06B0FD2857C9EABB415~0~YAAQ5hghF6Tkg0STAQAARUn+TAxPZqxShZ1RAzVBaSWtbIcLChL7wdRZewlVBlsofxFMcohaEu4V/dvAJyh6igowgPPWoOE75pehCxYb5VZGlWEy8ZlUMXvlK1cdzcryOwe/vhk4J9sEK63a2ma+TZSfnwrdsLCNTecpblWW4vCce0dcuEJSeSObUffHCI8sgPjJSKGL9c6To7bG8f1valYPjCCU8Re6gqdjHEgPDyarpfvbKCZKkQR2hzpR1uogEaxsaHHoWqmU/zXW8b5agFzgG49CegNlFpN4oiWsal7BMSKSBCQOGQERKU+XJt+T020TJqs9h3uHj9ZiUb4wNpDuBM6TohiTdYN5byEZU0xuBXUv1aLDs8MFAX1+G9VbLs690B4xgKrtVbsv3l5fIPxI3XoukWVJDexzV0LjTWkvl1Dg3g7th1XPpGv7KFagkE9dr+4KzH+o6o+4XGs/7JXDKX8tQWFMUVpcTA+BNtGU/3E41JezjzPkiB2txUrmcttmHQ85JZFrfi8guyh55kAQ/06HZu8AXQKD3vxczJcSHG+gu4wmKf3GUuzldRsPK6nKX+LOxv+Fl1vcjx8MlPjOKsJl+EyKp78F8ETTJmVkFkSzd4Tq0jXGKilMUn54bdS6uLZQP1pHNsnumGgPrcPyTjfc16HpD5cWARacnQYTDteAtWyI1m05ZBifwD+J~-1~-1~1732167148; ak_bmsc=3E59F138696E5F4321D8684C9B5BEF6D~000000000000000000000000000000~YAAQ5hghF4fog0STAQAAQVD+TBnVCVW/I7YllnAAj+EvaOc8aPMRQP3FD+uewYqlteA98Be6ihfmKpQfWbN2s/8wVO/X7xMa1ADXVyKWgi5FDOtrQs7YeGQBptHBVTVTPIgHHJgtKUBWQSzpxQKtCEvR5n3fD5ahfe/ksDiep6SZ1Vk48R5SmhBi3kUBm3c7SpeVynsQEq+7IjV41rxTAAuu1BdbPGjBeuc/eDIPDJxW3c4Lt9zUyhYaO8fPZM5nVYS+fx0JeOKhYWhjdCTxjCCELjO3k7Jhdqm7vcd/+PCt/m6Pd6iJeaoyMYYnE+VxqFnGI4HrFVICkoJHCppmvLcBnVQpt+uZ4cF7ZsLVRK3ZTezk840P4TRg0V5HCVi1n3504JmUzN7/w1LCgV0NzGvIWXxV2Sn/ASF7qslA7QWZSy9LJlvJ2Oegik+2Q7d2zYpsw1By9CZ1CL12u7Vs/y84uOB3UdwPeQsBils=; INP_POW=0.5590092492353755; bm_sv=7B0604FB5097F7D5AC6080758A051918~YAAQ5hghF8lUhESTAQAAH/7+TBlY7AGutDyiFltyHvwTV9YmSxjUyT5oy5D/UFicyPst/bbK9Smx2N/0yzPh9ESBPUFxQZ6qKeV72gnQy3IxGZYfuaSWY6IOs9SOtV13kK5InLEtYwp/Nf/5nPXjVuBXT1IeQbQwfwj9/zS0eIWRQ86chXU4gHWbLzmmv+u8GQ2197ixvw9s2Z5H1OA9idff8nMO87VCcY9sP83AyKAAKVlWTDNnBmI1rpC3ApWFEA==~1; mp_60483c180bee99d71ee5c084d7bb9d20_mixpanel=%7B%22distinct_id%22%3A%20%22122190837%22%2C%22%24device_id%22%3A%20%22192997db928158-0967c31e8a697-26001051-100200-192997db92981b%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22%24user_id%22%3A%20%22122190837%22%2C%22Is%20Anonymous%22%3A%20%22False%22%2C%22Instance_Id%22%3A%20%229f141fa9-9639-4470-9dd1-fd5e9d11%22%2C%22Session%20ID%22%3A%20%22fd064182-bbb7-4ef7-94b9-bf264eb3%22%2C%22V2%20Cat-Nav%20Exp%20Enabled%22%3A%20true%2C%22last%20event%20time%22%3A%201732163605220%2C%22%24search_engine%22%3A%20%22google%22%7D',
#     'meesho-iso-country-code': 'IN',
#     'origin': 'https://www.meesho.com',
#     'priority': 'u=1, i',
#     'referer': 'https://www.meesho.com/pack-of-3-3s-combo-shoes-for-men-black-red-blue-black-t-blue-combo-shoes-in-color-comfortable-and-walking-shoes-for-men/p/2g1jlv',
#     'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
#     'sec-ch-ua-mobile': '?1',
#     'sec-ch-ua-platform': '"Android"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
# }
#
#
# proxy = {
#     'http':'http://9dbe950ef6284a5da9e7749db9f7cbd1:@api.zyte.com:8011/',
#     'https': 'http://9dbe950ef6284a5da9e7749db9f7cbd1:@api.zyte.com:8011/'
# }
# start = time.time()
# for i in range(5):
#     pin_list = ['560001','110001','400001','700020']
#     for i in pin_list:
#         json_data = {
#             'dest_pin': i,
#             'product_id': '2g1jlv',
#             'supplier_id': 204085,
#             'quantity': 1,
#         }
#         time.sleep(5)
#         import requests
#
#         url = "https://prod.meeshoapi.com/api/1.0/anonymous/shipping?dest_pin=110001&product_id=251757266&quantity=1&supplier_id=701966"
#
#         payload = {}
#         headers = {
#             'Authorization': '32c4d8137cn9eb493a1921f203173080',
#             'Xo': 'eyJ0eXBlIjoiY29tcG9zaXRlIn0=.eyJqd3QiOiJleUpvZEhSd2N6b3ZMMjFsWlhOb2J5NWpiMjB2ZG1WeWMybHZiaUk2SWpFaUxDSm9kSFJ3Y3pvdkwyMWxaWE5vYnk1amIyMHZhWE52WDJOdmRXNTBjbmxmWTI5a1pTSTZJa2xPSWl3aVlXeG5Jam9pU0ZNeU5UWWlmUS5leUpwWVhRaU9qRTNNekl4T1RFNE5qSXNJbVY0Y0NJNk1UZzRPVGczTVRnMk1pd2lhSFIwY0hNNkx5OXRaV1Z6YUc4dVkyOXRMMmx1YzNSaGJtTmxYMmxrSWpvaU5qVTRPVGs0Wm1VME9UUXlOR1V6T0Rsak5EQmtPVEJrWkRRMk5XUTBObVlpTENKb2RIUndjem92TDIxbFpYTm9ieTVqYjIwdllXNXZibmx0YjNWelgzVnpaWEpmYVdRaU9pSTBOamxtWkRFd09DMHpPR1JoTFRSaU1Ua3RPREZqTVMwNFlUa3lPVFk1TlRGaU56a2lmUS5IR1g1dW9qUzFwbFlVQnRpa054Zk5rc3AtbTVNRXQyUjJUVldCbmJHWUVJIiwieG8iOm51bGx9'
#         }
#
#         response = requests.request("GET", url, headers=headers, data=payload)
#
#         print(response.text)
#
# print(time.time()-start)

import http.client

conn = http.client.HTTPSConnection("shopee-id.p.rapidapi.com")

payload = "{\"userid\":\"126441979\",\"cookie\":\"LmVYSTRTak5JYm1kalFYbHpUeGFUZGdySXk1QXpGTmEwMUtvRVVGc0FzOEc4eDZvUEoybENuRy9TdGpqK3p5T2cyWmFuRUkwWExwV1JLWWN2VzNHTVByWHZsRU9vR2pkRTZCZDErNlZIZ2RsR1p2b1M0TUpZYkg2TnAvamwraU5CLzN5aG5CNVM3Vy9RdXpHYU9jaE53Y3pscHQ1MVZCSnlFTVBIdkpqVTU4S0l0SkdxU2ZPVnRQM1oraU84RWNrYk5JU1hJYkZBbnlqVEc4Vmpta1ZrZld6V0krN04wcDFHYThlb241S3Z5bDBRQ2lXb0VUZ2ZNN2VyeEVuMUR4KzAK\",\"useragent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36\"}"

headers = {
    'x-rapidapi-key': "168262fcabmsh583eda966ee2eeap1fc3c2jsn48f3eb94e8de",
    'x-rapidapi-host': "shopee-id.p.rapidapi.com",
    'Content-Type': "application/json"
}

conn.request("POST", "/follow/", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))