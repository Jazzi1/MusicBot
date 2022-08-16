import os

import psycopg2

MUSIC_DIR = 'got_music/'


def get_connection():
    connection = psycopg2.connect(
        host='localhost',
        port=5432,
        user='postgres',
        dbname='postgres',
        password='123'
    )
    return connection


def get_random_music():
    pass


def get_current_music(id_music: int, full_path=False):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM music_list WHERE id = %s'

    cursor.execute(sql, (id_music,))
    data = cursor.fetchall()
    name_music = data[0][1] + ' - ' + data[0][4]
    with open('got_music/' + name_music + '.mp3', 'wb') as music_file:
        music_file.write(bytes(data[0][3]))

    if full_path:
        name_music = MUSIC_DIR + name_music + '.mp3'

    return name_music


def get_music_by_name(name_music: str, full_path=False):
    connection = get_connection()
    cursor = connection.cursor()

    sql = 'SELECT * FROM music_list WHERE name = %s'
    cursor.execute(sql, (name_music,))
    data = cursor.fetchall()
    for i in data:
        music_name = i[1] + ' - ' + i[4]
        with open('got_music/' + music_name + '.mp3', 'wb') as music_file:
            music_file.write(bytes(i[3]))


def get_music_by_artist(artist_name: str, full_path=False):
    connection = get_connection()
    cursor = connection.cursor()

    sql = 'SELECT * FROM music_list WHERE artist = %s'
    cursor.execute(sql, (artist_name,))
    data = cursor.fetchall()
    music_list = []
    for i in data:
        music_name = i[1] + ' - ' + i[4] + '.mp3'
        with open('got_music/' + music_name, 'wb') as music_file:
            music_file.write(bytes(i[3]))
            if full_path:
                music_list.append('got_music/' + music_name)
            else:
                music_list.append(music_name)

    return music_list


def get_music_by_name_and_artist(artist_name: str, music_name: str):
    connection = get_connection()
    cursor = connection.cursor()

    sql = 'SELECT * FROM music_list WHERE artist = %s and name = %s'
    cursor.execute(sql, (artist_name, music_name))
    data = cursor.fetchall()
    name_music = data[0][1] + ' - ' + data[0][4]
    with open('got_music/' + name_music + '.mp3', 'wb') as music_file:
        music_file.write(bytes(data[0][3]))


def get_music_by_genre(genre: str, full_path=False):
    connection = get_connection()
    cursor = connection.cursor()

    sql = 'SELECT * FROM music_list WHERE genre = %s'
    cursor.execute(sql, (genre,))
    data = cursor.fetchall()
    music_list = []
    for i in data:
        music_name = i[1] + ' - ' + i[4] + '.mp3'
        with open('got_music/' + music_name, 'wb') as music_file:
            music_file.write(bytes(i[3]))
            if full_path:
                music_list.append('got_music/' + music_name)
            else:
                music_list.append(music_name)

    return music_list


def add_music_to_the_table(name: str, artist: str, genre: str, file: str):
    connection = get_connection()
    cursor = connection.cursor()

    sql = f'INSERT INTO music_list(name, artist, genre, bytes) VALUES (%s, %s, %s, %s)'

    binary_music = open(file, 'rb')
    cursor.execute(sql, (name, artist, genre, binary_music.read()))

    connection.commit()
    cursor.close()


def get_music(name: str, artist: str):
    connection = get_connection()
    cursor = connection.cursor()

    sql = 'SELECT name, artist, genre, bytes FROM music_list WHERE name = %s and artist = %s'
    cursor.execute(sql, (name, artist,))

    data = cursor.fetchone()
    file = data[1] + ' - ' + data[0] + '.mp3'
    saved_music = open('got_music/' + file, 'wb')
    saved_music.write(data[3])
    saved_music.close()


def music_search(path):
    result = []
    for root, dirs, files in os.walk(path):
        result.extend(files)
    right_music = []
    for i in result:
        if i.endswith('.mp3'):
            s = i.split(' - ')
            if len(s) == 2:
                right_music.append(i)

    return right_music


def send_music_from_dir(dir_name: str):
    music = music_search(dir_name)
    for i in music:
        s = i.strip('.mp3').split(' - ')
        try:
            add_music_to_the_table(s[1], s[0], '-', dir_name + i)
        except:
            print(i, 'ERROR')
        else:
            print(i, 'ADDED')
