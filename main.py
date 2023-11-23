#Файл с основными командами
#Подключение библиотек

import res
import discord
from discord.ext import commands
from discord.ui import Button, View, Select
import numpy as np
import question
import embed
import class_novob
import time

#Базовые структуры
class Main(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

bot = Main(command_prefix = "Многоуважаемый дежурный по булочкам ",intents = discord.Intents.all(),help_command = None)
####Функция удаления сообщений####
#Первый аргумент из какого канала удалить сообщения. Второй аргумент говорит сколько сообщений надо удалить
async def del_bot_mes(channel, lim = None): 
    #Удаляю сообщения
    async for message in channel.history(limit=lim):
        if message.author.id == bot.user.id:
            try:
                await message.delete()
            except discord.errors.NotFound:
                pass

#####Функция обработки исключения#####
async def on_error(user):
    channel = bot.get_channel(user.dm_channel.id)
    await channel.send("Произошла техническая ошибка или вы очень долго отвечали на вопрос.\n Через 10 секунд все сообщения бота тут удалятся.\nПосле того как все сообщения удаляться, зайдите обратно на сервер и снова нажмите кнопку пройти опрос")
    time.sleep(10)
    await del_bot_mes(channel)
    #Очищаю массивы
    try:
        mem_not_end_opr.remove(user.id)
        del question.mem_data[user.id]   
    except:
        pass

#Время ожидания ответа
time_wait = question.time_wait
###########################################Классы кнопок########################################
#Кнопка при вступлении
class main_but(View):
    @discord.ui.button(label = "Пройти опрос", style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction, button):
        await interaction.response.defer()  
        try:
            await Clean_and_Intro_LS(interaction.user)
        except Exception:
            await on_error(interaction.user)

#Кнопка после ввода ответов на тест
class main_resualt_but(View):
    @discord.ui.button(label = "Продолжить", style=discord.ButtonStyle.success)
    async def button_callback(self, interaction, button):
        await interaction.response.defer()
        
#Кнопка завершающая
class main_end_but(View):
    @discord.ui.button(label = "Завершить тест", style=discord.ButtonStyle.danger)
    async def button_callback(self, interaction, button):
        try:
            await interaction.response.defer()
            #Изменю никнейм
            guild = bot.get_guild(res.id_server)
            id_v = interaction.user.id
            member = guild.get_member(id_v)
            #Изменяю никнейм
            nick_ser = question.mem_data[id_v].nick
            nick_ser = "Новобранец | " + nick_ser
            await member.edit(nick = nick_ser)
            #Добавляю не выбираемые роли
            for i in res.not_choice_role:
                role = guild.get_role(i)
                await member.add_roles(role)
            #Добавляю роли мейн тайма
            for i in question.mem_data[id_v].id_main_time:
                role = guild.get_role(i)
                await member.add_roles(role)
            #Добавляю роль колличество часов
            role = guild.get_role(question.mem_data[id_v].id_hours)
            await member.add_roles(role)
            #Добавляю роль главного направления
            role = guild.get_role(question.mem_data[id_v].id_direction)
            await member.add_roles(role)
            #Добавляю роль главной роли в игре
            role = guild.get_role(question.mem_data[id_v].id_main_game_role)
            await member.add_roles(role)
            #Добавляю роли второстепенных ролей в игре
            for i in question.mem_data[id_v].id_game_role:
                role = guild.get_role(i)
                await member.add_roles(role)
            #Удаляю массив с ролями 
            del question.mem_data[id_v]
            channel = bot.get_channel(res.id_chanel_pogovorim_tut)
            await channel.send(f"У нас новенький <@{interaction.user.id}>\nДобро пожаловать в академию!\nУспехов в учёбе!")
        except:
            await on_error(interaction.user)
            guild = bot.get_guild(res.id_server)
            id_v = interaction.user.id
            member = guild.get_member(id_v)
            await member.edit(roles=[])

        


###########################################Функциии разные########################################

#Для отслеживания людей, которые не прошли собеседование в личных сообщений бота до конца
mem_not_end_opr = []

#Очистка сообщений + вызов функции
async def Clean_and_Intro_LS(user):

    #Проверка на то что пользователь ещё не проходит тест
    if ((user.id in mem_not_end_opr) and (user.id in question.mem_data)):
        return
    else:
        mem_not_end_opr.append(user.id)
        question.mem_data[user.id] = class_novob.novob(user.id)

    #Удаление сообщений
    await user.send("Привет")
    channel = bot.get_channel(user.dm_channel.id)
    await del_bot_mes(channel)

    await Intro_LS(user)

#Функция прохождения первого собеседования в личных сообщения бота
async def Intro_LS(user):
    try:
        #Проверка на выбор селекта 
        def check(interaction):
            custom_id = interaction.data['custom_id']
            return ((interaction.user.id == user.id) and (interaction.channel.id == user.dm_channel.id) and (custom_id == sel))

        #Тут создаю окошечко для наших селектов и строк
        s = View()
        
        #Приветственное сообщение
        await user.send(embed=embed.emb_1)
        
        #### 1 вопрос
        await question.question_1(user, bot)

        #### 2 вопрос
        sel = "s_2"
        await question.question_2(user, bot, s, check)

        #### 3 вопрос
        sel = "s_3"
        await question.question_3(user, bot, s, check)

        #### 4 вопрос
        sel = "s_4"
        await question.question_4(user, bot, s, check)

        #### 5 вопрос
        sel = "s_5"
        await question.question_5(user, bot, s, check)

        #### 6 вопрос
        sel = "s_6"
        await question.question_6(user, bot, s, check)

        #### 7 вопрос
        sel = "s_7"
        await question.question_7(user, bot, s, check)
        
        #### 8 вопрос
        sel = "s_8"
        await question.question_8(user, bot, s, check)

        #### 9 вопрос   
        sel = "s_9" 
        await question.question_9(user, bot)

        #### 10 вопрос
        sel = "s_10"
        await question.question_10(user, bot, s, check)

        #### 11 вопрос
        sel = "s_11"
        await question.question_11(user, bot, s, check)

        #### 12 вопрос
        sel = "s_12"
        await question.question_12(user, bot, s, check)

        #### 13 вопрос rdy
        sel = "s_13"
        await question.question_13(user, bot, s, check)

        #### 14 вопрос
        sel = "s_14"
        await question.question_14(user, bot, s)


        #Результирующая кнопка 
        but_rez = main_resualt_but()
        await user.send(view=but_rez)
        #Проверка на нажатие на кнопку результирующую тест
        def check_in_rez(interaction):
            return ((interaction.user.id == user.id) and (interaction.channel.id == user.dm_channel.id) and (interaction.data['component_type'] == 2))
        await bot.wait_for('interaction', check=check_in_rez, timeout=time_wait)

        #Удаление кнопки
        channel = bot.get_channel(user.dm_channel.id)
        await del_bot_mes(channel, 1)


        result_emb = discord.Embed(
            title="Ваши ответы на наши вопросы:",
            description=(
                f"_**1. Какой у тебя ник в игре?**_\n{question.mem_data[user.id].nick}\n\n"
                
                f"_**2. В какое время относительно МСК ты играешь в основном?**_\n{', '.join(question.mem_data[user.id].main_time)}\n\n"

                f"_**3. Какой у тебя часовой пояс?**_\n{question.mem_data[user.id].time_zone}\n\n"
                
                f"_**4. Сколько у тебя часов в SQUAD?**_\n{question.mem_data[user.id].hours}\n\n"

                f"_**5. Какое направление тебе нравится больше всего?**_\n{question.mem_data[user.id].direction}\n\n"

                f"_**6. Выбери одну роль (стрелковую специальность), номер один для тебя?**_\n{question.mem_data[user.id].main_game_role}\n\n"

                f"_**7. Выбери дополнительные 2 или более роли, помимо основной. Напиши их ниже.**_\n{', '.join(question.mem_data[user.id].game_role)}\n\n"

                f"_**8. Ты понимаешь, что для того, чтобы играть командно, нужно, чтобы все делали одинаково? **_\n{question.mem_data[user.id].answer_q8}\n\n"

                f"_**9. Сколько тебе лет?**_\n{question.mem_data[user.id].age}\n\n"

                f"_**10. Оцени самостоятельно навык твоей стрельбы в SQUAD?**_\n{question.mem_data[user.id].shooting_skill}\n\n"

                f"_**11. Насколько ты считаешь себя дисциплинированным игроком, если играешь в отряде?**_\n{question.mem_data[user.id].discipline}\n\n"

                f"_**12. Как ты считаешь, насколько ты хорош при радиообмене от 0 до 10?**_\n{question.mem_data[user.id].radio_exchange}\n\n"

                f"_**13. Ты хочешь играть серьезные игры в SQUAD? (Считай что это киберспорт, но только в скваде)**_\n{question.mem_data[user.id].answer_q13}\n\n"

                f"_**14. Откуда вы о нас узнали? Если вас пригласили, обязательно напишите ник человека, кто это сделал (Хотя бы примерный, мы поймем xD)**_\n{question.mem_data[user.id].answer_q14}"
            ),
            color=discord.Color.from_rgb(152, 41, 101)
            )
        result_emb.set_footer(text="Created by Zyu & _Osha_")
        
        await user.send(embed=result_emb)


        but_end = main_end_but()
        await user.send(view=but_end)
        #Проверка на нажатие на кнопку заканачивающую тест
        def check_in_end(interaction):
            return ((interaction.user.id == user.id) and (interaction.channel.id == user.dm_channel.id) and (interaction.data['component_type'] == 2))
        await bot.wait_for('interaction', check=check_in_end, timeout=time_wait)

        #Удаление сообщений бота
        channel = bot.get_channel(user.dm_channel.id)
        await del_bot_mes(channel)

        #Отправляю в канал с формами
        channel = bot.get_channel(res.id_chanel_whitch_form)
        await channel.send(f"Новая форма\n<@&{res.id_acad}> <@&{res.id_nach_otdela}> <@&{res.id_nach_shtab}>")  
        await channel.send(embed=result_emb)  

        try:
            mem_not_end_opr.remove(user.id)
        except:
            pass
    except:
        await on_error(user)
    return





#При включении бота
@bot.event
async def on_ready():
    channel = bot.get_channel(res.id_hochu_v_cadetku)
    await del_bot_mes(channel)
    print("I am here")
    but_main = main_but()
    await channel.send("Я начал работу", view=but_main)

#КЕК
@bot.command()
async def привет(ctx):
    await ctx.send("Пошёл нахуй")


bot.run(res.token)
