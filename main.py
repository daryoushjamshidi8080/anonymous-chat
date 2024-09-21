#Librarys
from pyrogram import Client,filters
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton)
from pyromod import listen 
from Sql.mainSql import DatabaseManager
import apis
from buttons import Button
from quesfuser import Response
import random 
from profile import Profile
from seva_photo import Photo
from pyrogram.raw.types import InputFile
import os
import datetime 
from datetimer import Time 
from csv_manager import CSVManager
from search_user import SearchUsers
from message_manager import MessageManager
from block_users import Blockusers


# Database connection
db_manager = DatabaseManager(
    dbname='anonymouschat',
    user='postgres',
    password='12345',
    host='127.0.0.1',
    port='5432'
)


# Bot initialization
bot = Client(
    apis.bot_name,
    api_id=apis.app_api_id,
    api_hash=apis.app_api_hash,
    bot_token=apis.bot_api_hash
    )



# Object Buttom class
Button = Button()
# Object Response from user
response = Response()
# Object Profile
profile = Profile()
# Object save photo 
photo = Photo()
# Object datetimer 
time = Time()
# Object search users
Search_users = SearchUsers(db_manager=db_manager)
# Object Message Manager
message_manager = MessageManager(db_manager,Button)
# Object Block users
block_user = Blockusers(db_manager=db_manager)


# dictionary waiting usersall
dict_waiting_all = {}
# dictionary waiting girl
dict_waiting_girl = {}
# dictionary waiting boy
dict_waiting_boy = {}



#global variable for waiting for the  photo 
is_waiting_for_photo = False
#global variable for set chat id Profile changer
photo_chat_id = None
# A variable to store private chat status
private_chats = []





# Object CSV file manager 
csv_manager = CSVManager('/home/daryoush/Codes/chatAnonymous/connected_paris.csv')


@bot.on_message(filters.command("anonymous"))
async def handle_message(client, message):
    print(message)



#command start bot
@bot.on_message(filters.command("start"))
async def main(client, message):
    # print(message.command[1])

    # Check if you already exist or not
    return_id = db_manager.fetch_chat_id(message.chat.id)
    command_anonymous = message.command if len(message.command)!=1 else None
    
    #send message anonymus for  user
    if return_id and  command_anonymous:
        point_show_id = message.command[1] # show id point user
        sender_chat_id = message.chat.id # chat id sender user

        await message_manager.send_anonymous_message(client, sender_chat_id, point_show_id)#method send message anonymous
        
    elif command_anonymous:
        sender_chat_id =  message.chat.id
        point_show_id = message.command[1] # show id point user

        #defult create new profile for user
        name = 'پچ پچ چت'
        gender = 'boy'
        age = 0

        
        
        await message_manager.send_anonymous_message(client, sender_chat_id, point_show_id)#method send message anonymous
        await message.reply_text('''برای استفاده بیشتر از این ربات پروفایل خودرا تکمیل کنید
                                 `درصپوت تکمیل نکردن در جستجوی ها به مشکل میخورید`
                                 ''')
    #start bot  
    elif return_id:
        await message.reply_text(f"""
                     برات چکار کنم حالا{return_id[0][0]} ؟
    `از منوی پایین 👇 انتخاب کن`
    """,reply_markup=Button.menu_start())
    else:
        
        #Create new Accont(start new bot)
        await message.reply_text(f"""☺️`سلام به پچ پچ چت خوش اومدی خودتو معرفی میکنی؟`""")    
        await message_manager.get_new_data_for_pro(bot, message)

        
        #send Newly created profile to user
        await message.reply_text('profile', reply_markup=Button.menu_profile())

        #Performance request from user 
        await message.reply_text(f"""
                    برات چکار کنم حالا؟
    `از منوی پایین 👇 انتخاب کن`
    """,reply_markup=Button.menu_start())
        




#Connect to chat button
@bot.on_message(filters.text | filters.photo | filters.animation | filters.video | filters.sticker)
async def connect_chat_button(client, message):
    global is_waiting_for_photo, photo_chat_id , private_chats, dict_waiting_all, dict_waiting_boy, dict_waiting_girl, dict_waiting_boy


    # start commands /user for call user profile
    if message.text and message.text.startswith("/user_"):
        command_id = (message.text)[1:]
        fetch_prof_of_show_id = (db_manager.fetch_user_id_of_show_id(command_id))[0][0]


        await profile.profile_user(client, db_manager, message, Button, user_id = fetch_prof_of_show_id)
    # Review photo submission pending for profile change
    if is_waiting_for_photo and photo_chat_id == message.chat.id:
        try:
           await photo.save_photo(message, client, db_manager)
        except Exception as e :
            await message.reply_text(f'خطا در بارگزاری عکس{e}')
        finally:
            # After saving the photo, return the mode to inactive mode
            is_waiting_for_photo = False
            photo_chat_id = None
    



    text = message.text
    # Check if the user is chatting or not
    if csv_manager.is_chat_in_csv(message.chat.id) :

        protect_content = False
        if message.chat.id in private_chats:
            protect_content = True

        if message.text in ['پایان چت', 'فعال سازی چت خصوصی', 'نمایش پروفایل', 'غیرفعال سازی چت خصوصی']:
            pass
        else:
            # manage send message user
            await message_manager.manage_send_message(client, message, csv_manager, protect_content)
        # buttons chating 
        if text == 'نمایش پروفایل':
            #search partner id of chat id is csv file
            partner_id = csv_manager.search_partner_id(message.chat.id)
            # await message.reply_text(f'{partner_id}')
            await profile.profile_user(client, db_manager, message, Button, chat_id = partner_id)
            await client.send_message(partner_id,'پروفایل شمارو مشاهده کرد')
            
        elif text == 'فعال سازی چت خصوصی':
            private_chats.append(message.chat.id)
            await client.send_message(message.chat.id, "چت خصوصی فعال شد. پیام‌ها محافظت می‌شوند.", reply_markup=Button.menu_show_pro_end_caht_inactive())
        
        elif text == 'غیرفعال سازی چت خصوصی':
            private_chats.remove(message.chat.id)
            await client.send_message(message.chat.id, 'چت خصوصی غیر فعال شد', reply_markup=Button.menu_show_pro_end_caht_active())

        elif text == 'پایان چت':
            if csv_manager.search_partner_id(message.chat.id):
                #search partner id of chat id in csv file
                partner_id = csv_manager.search_partner_id(message.chat.id)
                #add user status to database (no chating)
                db_manager.add_status_user(0, message.chat.id)
                db_manager.add_status_user(0, partner_id)

                csv_manager.remove_chat_id_from_csv(message.chat.id)# remove chat id of csv file
                csv_manager.remove_chat_id_from_csv(partner_id)# remove partner id of csv file

                

                # Notification to both users
                await client.send_message(message.chat.id, "بلاکش میکنی یا بعدا وصل میشی باز", reply_markup=Button.menu_block())
                user_answer = await response.respons_text(bot,message.chat.id )
                await client.send_message(message.chat.id, "چت شما با کاربر دیگر قطع شد.", reply_markup=Button.menu_start())
                await client.send_message(partner_id, "چت شما ازطریق پارتنرتون قطع شد.", reply_markup=Button.menu_start())
            else:
                await message.reply_text("شما در حال حاضر با کسی متصل نیستید.",reply_markup=Button.menu_start())

                
            #add user to block list 
            if user_answer.text == 'بلاک کن' :
                await block_user.block_user(message ,partnaer_chat_id=partner_id, user_chat_id=message.chat.id)

                
    elif not (message.text in ['🔗 به یه ناشناس وصلم کن!', '🚸 معرفی به دوستان (سکه رایگان)', '📬 انتقادات و پیشنهادات', '📩 لینک ناشناس من', '💰 سکه', '👤 پروفایل']):
        await message.reply_text(f"""
    `از منوی پایین 👇 انتخاب کن`
    """,reply_markup=Button.menu_start())
    else:

        # Buttom chance connection
        if message.text == '🔗 به یه ناشناس وصلم کن!':
            #update time login 
            time.update_time_login(db_manager, chat_id=message.chat.id)
            await message.reply_text("""
                            به کی وصلت کنم؟`👇انتخابکن`
    """,reply_markup=Button.menu_chatـrequest())
        
        text = message.text

        # Buttom display for profile 
        if text == '👤 پروفایل':
            #update time login 
            time.update_time_login(db_manager, message.chat.id)

            await profile.profile_user(client, db_manager, message, Button)


        if text == '💰 سکه':
            #update time login 
            time.update_time_login(db_manager, message.chat.id)
            await message.reply_text("""
                    فعلا به سکه نیاز نداری برو حالشو ببر ☺️😋
    """)
            
        
        # Buttom receive for anonymous message 
        elif text == '📩 لینک ناشناس من':
            #update time login 
            time.update_time_login(db_manager, message.chat.id)
            user_id = db_manager.fetch_user_id_of_users(message.chat.id)[0][0]
            show_id = db_manager.fetch_show_id(user_id)[0][0]
            # link anonymous
            await message.reply_text(f'''
                                     هر هرحرفی که تو دلت داری با این لینک ناشناس برام بگو

                                     👇👇👇

`https://t.me/PajPajbot?start={show_id}`
''')
        
        # Bouttom for Communicate with the manager
        elif text == '📬 انتقادات و پیشنهادات':
            #update time login 
            time.update_time_login(db_manager, message.chat.id)

            #fetch show id sender 
            sender_user_id =db_manager.fetch_user_id_of_users(message.chat.id)[0][0]
            sender_show_id = db_manager.fetch_show_id(sender_user_id)[0][0]
            #method send message for support 
            await message_manager.support(client, message, sender_show_id)

        # Button for receive free coin
        if text == '🚸 معرفی به دوستان (سکه رایگان)': 
            #update time login 
            time.update_time_login(db_manager, message.chat.id)  
            await message.reply_text('به زودی...')






@bot.on_callback_query()
async def hande_callback_query(client, callback_query):

    global is_waiting_for_photo, photo_chat_id, dict_waiting_all, dict_waiting_boy, dict_waiting_girl
    chat_id = callback_query.message.chat.id # user chat id telegram


    #search anonymouse
    if callback_query.data == 'chancesearch':

        #fetch all profile user requeset
        user_data_profile = db_manager.fetch_all_profile(chat_id=chat_id)
        chat_id_user = callback_query.message.chat.id
        gender_user = user_data_profile[0][5]
    
        # Search again for the same model
        if any(callback_query.message.chat.id == int(chat_id) for chat_id, __ in list(dict_waiting_all.items()) ) :
            await callback_query.message.reply_text('چند بار میزنی دارم جستوجو میکنم')
        elif csv_manager.is_chat_in_csv(callback_query.message.chat.id):
            await callback_query.message.reply_text('شما درحال چت هستین')
        else:
            # method search anonymouse
            await Search_users.search_users(client, [chat_id_user, gender_user], dict_waiting_all, dict_waiting_boy, dict_waiting_girl)

    #search girl 
    elif callback_query.data == 'girlsearch':

        user_data_profile = db_manager.fetch_all_profile(chat_id=chat_id)
        chat_id_user = callback_query.message.chat.id
        gender_user = user_data_profile[0][5]
    
        # Search again for the same model
        if any(callback_query.message.chat.id == int(chat_id) for chat_id, __ in list(dict_waiting_girl.items()) ) :
            await callback_query.message.reply_text('چند بار میزنی دارم جستوجو میکنم')
        elif csv_manager.is_chat_in_csv(callback_query.message.chat.id):
            await callback_query.message.reply_text('شما درحال چت هستین')
        else:
            # method Search girls
            await Search_users.search_girl_user(client, [chat_id_user, gender_user], dict_waiting_girl, dict_waiting_boy, dict_waiting_all)
    
    #search boys 
    elif callback_query.data == 'boysearch':

        user_data_profile = db_manager.fetch_all_profile(chat_id=chat_id)
        chat_id_user = callback_query.message.chat.id
        gender_user = user_data_profile[0][5]
    
        # Search again for the same model
        if any(callback_query.message.chat.id == int(chat_id) for chat_id, __ in list(dict_waiting_boy.items()) ) :
            await callback_query.message.reply_text('چند بار میزنی دارم جستوجو میکنم')
        elif csv_manager.is_chat_in_csv(callback_query.message.chat.id):
            await callback_query.message.reply_text('شما درحال چت هستین')
        else:
            # method search boys
            await Search_users.search_boy_user(client, [chat_id_user, gender_user], dict_waiting_girl, dict_waiting_boy, dict_waiting_all)
            

    elif callback_query.data == 'lgbtsearch':
        await callback_query.message.reply_text('بزودی')
    elif callback_query.data == 'homesearch' :
        await callback_query.message.reply_text('بزودی')

    # Go to edit profile
    elif callback_query.data == 'editprofile':
        #update time login 
        time.update_time_login(db_manager,chat_id)
        await callback_query.message.edit_reply_markup(Button.menu_edit_profile())

    # edit name user in the database 
    elif callback_query.data == 'namechange':
        #update time login 
        time.update_time_login(db_manager,chat_id)
        await callback_query.message.reply_text('اسم جدید را بفرستید')
        resulte_response = await response.respons_text(bot, chat_id)
        new_name = resulte_response.text
        db_manager.edit_all_profile(name=new_name, chat_id=chat_id)
        await callback_query.message.reply_text('اسم شما با موفقیت تغییر یافت', reply_markup=Button.menu_start())


    # edit age user in the database
    elif callback_query.data == 'agechange':
        #update time login 
        time.update_time_login(db_manager,chat_id)
        await callback_query.message.reply_text('سن جدید را بفرستید از منوی پایین',reply_markup=Button.menu_number())
        resulte_response = await response.respons_text(bot, chat_id)
        new_age =resulte_response.text
        db_manager.edit_all_profile(age=new_age, chat_id=chat_id)
        await callback_query.message.reply_text('سن شما با موفقیت تغییر یافت', reply_markup=Button.menu_start())


    #edit province and city user in the database
    elif callback_query.data == 'citychange' or callback_query.data == 'provincechange':
        #update time login 
        time.update_time_login(db_manager,chat_id)
        await callback_query.message.reply_text('استان جدید خود را انتخاب کنید', reply_markup=Button.menu_provinces())
        resulte_response = await response.respons_text(bot, chat_id)
        new_province =resulte_response.text
        province_dict = {
                            '1': 'آذربایجان شرقی',
                            '2': 'آذربایجان غربی',
                            '3': 'اردبیل',
                            '4': 'اصفهان',
                            '5': 'البرز',
                            '6': 'ایلام',
                            '7': 'بوشهر',
                            '8': 'تهران',
                            '9': 'چهارمحال و بختیاری',
                            '10': 'خراسان جنوبی',
                            '11': 'خراسان رضوی',
                            '12': 'خراسان شمالی',
                            '13': 'خوزستان',
                            '14': 'زنجان',
                            '15': 'سمنان',
                            '16': 'سیستان و بلوچستان',
                            '17': 'فارس',
                            '18': 'قزوین',
                            '19': 'قم',
                            '20': 'کردستان',
                            '21': 'کرمان',
                            '22': 'کرمانشاه',
                            '23': 'کهگیلویه و بویراحمد',
                            '24': 'گلستان',
                            '25': 'گیلان',
                            '26': 'لرستان',
                            '27': 'مازندران',
                            '28': 'مرکزی',
                            '29': 'هرمزگان',
                            '30': 'همدان',
                            '31': 'یزد'
                    }
        for key, value in province_dict.items():
                if value == new_province:
                    province_id = key
                    break
        # await callback_query.message.reply_text('استان شما باموفقیت تغییر یافت')
        db_manager.edit_all_profile(chat_id, province=province_id)
        await callback_query.message.reply_text('شهرستان جدید خود را انتخاب کنید', reply_markup=Button.menu_city(new_province))
        answer = await response.respons_text(bot,chat_id)
        city = answer.text
        city_id = (db_manager.fetch_city_id(city))[0][0]
        print(f'province id :{province_id}, city id : {city_id}')
        db_manager.edit_all_profile(chat_id,city=city_id)
        await callback_query.message.reply_text('شهر شما باموفقیت تغییر یافت', reply_markup=Button.menu_start())
    # edit biography user in the database
    elif callback_query.data == 'biographychange':
        #update time login 
        time.update_time_login(db_manager,chat_id)
        await callback_query.message.reply_text('بیوگرافی موردنظر را بفرستید')
        resulte_response = await response.respons_text(bot, chat_id)
        new_bio = resulte_response.text
        db_manager.edit_all_profile(biography=new_bio, chat_id=chat_id)
        await callback_query.message.reply_text('بیوگرافی شما با موفقیت تغییر کرد', reply_markup=Button.menu_start())

    # edit gender user in the database
    elif callback_query.data == 'genderchange':
        time.update_time_login(db_manager,chat_id)
        await callback_query.message.reply_text('جنست  جدید را بفرستید از منوی پایین' ,reply_markup=Button.menu_gender())
        resulte_response = await response.respons_text(bot, chat_id)
        new_gender = resulte_response.text
        new_gender= 0 if new_gender== 'پسر' else 1 
        db_manager.edit_all_profile(gender=new_gender, chat_id=chat_id)
        await callback_query.message.reply_text('جنسیت شما با موفقیت تغییر یافت', reply_markup=Button.menu_start())

    # Go to edit image profile
    elif callback_query.data == 'picturechange':
        #update time login 
        time.update_time_login(db_manager,chat_id)

        if not is_waiting_for_photo :
            await callback_query.message.reply_text("عکس پروفایل جدید را ارسال کنید")
            is_waiting_for_photo = True
            photo_chat_id = callback_query.message.chat.id #caht id Profile picture sender


     # send reques chat for user of profile
    elif callback_query.data == 'chatrequestofuser':

        #send notefycation error 
        if csv_manager.is_chat_in_csv(callback_query.message.chat.id) :
            await callback_query.answer(
        text="باید چت قطع کنید برای استفاده از این بخش", 
        show_alert=True
        )
            
        else :
            user_request_user_id = db_manager.fetch_user_id_of_users(callback_query.message.chat.id)[0][0]
            user_request_show_id = db_manager.fetch_show_id(user_request_user_id)[0][0]

            #fetch show id of caption
            point_user_show_id = message_manager.fetch_show_id_of_caption(callback_query.message.caption)# show id point user

            #fetch user id of show id 
            point_user_id = db_manager.fetch_user_id_of_show_id(point_user_show_id)[0][0]
            point_chat_id = db_manager.fetch_chat_id_of_user_id(point_user_id)[0][0]

            #send request  to self
            if point_chat_id == callback_query.message.chat.id :
                await callback_query.answer(text='نمیتوانید به خودتون درخواست بدین باید به کاربر دیگری درخواستبفرستین', show_alert=True)
            elif csv_manager.is_chat_in_csv( point_chat_id):
                await callback_query.answer(text='درحال چت هست ', show_alert=True)
            else:
                #method send request to user for chat 
                await message_manager.sned_request_caht(client, callback_query, point_user_id, point_chat_id, user_request_show_id, user_request_user_id)
                    
        
    # button block user 
    elif callback_query.data == 'blockuser':

        # send notefycation error 
        if csv_manager.is_chat_in_csv(callback_query.message.chat.id) :
            await callback_query.answer(
        text="باید چت قطع کنید برای استفاده از این بخش", 
        show_alert=True
        )
        else:

            show_id = message_manager.fetch_show_id_of_caption(callback_query.message.caption)# show id point user
            #fetch user id of show id 
            point_user_id = db_manager.fetch_user_id_of_show_id(show_id)[0][0]

            #fetch chat id point user
            point_chat_id = db_manager.fetch_chat_id_of_user_id(point_user_id)[0][0]
            
            if point_chat_id == callback_query.message.chat.id :
                #send request  to self
                await callback_query.answer(text='نمی توانید خودتان را بلاک کنید', show_alert=True)
            else:

                #method block user
                await block_user.block_user(callback_query.message, partner_user_id= point_user_id, user_chat_id= callback_query.message.chat.id)

    elif callback_query.data == 'blocklist':
        await callback_query.message.reply_text('بزودی...')


    # send direct message for user
    elif callback_query.data == 'directmessage':
        if csv_manager.is_chat_in_csv(callback_query.message.chat.id):
            await callback_query.answer(
        text="باید چت قطع کنید برای استفاده از این بخش", 
        show_alert=True
        )
        else:
            #fetch show id of caption
            show_id = message_manager.fetch_show_id_of_caption(callback_query.message.caption)# show id point user
            #fetch user id of show id 
            point_user_id = db_manager.fetch_user_id_of_show_id(show_id)[0][0]
            point_user_chat_id = (db_manager.fetch_chat_id_of_user_id(point_user_id))[0][0]

            if point_user_chat_id == callback_query.message.chat.id :
                await callback_query.answer(
                    text='نمی توانید به خودتان دایرکت بفرستید',
                    show_alert=True
                )
            else:
                await callback_query.message.reply_text('پیام خود را وارد بنویسد')
                message = await response.respons_text(bot, point_user_chat_id)
                await message_manager.send_message_direct(client, callback_query, point_user_id, message.text,callback_query.message.chat.id)
            
            
    # report partner
    elif callback_query.data == 'reportuser':
        if csv_manager.is_chat_in_csv(callback_query.message.chat.id):
            await callback_query.answer(
        text="باید چت قطع کنید برای استفاده از این بخش", 
        show_alert=True
        )
            

    #block sender user direct
    elif callback_query.data == 'blocksenddirect':
        show_id = message_manager.fetch_show_id_of_caption(callback_query.message.text)# show id point user
        #fetch user id of show id 
        point_user_id = db_manager.fetch_user_id_of_show_id(show_id)[0][0]

        #method block user
        await block_user.block_user(callback_query.message, partner_user_id= point_user_id, user_chat_id= callback_query.message.chat.id)


    # Send a reply to Direct
    elif callback_query.data == 'sendanswer':
        #fetch show id of caption
        show_id = message_manager.fetch_show_id_of_caption(callback_query.message.text)# show id point user
        #fetch user id of show id 
        point_user_id = db_manager.fetch_user_id_of_show_id(show_id)[0][0]
        point_user_chat_id = (db_manager.fetch_chat_id_of_user_id(point_user_id))[0][0]
        
        await callback_query.message.reply_text('پیام خود را وارد بنویسد')
        message = await response.respons_text(bot, point_user_chat_id)#Waiting for a reply user

        # methode send message for direct 
        await message_manager.send_message_direct(client, callback_query, point_user_id, message.text,callback_query.message.chat.id)
        
    elif callback_query.data == 'blockrequest':

        point_user_show_id = message_manager.fetch_show_id_of_caption(callback_query.message.text)# show id point user
        
        #fetch user id of show id 
        point_user_id= db_manager.fetch_user_id_of_show_id(point_user_show_id)[0][0]

        #method block user
        await block_user.block_user(callback_query.message, partner_user_id= point_user_id, user_chat_id= callback_query.message.chat.id)


    # accept request chat at point user
    elif callback_query.data == 'acceptrequest':

        point_user_show_id =message_manager.fetch_show_id_of_caption(callback_query.message.text)# show id point user

        #fetch user id of show id 
        point_user_id= db_manager.fetch_user_id_of_show_id(point_user_show_id)[0][0]
        point_user_chat_id = db_manager.fetch_chat_id_of_user_id(point_user_id)[0][0]
        
        #send notifiycation for user sender 
        if csv_manager.is_chat_in_csv(point_user_chat_id):
            await callback_query.answer(text=' درحال چت هست نمی توانید به شما وصل شود', show_alert= True)

        else:
        
            await message_manager.accept_request_chat(client, callback_query.message.chat.id, point_user_chat_id)


    # Rejection of the request
    elif callback_query.data == 'rejectrequest':
                
        point_user_show_id =message_manager.fetch_show_id_of_caption(callback_query.message.text)# show id point user

        #fetch user id of show id 
        point_user_id= db_manager.fetch_user_id_of_show_id(point_user_show_id)[0][0]
        point_user_chat_id = db_manager.fetch_chat_id_of_user_id(point_user_id)[0][0]

        await message_manager.reject_request(client, callback_query, point_user_chat_id, callback_query.message.chat.id)
        
    #Reply to anonymous message
    elif callback_query.data == 'responsanonymous':
        point_user_id = int(message_manager.fetch_user_id_of_text(callback_query.message.text))
        
        #fetch caht id of user id 
        point_chat_id = db_manager.fetch_chat_id_of_user_id(point_user_id)[0][0]

        # fetch show id point user
        point_show_id = db_manager.fetch_show_id(point_user_id)[0][0]

        # method send message anonymous of class messsage menager 
        await message_manager.send_anonymous_message(client, callback_query.message.chat.id, point_show_id)

bot.run()
