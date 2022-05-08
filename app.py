from vk_api import VkApi, VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from auth_data import app_token as token

from functions import get_profile_photo, get_friends, get_groups, get_profile_id


def send_message(user_id, text, keyboard=None):
    post = {
        'user_id': user_id,
        'message': text,
        'random_id': 0
    }

    if keyboard is not None:
        post['keyboard'] = keyboard.get_keyboard()

    vk_session.method('messages.send', post)


def send_img(user_id, img, text):
    attachments = []
    print(img)
    upload_img = upload.photo_messages(photos=img)[0]
    attachments.append(f'photo{upload_img["owner_id"]}_{upload_img["id"]}')
    vk_session.method('messages.send', {
        'user_id': user_id,
        'message': text,
        'attachment': ','.join(attachments),
        'random_id': 0
    })


def info_sending():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                msg = event.text.lower()
                user_id = event.user_id

                if msg == 'стоп':
                    send_message(user_id, 'Поиск остановлен')
                    return 0
                try:
                    send_message(user_id, 'Ждите...')
                    send_img(user_id, get_profile_photo(msg), 'Смотрите')
                    send_message(user_id, get_profile_id(msg))
                    send_message(user_id, get_friends(msg))
                    send_message(user_id, get_groups(msg))
                    keyboard_end = VkKeyboard(one_time=True)
                    keyboard_end.add_button('Стоп', VkKeyboardColor.PRIMARY)
                    send_message(user_id, 'Кого ищем: ', keyboard=keyboard_end)
                except Exception:
                    send_message(user_id, 'Неверно указан пользователь')


def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:

                msg = event.text.lower()
                user_id = event.user_id

                if msg == 'привет':
                    send_message(user_id, 'Привет')
                    keyboard_start = VkKeyboard(one_time=True)
                    keyboard_start.add_button('Найти информацию', VkKeyboardColor.PRIMARY)
                    send_message(user_id, 'Что вы хотите сделать?', keyboard=keyboard_start)

                elif msg == 'найти информацию':
                    send_message(user_id, 'Чтобы очстановиться напишите "Стоп"')
                    keyboard_end = VkKeyboard(one_time=True)
                    keyboard_end.add_button('Стоп', VkKeyboardColor.PRIMARY)
                    send_message(user_id, 'Кого ищем: ', keyboard=keyboard_end)
                    info_sending()

                else:
                    keyboard_start = VkKeyboard(one_time=True)
                    keyboard_start.add_button('Найти информацию', VkKeyboardColor.PRIMARY)
                    send_message(user_id, 'Что вы хотите сделать?', keyboard=keyboard_start)


if __name__ == '__main__':
    vk_session = VkApi(token=token)
    session_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    upload = VkUpload(vk_session)
    main()
