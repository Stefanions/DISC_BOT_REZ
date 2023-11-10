#Подключение библиотек
import res
import discord
from discord.ext import commands
from discord.ui import Button, View, Select
import numpy as np
from typing import List

#HASH_MAP 
class novob:
    def __init__(self, id):
        self.user_id = id
    
    #############Поля для раздачи ролей###############
    #id роли мейн тайма
    id_main_time : List[int]
    #id роли количества часов
    id_hours : int
    #id главного направления
    id_direction : int
    #id главной роли в игре
    id_main_game_role : int
    #id второстепенных ролей в игре
    id_game_role : List[int]

    #############Поля для потенциально отправки в гугл форму###############
    #Ник в игре
    nick : str
    #Наименование мейн тайма
    main_time : List[str]
    #Часовой пояс
    time_zone : str
    #количества часов
    hours : str
    #Главное направление
    direction : str
    #Главная роль в игре
    main_game_role : str
    #Второстепенные роли
    game_role : List[str]
    #Ответ на вопрос Ты понимаешь, что для того, что бы играть командно, нужно, что бы все делали одинаково? 
    answer_q8 : str
    #Возраст
    age : int
    #Ответ на вопрос Оцени самостоятельно навык твоей стрельбы в SQUAD? от 0 до 10
    shooting_skill : str
    #Ответ на вопрос Насколько ты считаешь себя дисциплинированным игроком, если играешь в отряде? От 0 до 10
    discipline : str
    #Ответ на вопрос Как ты считаешь, насколько ты хорош при радиообмене от 0 до 10?
    radio_exchange : str
    #Ответ на вопрос Ты хочешь играть серьезные игры в SQUAD? (Считай что это киберспорт, но только в скваде)
    answer_q13 : str
    #Ответ на вопрос Откуда вы о нас узнали? Если вас пригласили, обязательно напишите ник человека, кто это сделал (Хотя бы примерный, мы поймем xD)
    answer_q14 : str
    
