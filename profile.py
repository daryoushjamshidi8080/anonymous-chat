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
                button_menu = button.munu_show_profile()
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

            if not(status == 2 ):
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



























    #     #fetch all profile user requeset
    #     user_data_profile = db_manager.fetch_all_profile(chat_id=chat_id)

    #         #search gender
    #         gender = user_data_profile[0][5]

    #         #connect to boy user
    #         if waiting_boy and gender == 0:
    #             user_name = user_data_profile[0][0]

    #             partner_id = waiting_boy[0]

    #             #fatch all profile partner 
    #             partner_data_profile = db_manager.fetch_all_profile(chat_id=partner_id[0])

    #             # partner name 
    #             partner_name  = partner_data_profile[0][0]
                
    #             #check block lsit
    #             user_id = int((db_manager.fetch_user_id_of_users(callback_query.message.chat.id))[0][0])
    #             partner_user_id = int((db_manager.fetch_user_id_of_users(partner_id[0]))[0][0])

    #             try:
    #                 fetch_block_id = (db_manager.fetch_block_id(user_id))[0][0]#fetch bluck id of block table
    #             except:
    #                 fetch_block_id = None
        
    #             #add user to chat with the partnerChatGPT
    #             if not(fetch_block_id == partner_user_id) :

    #                 waiting_boy.pop(0)
                    
    #                 csv_manager.add_to_data([chat_id, partner_id[0]])
    #                 csv_manager.add_to_data([partner_id[0], chat_id])

    #                 #add user status to database (chating)
    #                 db_manager.add_status_user(2, chat_id)
    #                 db_manager.add_status_user(2, partner_id[0])



    #                 await client.send_message(chat_id, f"شما با کاربر  {partner_name}: متصل شدید.", reply_markup=Button.menu_show_pro_end_caht_active())
                    
    #             else:
    #                 # gender request user
    #                 gender = user_data_profile[0][5]
    #                 # add user to list waiting chat 
    #                 waiting_users.append((chat_id,gender))
    #                 await callback_query.message.reply_text("شما در صف انتظار قرار گرفتید. منتظر بمانید تا کاربر دیگری درخواست اتصال دهد .")


    #         #connect to girl user
    #         elif waiting_girl and gender == 1:
    #             user_name = user_data_profile[0][0]

    #             partner_id = waiting_girl[0]

    #             #fatch all profile partner 
    #             partner_data_profile = db_manager.fetch_all_profile(chat_id=partner_id[0])

    #             # partner name 
    #             partner_name  = partner_data_profile[0][0]
                
    #             #check block lsit
    #             user_id = int((db_manager.fetch_user_id_of_users(callback_query.message.chat.id))[0][0])
    #             partner_user_id = int((db_manager.fetch_user_id_of_users(partner_id[0]))[0][0])
                    
    #             try:
    #                 fetch_block_id = (db_manager.fetch_block_id(user_id))[0][0]#fetch bluck id of block table
    #             except:
    #                 fetch_block_id = None
        
    #             #add user to chat with the partner
    #             if not(fetch_block_id == partner_user_id) :

    #                 waiting_girl.pop(0)
                    
    #                 csv_manager.add_to_data([chat_id, partner_id[0]])
    #                 csv_manager.add_to_data([partner_id[0], chat_id])

    #                 #add user status to database (chating)
    #                 db_manager.add_status_user(2, chat_id)
    #                 db_manager.add_status_user(2, partner_id[0])



    #                 await client.send_message(chat_id, f"شما با کاربر  {partner_name}: متصل شدید.", reply_markup=Button.menu_show_pro_end_caht_active())
    #                 await client.send_message(partner_id[0], f"شما با کاربر {user_name} متصل شدید.", reply_markup=Button.menu_show_pro_end_caht_active())
    #             else:
    #                 # gender request user
    #                 gender = user_data_profile[0][5]
    #                 # add user to list waiting chat 
    #                 waiting_users.append((chat_id,gender))
    #                 await callback_query.message.reply_text("شما در صف انتظار قرار گرفتید. منتظر بمانید تا کاربر دیگری درخواست اتصال دهد .")


    #         # If there is a user in the waiting list, log in
    #         elif waiting_users:
    #             #user request name
    #             user_name = user_data_profile[0][0]

    #             partner_id = waiting_users[0]

    #             #fatch all profile partner 
    #             partner_data_profile = db_manager.fetch_all_profile(chat_id=partner_id[0])

    #             # partner name 
    #             partner_name  = partner_data_profile[0][0]
                
    #             #check block lsit
    #             user_id = int((db_manager.fetch_user_id_of_users(callback_query.message.chat.id))[0][0])
    #             partner_user_id = int((db_manager.fetch_user_id_of_users(partner_id[0]))[0][0])
                    
    #             print(user_id)
    #             try:
    #                 fetch_block_id = (db_manager.fetch_block_id(user_id))[0][0]#fetch bluck id of block table
    #             except:
    #                 fetch_block_id = None
            
    #             #add user to chat with the partner
    #             if not(fetch_block_id == partner_user_id) :

    #                 waiting_users.pop(0)
                    
    #                 csv_manager.add_to_data([chat_id, partner_id[0]])
    #                 csv_manager.add_to_data([partner_id[0], chat_id])

    #                 #add user status to database (chating)
    #                 db_manager.add_status_user(2, chat_id)
    #                 db_manager.add_status_user(2, partner_id[0])



    #                 await client.send_message(chat_id, f"شما با کاربر  {partner_name}: متصل شدید.", reply_markup=Button.menu_show_pro_end_caht_active())
    #                 await client.send_message(partner_id[0], f"شما با کاربر {user_name} متصل شدید.", reply_markup=Button.menu_show_pro_end_caht_active())
    #             else:
    #                 # gender request user
    #                 gender = user_data_profile[0][5]
    #                 # add user to list waiting chat 
    #                 waiting_users.append((chat_id,gender))
    #                 await callback_query.message.reply_text("شما در صف انتظار قرار گرفتید. منتظر بمانید تا کاربر دیگری درخواست اتصال دهد .")

                    

    #         else:
    #             # gender request user
    #             gender = user_data_profile[0][5]
    #             # add user to list waiting chat 
    #             waiting_users.append((chat_id,gender))
    #             await callback_query.message.reply_text("شما در صف انتظار قرار گرفتید. منتظر بمانید تا کاربر دیگری درخواست اتصال دهد .")


            

    # elif callback_query.data == 'girlsearch':

    #     user_data_profile = db_manager.fetch_all_profile(chat_id=chat_id)
    #     print(waiting_girl)
        
    
    #     if any(callback_query.message.chat.id == chat_id for chat_id, __ in waiting_girl ) :
    #         await callback_query.message.reply_text('چند بار میزنی دارم جستوجو میکنم')
    #     elif csv_manager.is_chat_in_csv(callback_query.message.chat.id):
    #         await callback_query.message.reply_text('شما درحال چت هستین')
    #     else:
    #         #fetch gender user
    #         gender = user_data_profile[0][5]
            
    #         #connect girl to list waiting girl
    #         if (waiting_girl or waiting_users ) and gender == 1:
    #             partner_id = None
    #             count_puplice_user = -1
    #             count_waiting_girl = -1
    #             #serch in list waiting girl with gender girl
    #             for chat_id, gender in waiting_girl :
    #                 count_waiting_girl += 1
    #                 if gender == 1 :
    #                     partner_id = chat_id
    #                     break
    #             if partner_id == None  and waiting_users:
    #                 for chat_id, gender in waiting_users:
    #                     count_puplice_user += 1
    #                     if  gender == 1 :
    #                         partner_id = chat_id
    #                         break
    #             if partner_id == None:
    #                 gender = user_data_profile[0][5]
    #                 # add user to list waiting chat 
    #                 waiting_girl.append((chat_id,gender))
    #                 await callback_query.message.reply_text("شما در صف انتظار قرار گرفتید. منتظر بمانید تا کاربر دیگری درخواست اتصال دهد .")

    #             elif not(partner_id == None):
    #                 user_name = user_data_profile[0][0]
                

    #                 #fatch all profile partner 
    #                 partner_data_profile = db_manager.fetch_all_profile(chat_id=partner_id)

    #                 # partner name 
    #                 partner_name  = partner_data_profile[0][0]
                    
    #                 #check block lsit
    #                 user_id = int((db_manager.fetch_user_id_of_users(callback_query.message.chat.id))[0][0])
    #                 partner_user_id = int((db_manager.fetch_user_id_of_users(partner_id))[0][0])
                        
    #                 try:
    #                     fetch_block_id = (db_manager.fetch_block_id(user_id))[0][0]#fetch bluck id of block table
    #                 except:
    #                     fetch_block_id = None
            
    #                 #add user to chat with the partner
    #                 if not(fetch_block_id == partner_user_id) :

    #                     if not(count_puplice_user== -1):
    #                         waiting_users.pop(count_puplice_user)
    #                     else:
    #                         waiting_girl.pop(count_waiting_girl)


                        
    #                     csv_manager.add_to_data([callback_query.message.chat.id, partner_id])
    #                     csv_manager.add_to_data([partner_id, callback_query.message.chat.id])

    #                     #add user status to database (chating)
    #                     db_manager.add_status_user(2, callback_query.message.chat.id)
    #                     db_manager.add_status_user(2, partner_id)



    #                     await client.send_message(callback_query.message.chat.id, f"شما با کاربر  {partner_name}: متصل شدید.", reply_markup=Button.menu_show_pro_end_caht_active())
    #                     await client.send_message(partner_id, f"شما با کاربر {user_name} متصل شدید.", reply_markup=Button.menu_show_pro_end_caht_active())

    #                 else:
    #                     #gender request user
    #                     gender = user_data_profile[0][5]
    #                     # add user to list waiting chat 
    #                     waiting_girl.append((chat_id,gender))
    #                     await callback_query.message.reply_text("شما در صف انتظار قرار گرفتید. منتظر بمانید تا کاربر دیگری درخواست اتصال دهد .")

                        
    #         elif (waiting_users or waiting_girl) and gender == 0:
    #             partner_id = None
    #             count_puplice_user = -1
    #             count_waiting_girl = -1
    #             #serch in list waiting girl with gender girl
    #             for chat_id, gender in waiting_girl :
    #                 count_waiting_girl += 1
    #                 if gender == 1 :
    #                     partner_id = chat_id
    #                     break
    #             print(count_puplice_user)
    #             if partner_id == None:
    #                 for chat_id, gender in waiting_users:
    #                     count_puplice_user +=1 
    #                     if  gender == 1 :
    #                         partner_id = chat_id
    #                         break
    #             if partner_id == None:
    #                 gender = user_data_profile[0][5]
    #                 # add user to list waiting chat 
    #                 waiting_girl.append((chat_id,gender))
    #                 await callback_query.message.reply_text("شما در صف انتظار قرار گرفتید. منتظر بمانید تا کاربر دیگری درخواست اتصال دهد .")


    #             elif not(partner_id == None):
    #                 user_name = user_data_profile[0][0]

    #                 #fatch all profile partner 
    #                 partner_data_profile = db_manager.fetch_all_profile(chat_id=partner_id)

    #                 # partner name 
    #                 partner_name  = partner_data_profile[0][0]
                    
    #                 #check block lsit
    #                 user_id = int((db_manager.fetch_user_id_of_users(callback_query.message.chat.id))[0][0])
    #                 partner_user_id = int((db_manager.fetch_user_id_of_users(partner_id))[0][0])
                        
    #                 try:
    #                     fetch_block_id = (db_manager.fetch_block_id(user_id))[0][0]#fetch bluck id of block table
    #                 except:
    #                     fetch_block_id = None
                
    #                 #add user to chat with the partner
    #                 if not(fetch_block_id == partner_user_id) :
                        
    #                     if not(count_puplice_user== -1):
    #                         waiting_users.pop(count_puplice_user)
    #                     else:
    #                         waiting_girl.pop(count_waiting_girl)

                            
                        
    #                     csv_manager.add_to_data([callback_query.message.chat.id, partner_id])
    #                     csv_manager.add_to_data([partner_id, callback_query.message.chat.id])

    #                     #add user status to database (chating)
    #                     db_manager.add_status_user(2, callback_query.message.chat.id)
    #                     db_manager.add_status_user(2, partner_id)



    #                     await client.send_message(callback_query.message.chat.id, f"شما با کاربر  {partner_name}: متصل شدید.", reply_markup=Button.menu_show_pro_end_caht_active())
    #                     await client.send_message(partner_id, f"شما با کاربر {user_name} متصل شدید.", reply_markup=Button.menu_show_pro_end_caht_active())
    #                 else:
    #                     # gender request user
    #                     gender = user_data_profile[0][5]
    #                     # add user to list waiting chat 
    #                     waiting_girl.append((chat_id,gender))
    #                     await callback_query.message.reply_text("شما در صف انتظار قرار گرفتید. منتظر بمانید تا کاربر دیگری درخواست اتصال دهد .")

    #         elif gender == 0 and  
    #         else:
    #             # gender request user
    #             gender = user_data_profile[0][5]
    #             # add user to list waiting chat 
    #             waiting_girl.append((chat_id,gender))
    #             await callback_query.message.reply_text("شما در صف انتظار قرار گرفتید. منتظر بمانید تا کاربر دیگری درخواست اتصال دهد .")




    # elif callback_query.data == 'boysearch':

    #     user_data_profile = db_manager.fetch_all_profile(chat_id=callback_query.message.chat.id)
    #     print(waiting_boy)
        
    
    #     if any(callback_query.message.chat.id == chat_id for chat_id, __ in waiting_boy ) :
    #         await callback_query.message.reply_text('چند بار میزنی دارم جستوجو میکنم')
    #     elif csv_manager.is_chat_in_csv(callback_query.message.chat.id):
    #         await callback_query.message.reply_text('شما درحال چت هستین')
    #     else:
    #         #fetch gender user
    #         gender = user_data_profile[0][5]
            
    #         #connect boy to list waiting boy
    #         if (waiting_boy or waiting_users ) and gender == 1:
    #             partner_id = None
    #             count_puplice_user = -1
    #             count_waiting_boy = -1
    #             #serch in list waiting girl with gender girl
    #             for chat_id, gender in waiting_girl :
    #                 count_waiting_boy += 1
    #                 if gender == 1 :
    #                     partner_id = chat_id
    #                     break
    #             if partner_id == None  and waiting_users:
    #                 for chat_id, gender in waiting_users:
    #                     count_puplice_user += 1
    #                     if  gender == 1 :
    #                         partner_id = chat_id
    #                         break
    #             if partner_id == None:
    #                 gender = user_data_profile[0][5]
    #                 # add user to list waiting chat 
    #                 waiting_boy.append((chat_id,gender))
    #                 await callback_query.message.reply_text("شما در صف انتظار قرار گرفتید. منتظر بمانید تا کاربر دیگری درخواست اتصال دهد .")

    #             elif not(partner_id == None):
    #                 user_name = user_data_profile[0][0]
                

    #                 #fatch all profile partner 
    #                 partner_data_profile = db_manager.fetch_all_profile(chat_id=partner_id)

    #                 # partner name 
    #                 partner_name  = partner_data_profile[0][0]
                    
    #                 #check block lsit
    #                 user_id = int((db_manager.fetch_user_id_of_users(callback_query.message.chat.id))[0][0])
    #                 partner_user_id = int((db_manager.fetch_user_id_of_users(partner_id))[0][0])
                        
    #                 try:
    #                     fetch_block_id = (db_manager.fetch_block_id(user_id))[0][0]#fetch bluck id of block table
    #                 except:
    #                     fetch_block_id = None
            
    #                 #add user to chat with the partner
    #                 if not(fetch_block_id == partner_user_id) :

    #                     if not(count_puplice_user== -1):
    #                         waiting_users.pop(count_puplice_user)
    #                     else:
    #                         waiting_boy.pop(count_waiting_boy)


                        
    #                     csv_manager.add_to_data([callback_query.message.chat.id, partner_id])
    #                     csv_manager.add_to_data([partner_id, callback_query.message.chat.id])

    #                     #add user status to database (chating)
    #                     db_manager.add_status_user(2, callback_query.message.chat.id)
    #                     db_manager.add_status_user(2, partner_id)



    #                     await client.send_message(callback_query.message.chat.id, f"شما با کاربر  {partner_name}: متصل شدید.", reply_markup=Button.menu_show_pro_end_caht_active())
    #                     await client.send_message(partner_id, f"شما با کاربر {user_name} متصل شدید.", reply_markup=Button.menu_show_pro_end_caht_active())

    #                 else:
    #                     # gender request user
    #                     gender = user_data_profile[0][5]
    #                     # add user to list waiting chat 
    #                     waiting_boy.append((chat_id,gender))
    #                     await callback_query.message.reply_text("شما در صف انتظار قرار گرفتید. منتظر بمانید تا کاربر دیگری درخواست اتصال دهد .")

                        
                        
    #         elif (waiting_users or waiting_boy) and gender == 0:
    #             partner_id = None
    #             count_puplice_user = -1
    #             count_waiting_boy = -1
    #             #serch in list waiting boy with gender boy
    #             for chat_id, gender in waiting_boy :
    #                 count_waiting_boy += 1
    #                 if gender == 1 :
    #                     partner_id = chat_id
    #                     break
    #             print(count_puplice_user)
    #             if partner_id == None:
    #                 for chat_id, gender in waiting_users:
    #                     count_puplice_user +=1 
    #                     if  gender == 1 :
    #                         partner_id = chat_id
    #                         break
    #             if partner_id == None:
    #                 gender = user_data_profile[0][5]
    #                 # add user to list waiting chat 
    #                 waiting_boy.append((chat_id,gender))
    #                 await callback_query.message.reply_text("شما در صف انتظار قرار گرفتید. منتظر بمانید تا کاربر دیگری درخواست اتصال دهد .")


    #             elif not(partner_id == None):
    #                 user_name = user_data_profile[0][0]

    #                 #fatch all profile partner 
    #                 partner_data_profile = db_manager.fetch_all_profile(chat_id=partner_id)

    #                 # partner name 
    #                 partner_name  = partner_data_profile[0][0]
                    
    #                 #check block lsit
    #                 user_id = int((db_manager.fetch_user_id_of_users(callback_query.message.chat.id))[0][0])
    #                 partner_user_id = int((db_manager.fetch_user_id_of_users(partner_id))[0][0])
                        
    #                 try:
    #                     fetch_block_id = (db_manager.fetch_block_id(user_id))[0][0]#fetch bluck id of block table
    #                 except:
    #                     fetch_block_id = None
                
    #                 #add user to chat with the partner
    #                 if not(fetch_block_id == partner_user_id) :
                        
    #                     if not(count_puplice_user== -1):
    #                         waiting_users.pop(count_puplice_user)
    #                     else:
    #                         waiting_boy.pop(count_waiting_boy)

                            
                        
    #                     csv_manager.add_to_data([callback_query.message.chat.id, partner_id])
    #                     csv_manager.add_to_data([partner_id, callback_query.message.chat.id])

    #                     #add user status to database (chating)
    #                     db_manager.add_status_user(2, callback_query.message.chat.id)
    #                     db_manager.add_status_user(2, partner_id)



    #                     await client.send_message(callback_query.message.chat.id, f"شما با کاربر  {partner_name}: متصل شدید.", reply_markup=Button.menu_show_pro_end_caht_active())
    #                     await client.send_message(partner_id, f"شما با کاربر {user_name} متصل شدید.", reply_markup=Button.menu_show_pro_end_caht_active())
    #                 else:
    #                     # gender request user
    #                     gender = user_data_profile[0][5]
    #                     # add user to list waiting chat 
    #                     waiting_boy.append((chat_id,gender))
    #                     await callback_query.message.reply_text("شما در صف انتظار قرار گرفتید. منتظر بمانید تا کاربر دیگری درخواست اتصال دهد .")

    #         else:
    #             # gender request user
    #             gender = user_data_profile[0][5]
    #             # add user to list waiting chat 
    #             waiting_boy.append((chat_id,gender))
    #             await callback_query.message.reply_text("شما در صف انتظار قرار گرفتید. منتظر بمانید تا کاربر دیگری درخواست اتصال دهد .")
