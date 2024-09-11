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


# list waiting users
waiting_users = []


#global variable for waiting for the  photo 
is_waiting_for_photo = False
#global variable for set chat id Profile changer
photo_chat_id = None

# A variable to store private chat status
private_chats = []


# Object CSV file manager 
csv_manager = CSVManager('/home/daryoush/Codes/chatAnonymous/connected_paris.csv')


#command start bot
@bot.on_message(filters.command("start"))
async def main(client, message):

    # Check if you already exist or not
    return_id = db_manager.fetch_chat_id(message.chat.id)
    if return_id:
        await message.reply_text(f"""
                     برات چکار کنم حالا{return_id[0][0]} ؟
    `از منوی پایین 👇 انتخاب کن`
    """,reply_markup=Button.menu_start())
    else:
        #Create new Accont
        await message.reply_text(f"""☺️`سلام به پچ پچ چت خوش اومدی خودتو معرفی میکنی؟`""")    

        # Basic information user during initial check-in
        basic_information = [message.chat.id]        #name question and save the name in the database
        await message.reply_text('اسم ؟')    
        answer= await response.respons_text(bot, message.chat.id)
        name = answer.text
        basic_information.append(name)

        #age question
        await message.reply_text('سن ؟', reply_markup=Button.menu_number())
        answer = await response.respons_text(bot, message.chat.id)
        age = answer.text
        basic_information.append(age)

        #province question
        await message.reply_text('استان ؟', reply_markup=Button.menu_provinces() )
        answer = await response.respons_text(bot, message.chat.id)
        province = answer.text
        province_id = db_manager.fetch_province_id(province)
        basic_information.append(province_id[0][0])
        
        #city question
        try: 
            await message.reply_text('شهر ؟', reply_markup=Button.menu_city(province))
            answer = await response.respons_text(bot, message.chat.id)
            city = answer.text
            city_id = db_manager.fetch_city_id(city)
            basic_information.append(city_id[0][0])
        except :
            new_city = []
            new_city.append(city)
            new_city.append(province_id[0][0])
            db_manager.insert_new_city(new_city)
            city_id = db_manager.fetch_city_id(city)
            basic_information.append(city_id[0][0])

        #gender question
        await message.reply_text('جنسیت ؟', reply_markup=Button.menu_gender())
        answer = await response.respons_text(bot, message.chat.id)
        gender = answer.text
        if gender == 'دختر' :
            gender = 1
        else:
            gender = 0
        basic_information.append(gender)


        #set Basic information during initial check-in
        db_manager.insert_data_new_start(basic_information)
        #set login time 
        time.set_first_time_log(db_manager, message.chat.id)
        
        

        #create show id for new user
        try:
            user_id =db_manager.fetch_user_id_of_users(message.chat.id)
            show_id = 'user_' + str(message.chat.id)[:-4]
            data = [show_id, user_id[0][0]]
            db_manager.create_show_id(data)
        except Exception as e:
            #Duplicate show ID, a new sowh ID was created
            random_char = ['@', '%', '*', '+', '$', '!']
            x =show_id + str(random.choice(random_char))+'H'
            print('Duplicate ID, a new ID was created error is : ', x)
            
        
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
    global waiting_users
    global is_waiting_for_photo, photo_chat_id , private_chats


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
            #search partner id of chat id is csv file
            partner_id = csv_manager.search_partner_id(message.chat.id)
            if message.text:
                await client.send_message(partner_id, message.text, protect_content=protect_content)
            elif message.animation:
                await client.send_animation(partner_id, message.animation.file_id,protect_content=protect_content)
            elif message.photo:
                await client.send_photo(partner_id, message.photo.file_id, protect_content=protect_content )
            elif message.sticker:
                await client.send_sticker(partner_id, message.sticker.file_id, protect_content=protect_content )
            elif message.video:
                await client.send_video(partner_id, message.video.file_id, protect_content=protect_content )
                

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

                #user_id of user request
                user_id = int((db_manager.fetch_user_id_of_users(message.chat.id))[0][0])
                partner_user_id = int((db_manager.fetch_user_id_of_users(partner_id))[0][0])
                
                # set ids to table 
                db_manager.set_id_to_block_list(partner_user_id, user_id)
                db_manager.set_id_to_block_list(user_id, partner_user_id)

                
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
            await message.reply_text("""anonymous link""")
        
        # Bouttom for Communicate with the manager
        elif text == '📬 انتقادات و پیشنهادات':
            #update time login 
            time.update_time_login(db_manager, message.chat.id)
            await message.reply_text("""support""")
            # ارسال پیام اخطار
        # Button for receive free coin
        if text == '🚸 معرفی به دوستان (سکه رایگان)': 
            #update time login 
            time.update_time_login(db_manager, message.chat.id)  
            await message.reply_text('به زودی...')


        print(waiting_users)
   




@bot.on_callback_query()
async def hande_callback_query(client, callback_query):

    global is_waiting_for_photo, photo_chat_id, waiting_users

    chat_id = callback_query.message.chat.id

    if callback_query.data == 'chancesearch':

        #fetch all profile user requeset
        user_data_profile = db_manager.fetch_all_profile(chat_id=chat_id)

        # Search again for the same model
        if any(csv_manager.is_chat_in_csv(callback_query.message.chat.id) == key for key, _ in waiting_users ) :
            await callback_query.message.reply_text('چند بار میزنی دارم جستوجو میکنم')
        elif csv_manager.is_chat_in_csv(callback_query.message.chat.id):
            await callback_query.message.reply_text('شما درحال چت هستین')
        else:
            # If there is a user in the waiting list, log in
            print(waiting_users)
            if waiting_users:
                #user request name
                user_name = user_data_profile[0][0]

                partner_id = waiting_users[0]

                #fatch all profile partner 
                partner_data_profile = db_manager.fetch_all_profile(chat_id=partner_id[0])

                # partner name 
                partner_name  = partner_data_profile[0][0]
                
                #check block lsit
                user_id = int((db_manager.fetch_user_id_of_users(callback_query.message.chat.id))[0][0])
                partner_user_id = int((db_manager.fetch_user_id_of_users(partner_id[0]))[0][0])
                    
                print(user_id)
                try:
                    fetch_block_id = (db_manager.fetch_block_id(user_id))[0][0]#fetch bluck id of block table
                except:
                    fetch_block_id = None
            
                #add user to chat with the partner
                if not(fetch_block_id == partner_user_id) :

                    waiting_users.pop(0)
                    
                    csv_manager.add_to_data([chat_id, partner_id[0]])
                    csv_manager.add_to_data([partner_id[0], chat_id])

                    #add user status to database (chating)
                    db_manager.add_status_user(2, chat_id)
                    db_manager.add_status_user(2, partner_id[0])



                    await client.send_message(chat_id, f"شما با کاربر  {partner_name}: متصل شدید.", reply_markup=Button.menu_show_pro_end_caht_active())
                    await client.send_message(partner_id[0], f"شما با کاربر {user_name} متصل شدید.", reply_markup=Button.menu_show_pro_end_caht_active())
                else:
                    # gender request user
                    gender = user_data_profile[0][5]
                    # add user to list waiting chat 
                    waiting_users.append((chat_id,gender))
                    await callback_query.message.reply_text("شما در صف انتظار قرار گرفتید. منتظر بمانید تا کاربر دیگری درخواست اتصال دهد .")

                    

            else:
                # gender request user
                gender = user_data_profile[0][5]
                # add user to list waiting chat 
                waiting_users.append((chat_id,gender))
                await callback_query.message.reply_text("شما در صف انتظار قرار گرفتید. منتظر بمانید تا کاربر دیگری درخواست اتصال دهد .")


    elif callback_query.data == 'girlsearch':
        await callback_query.message.reply_text('جستوجوی دختر')
        await callback_query.answer(
            text="This is an alert!", 
            show_alert=True
        )
    elif callback_query.data == 'boysearch':
        await callback_query.message.reply_text('جستوجوی پسر')
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

    # chat requestofuser for user
    elif callback_query.data == 'chatrequestofuser':
        if csv_manager.is_chat_in_csv(callback_query.message.chat.id) :
            await callback_query.answer(
        text="باید چت قطع کنید برای استفاده از این بخش", 
        show_alert=True
        )
    # button block user 
    elif callback_query.data == 'blockuser':
        if csv_manager.is_chat_in_csv(callback_query.message.chat.id) :
            await callback_query.answer(
        text="باید چت قطع کنید برای استفاده از این بخش", 
        show_alert=True
        )
    # send direct message for user
    elif callback_query.data == 'directmessage':
        if csv_manager.is_chat_in_csv(callback_query.message.chat.id):
            await callback_query.answer(
        text="باید چت قطع کنید برای استفاده از این بخش", 
        show_alert=True
        )
    # report partner
    elif callback_query.data == 'reportuser':
        if csv_manager.is_chat_in_csv(callback_query.message.chat.id):
            await callback_query.answer(
        text="باید چت قطع کنید برای استفاده از این بخش", 
        show_alert=True
        )
            



bot.run()
