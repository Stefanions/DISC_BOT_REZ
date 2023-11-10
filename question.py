#Подключение библиотек
import res
import discord
from discord.ext import commands
from discord.ui import Button, View, Select
import numpy as np

#HASH_MAP для запоминания ответов людей, которые проходят тест
mem_data = {}

#Время ожидания ответа
time_wait = 120.0

##############################################Селекты и не только + разные конструкции##############################################
####### 1 вопрос #######
async def q_1(user, bot):
    def check(message):
        return ((message.author.id == user.id) and (message.channel.id == user.dm_channel.id))
    mes = await bot.wait_for('message', check=check, timeout=time_wait)
    mem_data[user.id].nick = mes.content  

####### 2 вопрос #######
class q_2(Select):
    def __init__(self):
        super().__init__(
        placeholder="Список большой, листай вниз!", 
        min_values = 1,
        max_values = 4,
        options=[
        discord.SelectOption(label="Утром по МСК", value=res.q_2_1),
        discord.SelectOption(label="Днём по МСК", value=res.q_2_2),
        discord.SelectOption(label="Вечером по МСК", value=res.q_2_3),
        discord.SelectOption(label="Ночью по МСК", value=res.q_2_4)
        ], 
        custom_id="s_2"
        )
    async def callback(self, interaction):
        await interaction.response.defer()
        value = interaction.data['values']
        value_int = [int(x) for x in value]
        mem_data[interaction.user.id].id_main_time = value_int

        #-----------------------------#
        label_value = {}
        rez_label = []
        #Вытягиваю из селекта хэшмапу
        for i in (self.options):
            label_value[i.value] = i.label
        #Отбираю нужные лейблы
        for i in (value):
            rez_label.append(label_value[i])
        #-----------------------------#

        mem_data[interaction.user.id].main_time = rez_label

####### 3 вопрос #######
class q_3(Select):
    def __init__(self): 
        super().__init__(
        placeholder="Список большой, листай вниз!", 
        options=[
        # discord.SelectOption(label="UTC-12:00 (Антивампирский остров)"),
        # discord.SelectOption(label="UTC-11:00 (Самоа)"),
        # discord.SelectOption(label="UTC-10:00 (Гавайи)"),
        # discord.SelectOption(label="UTC-09:00 (Аляска)"),
        # discord.SelectOption(label="UTC-08:00 (Тихоокеанское время - Северная Америка)"),
        # discord.SelectOption(label="UTC-07:00 (Горное время - Северная Америка)"),
        # discord.SelectOption(label="UTC-06:00 (Центральное время - Северная Америка)"),
        # discord.SelectOption(label="UTC-05:00 (Восточное время - Северная Америка)"),
        # discord.SelectOption(label="UTC-04:00 (Атлантическое время - Северная Америка)"),
        # discord.SelectOption(label="UTC-03:00 (Бразилиа, Буэнос-Айрес)"),
        discord.SelectOption(label="UTC-02:00 (Среднеатлантическое время)"),
        discord.SelectOption(label="UTC-01:00 (Азорские острова, о. Зеленого Мыса)"),
        discord.SelectOption(label="UTC±00:00 (Западноевропейское время - Гринвич)"),
        discord.SelectOption(label="UTC+01:00 (Центральноевропейское время)"),
        discord.SelectOption(label="UTC+02:00 (Восточноевропейское время, Калининград)"),
        discord.SelectOption(label="UTC+03:00 (Московское время)"),
        discord.SelectOption(label="UTC+03:30 (Иранское время)"),
        discord.SelectOption(label="UTC+04:00 (Азербайджанское время, Грузинское время, Самарское время)"),
        discord.SelectOption(label="UTC+04:30 (Афганистанское время)"),
        discord.SelectOption(label="UTC+05:00 (Пакистанское время, Екатеринбургское время)"),
        discord.SelectOption(label="UTC+05:30 (Индийское стандартное время, Шри-Ланка)"),
        discord.SelectOption(label="UTC+05:45 (Непальское время)"),
        discord.SelectOption(label="UTC+06:00 (Омское время, Бангладешское время)"),
        discord.SelectOption(label="UTC+06:30 (Кокосовые острова, Мьянма)"),
        discord.SelectOption(label="UTC+07:00 (Красноярское время, Индокитайское время)"),
        discord.SelectOption(label="UTC+08:00 (Иркутское время, Китайское время, Западноавстралийское время)"),
        discord.SelectOption(label="UTC+08:45 (Юго-западное Западноавстралийское время)"),
        discord.SelectOption(label="UTC+09:00 (Якутское время, Японское стандартное время, Корейское время)"),
        discord.SelectOption(label="UTC+09:30 (Центральное австралийское время)"),
        discord.SelectOption(label="UTC+10:00 (Восточное австралийское время)"),
        discord.SelectOption(label="UTC+10:30 (Лорд-Хаулендский остров)"),
        discord.SelectOption(label="UTC+11:00 (Соломоновы острова, Вануату)"),
        discord.SelectOption(label="UTC+11:30 (Норфолкское время)"),
        discord.SelectOption(label="UTC+12:00 (Фиджи, Камчатское время)")
        # discord.SelectOption(label="UTC+12:45 (Чатемское время)"),
        # discord.SelectOption(label="UTC+13:00 (Тонга)"),
        # discord.SelectOption(label="UTC+14:00 (Линия перемены даты)")
        ], 
        custom_id="s_3")
    async def callback(self, interaction):
        await interaction.response.defer()
        value = interaction.data['values'][0]
        mem_data[interaction.user.id].time_zone = value


####### 4 вопрос #######
class q_4(Select):
    def __init__(self): 
        super().__init__(
        placeholder="Список большой, листай вниз!", 
        options=[
        discord.SelectOption(label="0-50 часов", value=res.q_4_1),
        discord.SelectOption(label="50+ часов", value=res.q_4_2),
        discord.SelectOption(label="100+ часов", value=res.q_4_3),
        discord.SelectOption(label="250+ часов", value=res.q_4_4),
        discord.SelectOption(label="500+ часов", value=res.q_4_5),
        discord.SelectOption(label="1000+ часов", value=res.q_4_6),
        discord.SelectOption(label="2000+ часов", value=res.q_4_7)
        ], 
        custom_id="s_4")
    async def callback(self, interaction):
        await interaction.response.defer()
        value = interaction.data['values']
        mem_data[interaction.user.id].id_hours = int(value[0])
        #-----------------------------#
        label_value = {}
        #Вытягиваю из селекта хэшмапу
        for i in (self.options):
            label_value[i.value] = i.label
        #-----------------------------#
        mem_data[interaction.user.id].hours = label_value[value[0]]



####### 5 вопрос #######
class q_5(Select):
    def __init__(self): 
        super().__init__(
        placeholder="Список большой, листай вниз!", 
        options=[
        discord.SelectOption(label="CMD подразделение", value=res.q_5_1),
        discord.SelectOption(label="Атакующее подразделение", value=res.q_5_2),
        discord.SelectOption(label="ДРГ подразделение", value=res.q_5_3),
        discord.SelectOption(label="Оборонительное подразделение", value=res.q_5_4),
        discord.SelectOption(label="Стройбат подразделение", value=res.q_5_5),
        discord.SelectOption(label="Минометное подразделение", value=res.q_5_6),
        discord.SelectOption(label="Техническое подразделение", value=res.q_5_7),
        discord.SelectOption(label="Пилотное подразделение", value=res.q_5_8)
        ], 
        custom_id="s_5")
    async def callback(self, interaction):
        await interaction.response.defer()
        value = interaction.data['values']
        mem_data[interaction.user.id].id_direction = int(value[0])
        #-----------------------------#
        label_value = {}
        #Вытягиваю из селекта хэшмапу
        for i in (self.options):
            label_value[i.value] = i.label
        #-----------------------------#
        mem_data[interaction.user.id].direction = label_value[value[0]]

####### 6 вопрос #######
class q_6(Select):
    def __init__(self): 
        super().__init__(
        placeholder="Список большой, листай вниз!", 
        options=[
        discord.SelectOption(label="CMD", value=res.q_6_1),
        discord.SelectOption(label="Сквадной", value=res.q_6_2),
        discord.SelectOption(label="Лидер Фаер Тимы", value=res.q_6_3),
        discord.SelectOption(label="Обычный стрелок", value=res.q_6_4),
        discord.SelectOption(label="Стрелок ГП", value=res.q_6_5),
        discord.SelectOption(label="Труба", value=res.q_6_6),
        discord.SelectOption(label="Тандем", value=res.q_6_7),
        discord.SelectOption(label="Медик", value=res.q_6_8),
        discord.SelectOption(label="Пулеметчик", value=res.q_6_9),
        discord.SelectOption(label="Танкист-командир", value=res.q_6_10),
        discord.SelectOption(label="Танкист-мехвод", value=res.q_6_11),
        discord.SelectOption(label="Танкист-стрелок", value=res.q_6_12),
        discord.SelectOption(label="Пилот", value=res.q_6_13)
        ], 
        custom_id="s_6")
    async def callback(self, interaction):
        await interaction.response.defer()
        value = interaction.data['values']
        mem_data[interaction.user.id].id_main_game_role = int(value[0])
        #-----------------------------#
        label_value = {}
        #Вытягиваю из селекта хэшмапу
        for i in (self.options):
            label_value[i.value] = i.label
        #-----------------------------#
        mem_data[interaction.user.id].main_game_role = label_value[value[0]]


####### 7 вопрос
class q_7(Select):
    def __init__(self): 
        super().__init__(
        placeholder="Список большой, листай вниз!", 
        min_values = 2,
        max_values = 12,
        options=[
        discord.SelectOption(label="CMD", value=res.q_7_1),
        discord.SelectOption(label="Сквадной", value=res.q_7_2),
        discord.SelectOption(label="Лидер Фаер Тимы", value=res.q_7_3),
        discord.SelectOption(label="Стрелок ГП", value=res.q_7_4),
        discord.SelectOption(label="Труба", value=res.q_7_5),
        discord.SelectOption(label="Тандем", value=res.q_7_6),
        discord.SelectOption(label="Медик", value=res.q_7_7),
        discord.SelectOption(label="Пулеметчик", value=res.q_7_8),
        discord.SelectOption(label="Такнкист-командир", value=res.q_7_9),
        discord.SelectOption(label="Танкист-мехвод", value=res.q_7_10),
        discord.SelectOption(label="Танкист-стрелок", value=res.q_7_11),
        discord.SelectOption(label="Пилот", value=res.q_7_12)
        ], 
        custom_id="s_7")

    async def callback(self, interaction):
        await interaction.response.defer()
        value = interaction.data['values']
        value_int = [int(x) for x in value]
        mem_data[interaction.user.id].id_game_role = value_int
        #-----------------------------#
        label_value = {}
        rez_label = []
        #Вытягиваю из селекта хэшмапу
        for i in (self.options):
            label_value[i.value] = i.label
        #Отбираю нужные лейблы
        for i in (value):
            rez_label.append(label_value[i])
        #-----------------------------#

        mem_data[interaction.user.id].game_role = rez_label


####### 8 вопрос #######
async def q_8(user, bot):
    def check(message):
        return ((message.author.id == user.id) and (message.channel.id == user.dm_channel.id))
    mes = await bot.wait_for('message', check=check, timeout=time_wait)
    mem_data[user.id].answer_q8 = mes.content  

####### 9 вопрос #######
async def q_9(user, bot):
    def check(message):
        return ((message.author.id == user.id) and (message.channel.id == user.dm_channel.id))
    mes = await bot.wait_for('message', check=check, timeout=time_wait)
    mem_data[user.id].age = mes.content 

    


####### 10 вопрос
class q_10(Select):
    def __init__(self): 
        super().__init__(
        placeholder="Список большой, листай вниз!", 
        options=[
        discord.SelectOption(label="0"),
        discord.SelectOption(label="1"),
        discord.SelectOption(label="2"),
        discord.SelectOption(label="3"),
        discord.SelectOption(label="4"),
        discord.SelectOption(label="5"),
        discord.SelectOption(label="6"),
        discord.SelectOption(label="7"),
        discord.SelectOption(label="8"),
        discord.SelectOption(label="9"),
        discord.SelectOption(label="10")
        ], 
        custom_id="s_10")
    async def callback(self, interaction):
        await interaction.response.defer()
        value = interaction.data['values']
        mem_data[interaction.user.id].shooting_skill = value[0]


####### 11 вопрос
class q_11(Select):
    def __init__(self): 
        super().__init__(
        placeholder="Список большой, листай вниз!", 
        options=[
        discord.SelectOption(label="0"),
        discord.SelectOption(label="1"),
        discord.SelectOption(label="2"),
        discord.SelectOption(label="3"),
        discord.SelectOption(label="4"),
        discord.SelectOption(label="5"),
        discord.SelectOption(label="6"),
        discord.SelectOption(label="7"),
        discord.SelectOption(label="8"),
        discord.SelectOption(label="9"),
        discord.SelectOption(label="10")
        ], 
        custom_id="s_11")
    async def callback(self, interaction):
        await interaction.response.defer()
        value = interaction.data['values']
        mem_data[interaction.user.id].discipline = value[0]

####### 12 вопрос
class q_12(Select):
    def __init__(self): 
        super().__init__(
        placeholder="Список большой, листай вниз!", 
        options=[
        discord.SelectOption(label="0"),
        discord.SelectOption(label="1"),
        discord.SelectOption(label="2"),
        discord.SelectOption(label="3"),
        discord.SelectOption(label="4"),
        discord.SelectOption(label="5"),
        discord.SelectOption(label="6"),
        discord.SelectOption(label="7"),
        discord.SelectOption(label="8"),
        discord.SelectOption(label="9"),
        discord.SelectOption(label="10")
        ], 
        custom_id="s_12")
    async def callback(self, interaction):
        await interaction.response.defer()
        value = interaction.data['values']
        mem_data[interaction.user.id].radio_exchange = value[0]

####### 13 вопрос
class q_13(Select):
    def __init__(self): 
        super().__init__(
        placeholder="Список большой, листай вниз!", 
        options=[
        discord.SelectOption(label="Да"),
        discord.SelectOption(label="Нет")
        ], 
        custom_id="s_13")
    async def callback(self, interaction):
        await interaction.response.defer()
        value = interaction.data['values']
        mem_data[interaction.user.id].answer_q13 = value[0]


####### 14 вопрос #######
async def q_14(user, bot):
    def check(message):
        return ((message.author.id == user.id) and (message.channel.id == user.dm_channel.id))
    mes = await bot.wait_for('message', check=check, timeout=time_wait)
    mem_data[user.id].answer_q14 = mes.content 