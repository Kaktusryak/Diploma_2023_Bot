import time
import logging
import datetime

import openai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup,KeyboardButton, \
InlineKeyboardMarkup,InlineKeyboardButton

import requests
import json
import re

storage = MemoryStorage()

isLogged = False
UserId = -1

UserNickname = ''

openai.api_key="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"


class Advice(StatesGroup):
    SPick = State()

class Add(StatesGroup):
    State1 = State()

class Remove(StatesGroup):
    State1 = State()

class BetterRemove(StatesGroup):
    State1 = State()
    State2 = State()

class Log(StatesGroup):
    State1 = State()
    State2 = State()

class Reg(StatesGroup):
    State1 = State()
    State2 = State()

class Search(StatesGroup):
    Result = State()
    AddC = State()

class SearchA(StatesGroup):
    ResultA = State()
    AddCA = State()

class SearchU(StatesGroup):
    ResultU = State()
    ResultC = State()

class Top(StatesGroup):
    State1 = State()
    State2 = State()
    


cancel_button = (KeyboardButton('!Cancel'))
help_button = (KeyboardButton('/help'))  
log_button = (KeyboardButton('/log'))
add_button = (KeyboardButton('/add'))
advice_button = (KeyboardButton('/advice'))
search_button = (KeyboardButton('/search'))
searchA_button = (KeyboardButton('/search_actor'))
searchU_button = (KeyboardButton('/search_user'))
reg_button = (KeyboardButton('/reg'))
start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb.add(help_button).add(log_button).add(reg_button).add(add_button).add(advice_button).add(search_button).add(searchA_button).add(searchU_button)

film_button = (KeyboardButton('Movie'))
series_button = (KeyboardButton('Series'))
cartoon_button = (KeyboardButton('Cartoon'))
game_button = (KeyboardButton('Game'))
book_button = (KeyboardButton('Book'))
other_button = (KeyboardButton('Any'))
advice_kb = ReplyKeyboardMarkup(resize_keyboard=True)
advice_kb.add(cancel_button).add(film_button).add(series_button).add(cartoon_button).add(book_button).add(game_button).add(other_button)



cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_kb.add(cancel_button)


top_kb = ReplyKeyboardMarkup(resize_keyboard=True)
top_kb.add(cancel_button).add(other_button).add(film_button).add(series_button).add(cartoon_button).add(book_button).add(game_button)






TOKEN = "5991785308:AAEAd-VVOpooal_hBluqvSYBC07crDyT6nY"

MSG = "If you forgot, your name is {}"

bot = Bot(token = TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())





#----------------------START
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_Name = message.from_user.full_name
    logging.info(f'{user_id=} {user_Name=} {time.asctime()}')
    await message.reply(f"Hello, {user_Name}!" ,  reply_markup = start_kb)


#----------------------remove
@dp.message_handler(commands=['remove'])
async def start_handler(message: types.Message):
    global isLogged
    global UserId
    global UserNickname
    if(isLogged):
        response = requests.get('https://localhost:7117/api/user/'+str(UserId),verify=False)
        data=response.text
        Answer='Your ['+UserNickname+'] content: \n'
        remove_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        remove_kb.add("!Cancel")
        parse_data=json.loads(data)
        for item in parse_data['contentViewModels']:
            Answer+="["+item['contentCategory']+"] "+item['name']+ ", " +item['releaseDate'][0:4]+" [id="+str(item['id'])+"]"+'\n'
            remove_kb.add("Remove "+ item['name'] + " [id="+str(item['id'])+"]")
        await message.reply(Answer,reply_markup=remove_kb)
        await BetterRemove.first()
    else:
        await message.reply(f"You are not logged")

@dp.message_handler( state=BetterRemove.State1)
async def add_handler(message: types.Message, state: FSMContext):
    if(message.text == '!Cancel'):
        a = ReplyKeyboardRemove()
        await message.reply('Action canceled',reply_markup=a)
        await state.finish()
    else:
        url = 'https://localhost:7117/api/user/deleteContent'
        regex = re.compile("\=(.*)\]")
        id = regex.findall(message.text)
        Id = id[0]
        await message.reply(Id)
        myobj={'userId':UserId,'contentId':int(Id)}
        response = requests.post(url,json=myobj,verify=False)
        if(response.status_code==200):
            await message.reply('Content successfully removed!\nTo exit this action press [!Cancel]')
        else:
            await message.reply('Something went wront\nProbably wrong id',reply_markup=a)
            await state.finish()


#----------------------REMOVE_id

@dp.message_handler(commands=['remove_id'], state=None)
async def start_handler(message: types.Message, state: FSMContext):
    
    global isLogged
    if(isLogged):
        await message.reply(f"Type the id of the searching content:\nId can be fount by looking though your library [/me]\nTo exit this action press [!Cancel]",reply_markup = cancel_kb)
        await Remove.first()
    else:
        await message.reply(f"You should be logged in to remove content from your favorites")
    

@dp.message_handler( state=Remove.State1)
async def add_handler(message: types.Message, state: FSMContext):
    if(message.text == '!Cancel'):
        a = ReplyKeyboardRemove()
        await message.reply('Action canceled',reply_markup=a)
        await state.finish()
    else:
        try:
            url = 'https://localhost:7117/api/user/deleteContent'
        
            myobj={'userId':UserId,'contentId':int(message.text)}
            response = requests.post(url,json=myobj,verify=False)
            if(response.status_code==200):
                await message.reply('Content successfully removed!\nTo exit this action press [!Cancel]',reply_markup=cancel_kb)
                
            else:
                await message.reply('Something went wront\nProbably wrong id\nTo exit this action press [!Cancel]',reply_markup=cancel_kb)
        except:
            await message.reply('Something went wront\nProbably wrong id\nTo exit this action press [!Cancel]',reply_markup=cancel_kb)


#----------------------TOP20

@dp.message_handler(commands=['top'], state=None)
async def start_handler(message: types.Message, state: FSMContext):
   
    await message.reply(f"Choose which category top 20 you want to see:\n",reply_markup = top_kb)
    await Top.first()

@dp.message_handler( state=Top.State1)
async def add_handler(message: types.Message, state: FSMContext):
    a = ReplyKeyboardRemove()
    answer = message.text
    match answer:
        case "!Cancel":
            await message.reply("Action canceled", reply_markup=a)
            await state.finish()
        case "Any":
            response = requests.get('https://localhost:7117/api/content/gettop20',verify=False)
        case "Movie":
            response = requests.get('https://localhost:7117/api/content/gettop20/1',verify=False)
        case "Series":
            response = requests.get('https://localhost:7117/api/content/gettop20/2',verify=False)
        case "Cartoon":
            response = requests.get('https://localhost:7117/api/content/gettop20/3',verify=False)
        case "Game":
            response = requests.get('https://localhost:7117/api/content/gettop20/4',verify=False)
        case "Book":
            response = requests.get('https://localhost:7117/api/content/gettop20/5',verify=False)
        case _:
            response = requests.get('https://localhost:7117/api/content/gettop20',verify=False)
    
    if(response.status_code!=200):
        await message.reply('Something went wrong!')
        await state.finish()
    else:
        content_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        content_kb.add("!Cancel")
        data=response.text
        Answer='Top 20:\n'
        parse_data=json.loads(data)
        for item in parse_data:
            Answer+="["+item['contentCategory']+"] "+item['name']+ ", " +item['releaseDate'][0:4]+" [id="+str(item['id'])+"]"+'\n'
            content_kb.add("Add "+ item['name'] + " [id="+str(item['id'])+"]")
        
        await message.reply(Answer,reply_markup=content_kb)
        await Top.next()

@dp.message_handler( state=Top.State2)
async def add_handler(message: types.Message, state: FSMContext):
    url = 'https://localhost:7117/api/user/addContent'
    a = ReplyKeyboardRemove()
    global isLogged
    if(message.text == '!Cancel'):
        
        await message.reply('Action canceled',reply_markup=a)
        await state.finish()
    else:
        if(isLogged):
            try:
                regex = re.compile("\=(.*)\]")
                id = regex.findall(message.text)
                Id = id[0]
                myobj={'userId':UserId,'contentId':int(Id)}
                response = requests.post(url,json=myobj,verify=False)
                if(response.status_code==200):
                    await message.reply('Content successfully added!\nTo exit this action press [!Cancel]') 
                else:
                    await message.reply('Something went wront\nProbably wrong id',reply_markup=a)
                    await state.finish()
            except:
                await message.reply('Something went wront\nProbably wrong id',reply_markup=a)
                await state.finish()
        else:
            await message.reply('You are not logged, please log in and try again',reply_markup=a)
            await state.finish()
                 



#----------------------ME
@dp.message_handler(commands=['me'])
async def start_handler(message: types.Message):
    global isLogged
    global UserId
    global UserNickname
    if(isLogged):
        response = requests.get('https://localhost:7117/api/user/'+str(UserId),verify=False)
        if(response.status_code!=200):
            await message.reply('Something went wrong!')
        else:
            data=response.text
            Answer='Your ['+UserNickname+'] content: \n'
            
            parse_data=json.loads(data)
            for item in parse_data['contentViewModels']:
                Answer+="["+item['contentCategory']+"] "+item['name']+ ", " +item['releaseDate'][0:4]+" [id="+str(item['id'])+"]"+'\n'
            await message.reply(Answer)
    else:
        await message.reply(f"You are not logged")
    


#-----------------------HELP

@dp.message_handler(commands=['help'], state=None)
async def start_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await message.reply(f"Hello, this is Norator bot!\nYou can use the following comands to interact with me:\n/start [To activate bot and see all possible commands]\n/help [This is where you are]\n/advice [To get an advice of what to watch from our AI friend]\n/add_id [To add content to your favorites by its id]\n/remove_id [To remove content from your favorites by its id]\n/remove [To remove content from your favorites]\n/search [To search content by its title and add titles to your profile favorites]\n/search_actor [To search content by its actor name and add titles to your profile favorites]\n/search_user [To search other user profiles by their nicknames]\n/me [To see your profile favorites]\n/top [To see top 20 of content (including category filter)]")
    
#----------------------ADD_id
@dp.message_handler(commands=['add_id'], state=None)
async def start_handler(message: types.Message, state: FSMContext):
    global isLogged
    if(isLogged):
        await message.reply(f"Type the id of the searching content:\nId can be fount by searching the content you want to add",reply_markup = cancel_kb)
        await Add.first()
    else:
        await message.reply(f"You should be logged in to add content to your favorites")
    

@dp.message_handler( state=Add.State1)
async def add_handler(message: types.Message, state: FSMContext):
    url = 'https://localhost:7117/api/user/addContent'
    if(message.text == '!Cancel'):
        a = ReplyKeyboardRemove()
        await message.reply('Action canceled',reply_markup=a)
        await state.finish()
    else:
        try:
            myobj={'userId':UserId,'contentId':int(message.text)}
            response = requests.post(url,json=myobj,verify=False)
            if(response.status_code==200):
                await message.reply('Content successfully added!\nTo exit this action press [!Cancel]',reply_markup=cancel_kb)
                
            else:
                await message.reply('Something went wront\nProbably wrong id\nTo exit this action press [!Cancel]',reply_markup=cancel_kb)
        except:
            await message.reply('Something went wront\nProbably wrong id\nTo exit this action press [!Cancel]',reply_markup=cancel_kb)
            
    
    




#----------------------SEARCH
@dp.message_handler(commands=['search'], state=None)
async def start_handler(message: types.Message, state: FSMContext):
    
    await message.reply(f"Type the title of the searching content:\n",reply_markup = cancel_kb)
    await Search.first()
    

@dp.message_handler( state=Search.Result)
async def add_handler(message: types.Message, state: FSMContext):
    if(message.text == '!Cancel'):
        a = ReplyKeyboardRemove()
        await message.reply('Action canceled',reply_markup=a)
        await state.finish()
    else:


        url = 'https://localhost:7117/api/content/getall?FilterParam='+message.text +'&PageNumber=1&PageSize=20'
        user_id = message.from_user.id
        
        response = requests.get(url,verify=False)
        data=response.text
        Answer='Titles we have found:\n'
        parse_data=json.loads(data)
        content_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        content_kb.add("!Cancel")
        for item in parse_data['entities']:
            Answer+="["+item['contentCategory']+"] "+item['name']+ ", " +item['releaseDate'][0:4]+"[id="+str(item['id'])+"]"+'\n'
            response1 = requests.get('https://localhost:7117/api/content/' + str(item['id']),verify=False)
            content_kb.add("Add "+ item['name'] + " [id="+str(item['id'])+"]")
            data1 = response1.text
            parse_data1 = json.loads(data1)
            for item in parse_data1['genreViewModels']:
                Answer+= "* "+item['name'] + '\n'
            for item in parse_data1['actorsViewModels']:
                Answer+= "> "+item['name'] + '\n'

        if(Answer=='Titles we have found:\n'):
            Answer='Nothing have been found'       
        await message.reply(Answer +  '\n',reply_markup=content_kb)
        await Search.next()

@dp.message_handler( state=Search.AddC)
async def add_handler(message: types.Message, state: FSMContext):
    url = 'https://localhost:7117/api/user/addContent'
    a = ReplyKeyboardRemove()
    global isLogged
    if(message.text == '!Cancel'):
        
        await message.reply('Action canceled',reply_markup=a)
        await state.finish()
    else:
        if(isLogged):
            try:
                regex = re.compile("\=(.*)\]")
                id = regex.findall(message.text)
                Id = id[0]
                myobj={'userId':UserId,'contentId':int(Id)}
                response = requests.post(url,json=myobj,verify=False)
                if(response.status_code==200):
                    await message.reply('Content successfully added!\nTo exit this action press [!Cancel]')
                else:
                    await message.reply('Something went wront\nProbably wrong id',reply_markup=a)
                    await state.finish()
            except:
                await message.reply('Something went wront\nProbably wrong id',reply_markup=a)
                await state.finish()
        else:
            await message.reply('You are not logged, please log in and try again',reply_markup=a)
            await state.finish()

#----------------------SEARCH_ACTOR
@dp.message_handler(commands=['search_actor'], state=None)
async def start_handler(message: types.Message, state: FSMContext):
    
    await message.reply(f"Type the Actor of the searching content:\n",reply_markup = cancel_kb)
    await SearchA.first()
    

@dp.message_handler( state=SearchA.ResultA)
async def add_handler(message: types.Message, state: FSMContext):
    if(message.text == '!Cancel'):
        a = ReplyKeyboardRemove()
        await message.reply('Action canceled',reply_markup=a)
        await state.finish()
    else:
        url = 'https://localhost:7117/api/content/getall?ActorName='+message.text +'&PageNumber=1&PageSize=20'
        user_id = message.from_user.id
        
        response = requests.get('https://localhost:7117/api/content/getall?ActorName='+message.text+'&PageNumber=1&PageSize=20',verify=False)
        data=response.text
        Answer='Titles we have found:\n'
        parse_data=json.loads(data)
        content_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        content_kb.add("!Cancel")
        for item in parse_data['entities']:
            Answer+="["+item['contentCategory']+"] "+item['name']+ ", " +item['releaseDate'][0:4]+" [id="+str(item['id'])+"]"+'\n'
            response1 = requests.get('https://localhost:7117/api/content/' + str(item['id']),verify=False)
            content_kb.add("Add "+ item['name'] + " [id="+str(item['id'])+"]")
            data1 = response1.text
            parse_data1 = json.loads(data1)
            #await message.reply(parse_data1['actorsViewModels'])
            for item in parse_data1['genreViewModels']:
                Answer+= "* "+item['name'] + '\n'
            for item in parse_data1['actorsViewModels']:
                Answer+= "> "+item['name'] + '\n'
            
        if(Answer=='Titles we have found:\n'):
            Answer='Nothing have been found'       
        await message.reply(Answer +  '\n', reply_markup=content_kb)
        await SearchA.next()   


@dp.message_handler( state=SearchA.AddCA)
async def add_handler(message: types.Message, state: FSMContext):
    url = 'https://localhost:7117/api/user/addContent'
    a = ReplyKeyboardRemove()
    global isLogged
    if(message.text == '!Cancel'):
        
        await message.reply('Action canceled',reply_markup=a)
        await state.finish()
    else:
        if(isLogged):
            try:
                regex = re.compile("\=(.*)\]")
                id = regex.findall(message.text)
                Id = id[0]
                myobj={'userId':UserId,'contentId':int(Id)}
                response = requests.post(url,json=myobj,verify=False)
                if(response.status_code==200):
                    await message.reply('Content successfully added!\nTo exit this action press [!Cancel]')
                else:
                    await message.reply('Something went wront\nProbably wrong id',reply_markup=a)
                    await state.finish()
            except:
                await message.reply('Something went wront\nProbably wrong id',reply_markup=a)
                await state.finish()
        else:
            await message.reply('You are not logged, please log in and try again',reply_markup=a)
            await state.finish()
                
    
#----------------------SEARCH_USER
@dp.message_handler(commands=['search_user'], state=None)
async def start_handler(message: types.Message, state: FSMContext):
    
    await message.reply(f"Type the Nickname of the searching user:\n",reply_markup = cancel_kb)
    await SearchU.first()
    

@dp.message_handler( state=SearchU.ResultU)
async def add_handler(message: types.Message, state: FSMContext):
    if(message.text == '!Cancel'):
        a = ReplyKeyboardRemove()
        await message.reply('Action canceled',reply_markup=a)
        await state.finish()
    else:


        user_id = message.from_user.id
        response = requests.get('https://localhost:7117/api/user/getall?FilterParam='+message.text+'&PageNumber=1&PageSize=999',verify=False)
        data=response.text
        Answer='Users we have found:\n'
        users=[]
        users.append(KeyboardButton("!Cancel"))
        parse_data=json.loads(data)
        for item in parse_data['entities']:
            Answer+=item['nickName']+" [id="+str(item['id'])+"]"+'\n'
            users.append(KeyboardButton( item['nickName']+" [id="+str(item['id'])+"]"))
        users_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        for i in users:
            users_kb.add(i)

        if(Answer=='Users we have found:\n'):
            Answer='Nothing have been found'   
            await state.finish()    
        else:

            await message.reply(Answer +  '\n')
            await bot.send_message(user_id, 'Choose one of the wollowing users:',reply_markup = users_kb)
            await SearchU.next()   
        
    
@dp.message_handler( state=SearchU.ResultC)
async def add_handler(message: types.Message, state: FSMContext):
    a = ReplyKeyboardRemove()
    if(message.text == "!Cancel"):
        await message.reply("Action canceled",reply_markup=a)
        await state.finish()
    else:
        user_id = message.from_user.id
        regex = re.compile("\=(.*)\]")
        id = regex.findall(message.text)
        Id = id[0]
        response = requests.get('https://localhost:7117/api/user/'+Id,verify=False)
        data=response.text
        Answer='Content of the user: '
        parse_data=json.loads(data)
        Answer+=parse_data['nickName']+'\n'
        for item in parse_data['contentViewModels']:
            Answer+="["+item['contentCategory']+"] "+item['name']+ ", " +item['releaseDate'][0:4]+" [id="+str(item['id'])+"]"+'\n'
        await message.reply(Answer +  '\n',reply_markup=a)
        
        
        await state.finish()   
        
    
#--------------------ADVICE


@dp.message_handler(commands=['advice'], state=None)
async def start_handler(message: types.Message, state: FSMContext):
   
    await message.reply(f"Choose wether you want to watch movie, series or cartoon:\n",reply_markup = advice_kb)
    await Advice.first()


@dp.message_handler(state=Advice.SPick)
async def advice_pick_handler(message: types.Message, state: FSMContext):
    a = ReplyKeyboardRemove()
    if(message.text=="!Cancel"):
        await message.reply("Action canceled",reply_markup=a)
        await state.finish()
    else:
        type = message.text.lower()
        user_id = message.from_user.id
        
        response = openai.Completion.create(
                    model = "text-davinci-003",
                    prompt = "Give me one title of the "+type+" to watch/read/play. Type only the title within one line",
                    temperature = 0.9,
                    max_tokens =1000,
                    top_p=1.0,
                    frequency_penalty = 0.0,
                    presence_penalty = 0.6,
                    stop=["You:"]
                ) 
        resp = response['choices'][0]['text']
        await bot.send_message(user_id,resp)


    
#-------------------------UNLOG
@dp.message_handler(commands=['unlog'], state=None)
async def log_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    global isLogged
    global UserId
    global UserNickname
    if(isLogged):
        UserNickname = ''
        isLogged = False
        UserId = -1
        await bot.send_message(user_id,'You were unlogged')
    else:
        await bot.send_message(user_id,'You can not be unlogged because you were not logged')
    

#-------------------------LOG
@dp.message_handler(commands=['log'], state=None)
async def log_handler(message: types.Message, state: FSMContext):
    
    global isLogged
    user_id = message.from_user.id

    if(isLogged):
        await bot.send_message(user_id,'You already logged')
    else:
        await bot.send_message(user_id,'Enter login:',reply_markup = cancel_kb)
        await Log.first()

@dp.message_handler(state=Log.State1)
async def title_handler(message: types.Message, state: FSMContext):
    if(message.text == '!Cancel'):
        a = ReplyKeyboardRemove()
        await message.reply('Action canceled',reply_markup=a)
        await state.finish()
    else:
        user_id = message.from_user.id
        
        if(message.text):
            
            
            await state.update_data(Login = message.text)
            await bot.send_message(user_id,'Enter password:')
            await Log.next()

        else:
            await bot.send_message(user_id,'You typed incorrect login, retry to log-in')
            await state.finish()

@dp.message_handler(state=Log.State2)
async def title_handler(message: types.Message, state: FSMContext):
    
    user_id = message.from_user.id
    global isLogged, UserId,UserNickname
    if(message.text):
        
        
        await state.update_data(Password = message.text)
        data=await state.get_data()
        Login = data.get("Login")
        response = requests.get('https://localhost:7117/api/user/login?NickName='+ Login+'&Password='+message.text, verify=False)
        if(response.status_code==200):

            data=response.text
            parse_data = json.loads(data)
            UID = parse_data['id']
            isLogged=True
            UserId = UID
            UserNickname = parse_data['nickName']
            await bot.send_message(user_id,f'You logged as {UserNickname}')
            await state.finish()
        else:
            await bot.send_message(user_id,'Wrong Login or Password')
            await state.finish()
    else:
        await bot.send_message(user_id,'You typed incorrect password')
        await state.finish()


#-------------------------Register
@dp.message_handler(commands=['reg'], state=None)
async def log_handler(message: types.Message, state: FSMContext):
    global isLogged
    user_id = message.from_user.id

    await bot.send_message(user_id,'Enter login:',reply_markup = cancel_kb)
    await Reg.first()

@dp.message_handler(state=Reg.State1)
async def title_handler(message: types.Message, state: FSMContext):
    
    user_id = message.from_user.id
    if(message.text == '!Cancel'):
        a = ReplyKeyboardRemove()
        await message.reply('Action canceled',reply_markup=a)
        await state.finish()
    else:
        if(message.text):   
            await state.update_data(Login = message.text)
            await bot.send_message(user_id,'Enter password:',reply_markup = cancel_kb)
            await Reg.next()

        else:
            await bot.send_message(user_id,'You typed incorrect login, retry to log-in')
            await state.finish()

@dp.message_handler(state=Reg.State2)
async def title_handler(message: types.Message, state: FSMContext):
    
    user_id = message.from_user.id
    global isLogged, UserId,UserNickname
    if(message.text == '!Cancel'):
        a = ReplyKeyboardRemove()
        await message.reply('Action canceled',reply_markup=a)
        await state.finish()
    else:
        if(message.text):
            
            
            await state.update_data(Password = message.text)
            data=await state.get_data()
            Login = data.get("Login")
            myObj={'nickName':Login,"dateOfBirth": "2003-04-03T14:48:05.705Z",'password':message.text}
            url = 'https://localhost:7117/api/user/createUser'
            response = requests.post(url, json=myObj,verify=False)
            if(response.status_code==200):
                await message.reply('You successfully registered!\nYou can now log-in to add content to your favorites and enjoy with Norator')
                await state.finish()
            else:
                await message.reply('Something went wront\n')
                await state.finish()
        else:
            await bot.send_message(user_id,'You typed incorrect password')
            await state.finish()



if __name__ == '__main__':
    executor.start_polling(dp)