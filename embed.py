#Подключение библиотек
import res
import discord
from discord.ext import commands
from discord.ui import Button, View, Select
import numpy as np
import class_novob

#Эмбеды

#Первый эмбед приветствия
emb_1 = discord.Embed(
    title="Добро пожаловать в Академию ССО!",
    description=
    (
        "Прежде чем мы с тобой начнем взаимодействовать, нам нужно подробнее узнать о тебе. "
        "\n\nГляди! Я снизу отправил тебе вопросы, ответь на них. Затем, нажми кнопку - 'завершить знакомство' и ты получишь доступ к Академии!\n\n"
        "p.s После прохождения формы, ты получишь доступ к Академии. Что тебе там делать?\n\n"
        "1) Жди тренировок.\n Их ты можешь найти в канале анонс-тренировок. Обязательно отмечайся!\n\n"
        "2) Просто присоединяйся в канал.\n Знакомься, но обязательно скажи, что ты только присоединился, что бы ребята понимали, что, возможно, тебе нужно помочь освоится."
    ),
        color=discord.Color.from_rgb(255, 255, 255) # ебашим белой полосочкой, иначе некрасиво)
    )


#Эмбеды вопросов 
class emb_2():
    def __init__(self, zagolovok):
        self.emb = discord.Embed(
            title=zagolovok,
            color=discord.Color.from_rgb(139, 187, 236)
            )