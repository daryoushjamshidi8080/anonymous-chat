import re

from search_user import SearchUsers
from csv_manager import CSVManager


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

          