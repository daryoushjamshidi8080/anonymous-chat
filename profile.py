import os
from datetimer import Time
import datetime

time = Time()

class Profile:
    async def profile_user(self, client, db_manager, message, button, user_id =None, chat_id=None):
        try:
            #fetch profill data of database in table of users
            if user_id:
                data_profile = db_manager.fetch_all_profile(user_id=user_id)
                button_menu = button.menu_send_request()
            #show profile  in te chat
            elif not(chat_id == None):
                data_profile = db_manager.fetch_all_profile(chat_id=chat_id)
                user_id = (db_manager.fetch_user_id_of_users(chat_id))[0][0]
                #update time login
                time.update_time_login(db_manager,message.chat.id)
                button_menu = button.munu_show_profile()
                
            else :
                button_menu = button.menu_profile()
                data_profile = db_manager.fetch_all_profile(chat_id=message.chat.id)
                user_id = (db_manager.fetch_user_id_of_users(message.chat.id))[0][0]
                #update time login
                time.update_time_login(db_manager,message.chat.id)

            
            

            if not data_profile:
                await message.reply_text('شما پروفایل درست نکردید /start از اول درست کنید')
                return
            name = data_profile[0][0]
            age = data_profile[0][1]
            province_id = data_profile[0][2]
            city_id = data_profile[0][3]
            biography = data_profile[0][4]
            gender = data_profile[0][5]
            status = data_profile[0][6]
            path_photo = data_profile[0][7]

            #list of province
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
            province = province_dict[str(province_id)]
            
            # fetch name city of database 
            city_name = (db_manager.fetch_name_city(city_id))[0][0]

            # fetch show id of database
            show_id = (db_manager.fetch_show_id(user_id))[0][0]

            if not(status == 3 ):
                last_logout_time = (db_manager.fetch_last_login_time(user_id))[0][0]
                time_status = time.time_difference_from_now(last_logout_time)
                time_result = None
                if time_status[:3]== 'scd':
                    status = 1
                elif time_status[:3] == 'min':
                    if int(time_status[4:]) < 5 :
                        status = 1
                    else:
                        status = 0
                    time_result = f'{time_status[4:]}دقیقه قبل انلاین بود'
                elif time_status[:3] == 'hur' :
                    status = 0
                    time_result = f'{time_status[4:]}ساعت قبل انلاین بود'
                elif time_status[:3] == 'day' :
                    status = 0
                    time_result = f'{time_status[4:]}روز قبل انلاین بود'
            
                
            gender = 'پسر' if gender == 0 else 'دختر'
            status = f'{time_result}' if status == 0 else 'آنلاین' if status == 1 else 'آنلاین(درحال چت)'
            biography = biography or '!?'
            

            if not(path_photo):
                #not photo to database #set defualte path
                photo_path = "/home/daryoush/Codes/chatAnonymous/Pictures/default_image.jpg"
            else:
                photo_path = path_photo

            
                await client.send_photo(
                message.chat.id,
                photo=photo_path,
                caption=f"""
        اسم : {name}

    سن : {age}

    استان : {province}

    شهر : {city_name}

    جنسیت : {gender}

    وضیعت : {status}

    بیوگرافی : {biography}



   ایدی:  /{show_id}
   

    """,reply_markup=button_menu)
        except Exception as e:
            await message.reply_text(f'خطا در بارگذاری پروفایل: {e}')
