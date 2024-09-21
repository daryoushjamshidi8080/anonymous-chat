import re

from search_user import SearchUsers
from csv_manager import CSVManager
from quesfuser import Response
from datetimer import Time
import random


# Object response for question of users
response = Response()
# Object time for save time login 
time  = Time()



class MessageManager:
     def __init__(self, db_manager, button):
          self.db_manager = db_manager
          self.button = button
          self.csv_manager = CSVManager('/home/daryoush/Codes/chatAnonymous/connected_paris.csv')
          self.search_user = SearchUsers(self.db_manager)

     #fetch show id of caption
     def fetch_show_id_of_caption(self, message_caption):
          pattern = r"/user_(\d+)"
          show_id = re.search(pattern, message_caption).group(1)

          return 'user_' + show_id
     
     #fetch user id of text
     def fetch_user_id_of_text(self, message_text):
          pattern = r"#(\d+)"
          user_id = re.search(pattern, message_text).group(1)

          return user_id
    #manage message for send 
     async def manage_send_message(self, client, message, csv_manager, protect_content):
     
          #search partner id of chat id is csv file
          partner_id = int(csv_manager.search_partner_id(message.chat.id))

          #Check if the message has been replicated to another message or not
          if message.reply_to_message:
               
               # Get the user ID of the sender of the current message
               current_user_id = message.from_user.id

               # Getting the user ID of the sender of the replicated message
               replied_user_id = message.reply_to_message.from_user.id

               # Checking whether the user has replied to his own message or not
               if current_user_id == replied_user_id:
                    reply_to_message_id = message.reply_to_message.id + 1 if message.reply_to_message else None

               else:
                    reply_to_message_id = message.reply_to_message.id - 1 if message.reply_to_message else None
          else:
               reply_to_message_id = None

          if message.text:
               await client.send_message(partner_id, message.text, reply_to_message_id=reply_to_message_id)#message.reply_to_message_id)
          elif message.animation:
               await client.send_animation(partner_id, message.animation.file_id,protect_content=protect_content, reply_to_message_id=reply_to_message_id)
          elif message.photo:
               await client.send_photo(partner_id, message.photo.file_id, protect_content=protect_content , reply_to_message_id=reply_to_message_id)
          elif message.sticker:
               await client.send_sticker(partner_id, message.sticker.file_id, protect_content=protect_content, reply_to_message_id=reply_to_message_id )
          elif message.video:
               await client.send_video(partner_id, message.video.file_id, protect_content=protect_content, reply_to_message_id=reply_to_message_id )
               
    
    # send message to direct user
     async def send_message_direct(self, client, callback_query, user_id, message, chat_id_sender):
         

         #fetch chat id of  database 
         chat_id = (self.db_manager.fetch_chat_id_of_user_id(user_id))[0][0]# chat id point user 

         user_id_sender = (self.db_manager.fetch_user_id_of_users(chat_id_sender))[0][0]# user id sender user 
         show_id = (self.db_manager.fetch_show_id(user_id_sender))[0][0]#show id sender
          

         block_list_user = (self.db_manager.fetch_block_id(user_id))#fetch bluck id of block table
         if user_id_sender in {block_id[0] for block_id  in block_list_user}:
             await callback_query.message.reply_text('شما بلاک هستین پیام شما به ایشان ارسال نمیشود')
         else:
          #send message to user
          await callback_query.message.reply_text('پیام شما با موفقیت ارسال شد')# send message to sender user
          await client.send_message(chat_id, f'''
          کاربری با ایدی /{show_id} با شما نوشته :
          `درصورت مشکل بلاک کنید در این صورت پیام های ایشان به شما ارسال نمیشود‍‍‍`
          {message}پیام : ''', 
          reply_markup=self.button.menu_direct_message())

     # send request chat for user 
     async def sned_request_caht(self, client, callback_query, point_user_id, point_chat_id, user_request_show_id, request_user_id):
          
          #status (online or offline) at user 
          status_point_user = self.db_manager.fetch_all_profile(chat_id=point_chat_id)[0][6]
          status_request_user = self.db_manager.fetch_all_profile(chat_id=callback_query.message.chat.id)[0][6]

          #fetch bluck id of block table
          block_list = (self.db_manager.fetch_block_id(point_user_id))

          print(request_user_id)
          if request_user_id in {block_id[0] for block_id in block_list}:
               await callback_query.message.reply_text('شما بلاک هستین پیام شما به ایشان ارسال نمیشود')
          elif status_point_user == 2:
               await callback_query.message.reply_text('کاربر درحال چت هست باید چت ایشان تمام شود')
          elif status_request_user == 2 :
               await callback_query.message.reply_text('شما درحال چت هستین باید چت را قطع کنید')
          else:
               # send reques for point user 
               await client.send_message(point_chat_id, f"""
               `کاربر` {'/'+user_request_show_id} `درخواست چت` با شما رو دارد
               `درصورت نیاز میتوانید بلاک کنید`
     """, reply_markup = self.button.menu_request_chat())
               
               await callback_query.message.reply_text('درخواست شما با موفقیت ارسال شد')# send message to sender user
          
     #accept request chat at point user
     async def accept_request_chat(self, client, request_chat_id, point_user_chatid):

          # Add chat IDs connected to csv file
          self.csv_manager.add_to_data([request_chat_id, point_user_chatid])
          self.csv_manager.add_to_data([point_user_chatid, request_chat_id])
          
          # User connection function
          await self.search_user.connect_users(client, request_chat_id, point_user_chatid)
          
     async def reject_request(self, client,  callback_query, sender_chat_id, point_caht_id):
          
          await client.send_message(sender_chat_id, f'درخواست شمارو {point_caht_id}رد کرد')
          print(callback_query)
          await client.delete_messages(chat_id=point_caht_id, message_ids=callback_query.message.id)
     
     # ask question of user
     async def ask_question(self, bot, message, value, basic_information, button=None):  
          if button :
               await message.reply_text(value, reply_markup=button)  
          else:
               await message.reply_text(value)   
          answer= await response.respons_text(bot, message.chat.id)
          value_resulte = answer.text
          basic_information.append(value_resulte)
          
     #get data profile of users
     async def get_new_data_for_pro(self, bot,message):
          # Basic information user during initial check-in
          basic_information = [message.chat.id] 
          await self.ask_question(bot, message, 'اسم', basic_information)#name question and save the name in the database
          await self.ask_question(bot, message, 'سن', basic_information, self.button.menu_number())#age question

          #province question
          await message.reply_text('استان ؟', reply_markup=self.button.menu_provinces() )
          answer = await response.respons_text(bot, message.chat.id)
          province = answer.text
          province_id = self.db_manager.fetch_province_id(province)
          basic_information.append(province_id[0][0])

          #city question
          try: 
               await message.reply_text('شهر ؟', reply_markup=self.button.menu_city(province))
               answer = await response.respons_text(bot, message.chat.id)
               city = answer.text
               city_id = self.db_manager.fetch_city_id(city)
               basic_information.append(city_id[0][0])
          except :
               new_city = []
               new_city.append(city)
               new_city.append(province_id[0][0])
               self.db_manager.insert_new_city(new_city)
               city_id = self.db_manager.fetch_city_id(city)
               basic_information.append(city_id[0][0])

          #gender question
          await message.reply_text('جنسیت ؟', reply_markup=self.button.menu_gender())
          answer = await response.respons_text(bot, message.chat.id)
          gender = answer.text
          if gender == 'دختر' :
               gender = 1
          else:
               gender = 0
          basic_information.append(gender)


          #set Basic information during initial check-in
          self.db_manager.insert_data_new_start(basic_information)
          #set login time 
          time.set_first_time_log(self.db_manager, message.chat.id)
          
          

          #create show id for new user
          try:
               user_id =self.db_manager.fetch_user_id_of_users(message.chat.id)
               show_id = 'user_' + str(message.chat.id)[:-4]
               data = [show_id, user_id[0][0]]
               self.db_manager.create_show_id(data)
          except Exception as e:
               #Duplicate show ID, a new sowh ID was created
               random_char = ['@', '%', '*', '+', '$', '!']
               x =show_id + str(random.choice(random_char))+'H'
               print('Duplicate ID, a new ID was created error is : ', x)
               
          


     async def send_anonymous_message(self, client, sender_chat_id, point_show_id):
          #fetch user id sender user
          sender_user_id = self.db_manager.fetch_user_id_of_users(sender_chat_id)[0][0]

          #fetch chat id point user
          point_user_id = self.db_manager.fetch_user_id_of_show_id(point_show_id)[0][0]
          point_chat_id = self.db_manager.fetch_chat_id_of_user_id(point_user_id)[0][0]

          #send message question to sender user
          await client.send_message(sender_chat_id, 'پیام خود را بنویسید')
          # question message of sender user 
          value =await response.respons_text(client, sender_chat_id)
          await client.send_message(sender_chat_id, '''
                                     پیام شما با موفقیت ارسال شد             
                `برای ارسال پیام دیگر روی لینک دوباره کلیک کنید`
''')


          await client.send_message(point_chat_id,f'''
`پیام ناشناس دریافتی شما:`
                                    
{value.text}

#{sender_user_id}
''', reply_markup=self.button.menu_respons_to_anonymus())


