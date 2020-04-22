import getpass

import requests


PELOSHADOW_EMAIL = '' # LOAD FROM CONFIG
PELOSHADOW_PASSWORD = getpass.getpass() # LOAD FROM CONFIG or getpass

PELOTON_API_ROOT = 'https://api.onepeloton.com/api'

s = requests.Session()
payload = {'username_or_email':PELOSHADOW_EMAIL, 'password':PELOSHADOW_PASSWORD}
s.post('https://api.onepeloton.com/auth/login', json=payload)

my_id = s.get(f'{PELOTON_API_ROOT}/me').json().get('id')

currently_followed_ids = []
next = True
page = 0
while page != None:
    resp = s.get(f'{PELOTON_API_ROOT}/user/{my_id}/following?page={page}')
    if resp.status_code != 200:
        next = None
        continue
    followers = resp.json()['data']
    for follower in followers:
        currently_followed_ids.append(follower['id'])
    page = resp.json().get('next', None)

users_to_follow =[] # TODO Load from input file

ids_to_follow = []

for user in users_to_follow:
    resp = s.get(f'{PELOTON_API_ROOT}/user/{user}')
    if resp.status_code == 200:
        candidate_id = resp.json()['id']
        if candidate_id not in currently_followed_ids:  
            ids_to_follow.append(candidate_id)
        else:
            print(f'User already followed: {user}')
    else:
        print(f'User not found: {user}')

for id in ids_to_follow:
    payload = {'user_id': id, 'action': 'follow'}
    s.post(f'{PELOTON_API_ROOT}/user/change_relationship', json=payload)
