import re


class MessageManager:
    def __init__(self, db_manager, button):
         self.db_manager = db_manager
         self.button = button
    #fetch show id of caption
    def fetch_show_id_of_caption(self, message_caption):
          pattern = r"/user_(\d+)"
          show_id = re.search(pattern, message_caption).group(1)

          return 'user_' + show_id
    
    #manage message for send 
    def manage_massage(self, chat_id, partnare_id):
         pass
    
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
     {message}پیام : ''', reply_markup=self.button.menu_direct_message())
          
     