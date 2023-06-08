import datetime
import discord
import pyodbc
import sqlite3
import mysql.connector
import asyncio
from datetime import datetime
from mysql.connector import Error
from discord.ext import commands

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
driver= '{SQL Server Native Client 11.0}'

cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};Server=10.100.0.160;UID=Femi;PWD=Start!;DB=MVVMLoginDb;")
config = {
    'token': '',
    'prefix': '!',
}
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

# СПИСК ПОЛЬЗОВАТЕЛЕЙ
@bot.command()
async def user(ctx):
    try:
        cursor = cnxn.cursor()
        print("Чтение пользователей\nОткрытие соединения")

        sqlite_select_query = "SELECT [Username],[Name],[LastName],[Email] FROM [User]"
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        for i in range(0, len(records)):
            n = i+1
            await ctx.reply("\tПользователь " + str(n) + ":\nЛогин: " + records[i][0] + "\nИмя: " + records[i][1] + "\nФамилия: " + records[i][2] + "\nПочта: " + records[i][3])
    
    except sqlite3.Error as error:
        print("Ошибка при чтении базы данных", error)

    finally:
        if cnxn:
            cursor.close()
            print("Чтение пользователей\nУСПЕШНО\nСоединение закрыто")

# СПИСК ЗАДАЧ НА СЕГОДНЯ
@bot.command()
async def task(ctx):
    try:
        cursor = cnxn.cursor()
        print("Чтение задач\nОткрытие соединения")

        sqlite_select_query = "SELECT [EndTime],[Description] FROM [Employes] WHERE EndTime = CONVERT(date,  GETDATE())"
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        for i in range(0, len(records)):
            n = i+1
            await ctx.reply("Дата окончания: " + str(records[i][0]) + "\nЗадача: " + records[i][1])
    
    except sqlite3.Error as error:
        print("Ошибка при чтении базы данных", error)

    finally:
        if cnxn:
            cursor.close()
            print("Чтение задач\nУСПЕШНО\nСоединение закрыто")

# ДОБАВЛЕНИЕ ЗАПИСИ
@bot.command()
async def add(ctx):
    message = ctx.message.content
    chunks = message.split(' ')
    end_date = datetime.strptime(chunks[1], '%d.%m.%Y').date()

    print("")
    print("Дата окончания (тип дата): ")
    print(end_date)

    description = message.rpartition(' - ')[-1]
    print("Заметка: ")
    print(description)
    print("")

    try:
        cursor = cnxn.cursor()
        print("Открытие соединения")

        sqlite_select_query = "INSERT INTO Employes values('" + str(end_date) + "','" + str(description) + "')"
        #sqlite_select_query = "INSERT INTO Employes values(end_date, description)"
        cursor.execute(sqlite_select_query)

    except sqlite3.Error as error:
        print("Ошибка при чтении базы данных", error)

    finally:
        if cnxn:
            cursor.close()
            print("УСПЕШНО\nСоединение закрыто")

# САМАЯ КРАЙНЯЯ СТРОКА
bot.run(config['token'])
