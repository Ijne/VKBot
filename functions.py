import json
import os
import sqlite3

import requests
from auth_data import token


def add_user(name):
    con = sqlite3.connect(name)
    cur = con.cursor()
    cur.execute(f"""INSERT INTO users(logins) VALUES({get_profile_id(name)})""")
    con.commit()
    con.close()


def download_img(url, id, name):
    try:
        res = requests.get(url)

        if not os.path.exists(f'{name}/files'):
            os.mkdir(f'{name}/files/')
        if not os.path.exists(f'{name}/files/photos'):
            os.mkdir(f'{name}/files/photos')

        with open(f'{name}/files/photos/{id}.jpg', 'wb') as img_file:
            img_file.write(res.content)
        print('Успешно скачано')
    except Exception:
        print('Что-то не так...')


def get_profile_id(name):
    try:
        try:
            name = int(name)
            url = f'https://api.vk.com/method/users.get?user_ids={name}&fields=photo_400_orig&count=40' \
                  f'&access_token={token}&v=5.81'
            print('Вход по id')
        except Exception:
            url = f'https://api.vk.com/method/users.get?user_ids={name}&fields=domain&count=40' \
                  f'&access_token={token}&v=5.81'
            req = requests.get(url)
            src = req.json()
            url = f'https://api.vk.com/method/users.get?user_ids={src["response"][0]["id"]}' \
                  f'&fields=photo_400_orig&count=40&access_token={token}&v=5.81'
            print('Вход по домену')
        req = requests.get(url)
        src = req.json()

        if os.path.exists(f'{name}'):
            print(f'Директория с именем {name} уже существует!')
        else:
            os.mkdir(str(name))

        with open(f'{name}/{name}.profile_json', 'w', encoding='utf-8') as file:
            json.dump(src, file, indent=4, ensure_ascii=False)

        try:
            return f'ID пользователя: {src["response"][0]["id"]}'
        except Exception:
            print('Что-то не так...')
    except Exception:
        print('Что-то не так...')


def get_profile_photo(name):
    try:
        try:
            name = int(name)
            url = f'https://api.vk.com/method/users.get?user_ids={name}&fields=photo_400_orig&count=40' \
                  f'&access_token={token}&v=5.81'
            print('Вход по id')
        except Exception:
            url = f'https://api.vk.com/method/users.get?user_ids={name}&fields=domain&count=40' \
                  f'&access_token={token}&v=5.81'
            req = requests.get(url)
            src = req.json()
            url = f'https://api.vk.com/method/users.get?user_ids={src["response"][0]["id"]}' \
                  f'&fields=photo_400_orig&count=40&access_token={token}&v=5.81'
            print('Вход по домену')
        req = requests.get(url)
        src = req.json()

        if os.path.exists(f'{name}'):
            print(f'Директория с именем {name} уже существует!')
        else:
            os.mkdir(str(name))

        with open(f'{name}/{name}.profile_json', 'w', encoding='utf-8') as file:
            json.dump(src, file, indent=4, ensure_ascii=False)

        try:
            photo = src['response'][0]

            download_img(photo['photo_400_orig'], 'profile_photo', name)
            return f'{name}/files/photos/profile_photo.jpg'
        except Exception:
            print('Что-то не так...')
    except Exception:
        print('Что-то не так...')


def get_wall_posts(name):
    try:
        try:
            name = int(name)
            url = f'https://api.vk.com/method/wall.get?owner_id={name}&count=40&access_token={token}&v=5.81'
            print('Вход по id')
        except Exception:
            url = f'https://api.vk.com/method/wall.get?domain={name}&count=40&access_token={token}&v=5.81'
            print('Вход по домену')
        req = requests.get(url)
        src = req.json()

        if os.path.exists(f'{name}'):
            print(f'Директория с именем {name} уже существует!')
        else:
            os.mkdir(str(name))

        with open(f'{name}/{name}.posts_json', 'w', encoding='utf-8') as file:
            json.dump(src, file, indent=4, ensure_ascii=False)

        try:
            posts = src['response']['items']

            for post in posts:
                if post['attachments'][0]['type'] == 'photo':
                    photo = post['attachments'][0]['photo']
                    download_img(photo['sizes'][-1]['url'], photo['id'], name)
                    return f'{name}/files/photos/{photo["id"]}.jpg'
        except Exception:
            print('Что-то не так...')
    except Exception:
        print('Что-то не так...')


def get_friends(name):
    try:
        try:
            name = int(name)
            url = f'https://api.vk.com/method/friends.get?user_id={name}&fields=domain&count=40' \
                  f'&access_token={token}&v=5.81'
            print('Вход по id')
        except Exception:
            url = f'https://api.vk.com/method/users.get?user_ids={name}&fields=domain&count=40' \
                  f'&access_token={token}&v=5.81'
            req = requests.get(url)
            src = req.json()
            url = f'https://api.vk.com/method/friends.get?user_id={src["response"][0]["id"]}' \
                  f'&fields=domain&count=40&access_token={token}&v=5.81'
            print('Вход по домену')
        req = requests.get(url)
        src = req.json()

        if os.path.exists(f'{name}'):
            print(f'Директория с именем {name} уже существует!')
        else:
            os.mkdir(str(name))

        with open(f'{name}/{name}_friends.json', 'w', encoding='utf-8') as file:
            json.dump(src, file, indent=4, ensure_ascii=False)

        try:
            friends = src['response']['items']
            text = 'Друзья: \n'
            for item in friends:
                text += f'{item["first_name"]} {item["last_name"]} - {item["id"]}\n'
            return text
        except Exception:
            print('Что-то не так...')
    except Exception:
        print('Что-то не так...')


def get_groups(name):
    try:
        try:
            name = int(name)
            url = f'https://api.vk.com/method/groups.get?user_id={name}&extended=1&count=40' \
                  f'&access_token={token}&v=5.81'
            print('Вход по id')
        except Exception:
            url = f'https://api.vk.com/method/users.get?user_ids={name}&fields=domain&count=40' \
                  f'&access_token={token}&v=5.81'
            req = requests.get(url)
            src = req.json()
            url = f'https://api.vk.com/method/groups.get?user_id={src["response"][0]["id"]}' \
                  f'&extended=1&count=40&access_token={token}&v=5.81'
            print('Вход по домену')

        req = requests.get(url)
        src = req.json()

        if os.path.exists(f'{name}'):
            print(f'Директория с именем {name} уже существует!')
        else:
            os.mkdir(str(name))

        with open(f'{name}/{name}_groups.json', 'w', encoding='utf-8') as file:
            json.dump(src, file, indent=4, ensure_ascii=False)

        try:
            groups = src['response']['items']
            text = 'Сообщества: \n'
            for item in groups:
                text += f'{item["name"]}\n'
            return text
        except Exception:
            print('Что-то не так...')
    except Exception:
        print('Что-то не так...')
