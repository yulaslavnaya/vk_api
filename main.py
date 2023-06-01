import vk_api
import json

user_id = input("Введите id пользователя: ")
params = input("Что хотите о нем узнать? (друзья, подарки, фото, видео) для выхода напишите `выход`")


# Введите свои учетные данные ВКонтакте
login = '89126019954'
with open("pass.txt", "r", encoding = "utf-8") as file:
    password = file.readline()

# Авторизация пользователя
vk_session = vk_api.VkApi(login, password)
vk_session.auth()

# Получение экземпляра API
vk = vk_session.get_api()

while params != "выход":
    if params == "подарки":

        gifts = vk.gifts.get(user_id=user_id)

        # Получение информации о пользователях, которые подарили подарки
        user_ids = [gift['from_id'] for gift in gifts['items']]
        users_info = vk.users.get(user_ids=user_ids, fields='first_name,last_name')

        # Создание словаря для хранения информации о пользователях
        users_dict = {user['id']: user for user in users_info}

        # Вывод списка подарков и имен пользователей, которые их подарили
        for gift in gifts['items']:
            from_user_id = gift['from_id']
            if from_user_id in users_dict:
                from_user = users_dict[from_user_id]
                print(f"Подарок: {gift['gift']['thumb_256']}")
                print(f"Подарил(а): {from_user['first_name']} {from_user['last_name']}")
                print()
            else:
                print(f"Подарок: {gift['gift']['thumb_256']}")
                print("Подарил(а): Неизвестный пользователь")
                print()
    elif params == "друзья":
        friends = vk.friends.get(user_id=user_id, fields='first_name,last_name')
        # Вывод списка друзей
        for friend in friends['items']:
            print(friend['first_name'], friend['last_name'])

    elif params == "фото":
        albums = vk.photos.getAlbums(owner_id=user_id)
        for album in albums['items']:
            print(album['title'])

    elif params == "видео":
        videos = vk.video.getAlbums(owner_id=user_id)
        # Вывод названий фотоальбомов
        for video in videos['items']:
            print(video['title'])

    else:
        print("некорректная команда!")
    params = input("Что хотите о нем узнать? (друзья, подарки, фото, видео) для выхода напишите `выход`")