




class Blockusers:
    def __init__(self, db_manager) :
        self.db_manager = db_manager
    #set block and on block
    async def block_user(self, message, user_id=None, partner_user_id = None,partnaer_chat_id=None, user_chat_id=None):


        #fetch user id users for set block to block table
        if partnaer_chat_id:    
            partner_id = (self.db_manager.fetch_user_id_of_users(partnaer_chat_id))[0][0]
        else:
            partner_id = partner_user_id

        if user_chat_id:
            user_id = (self.db_manager.fetch_user_id_of_users(user_chat_id))[0][0]
        else:
            user_id = user_id 


        fetch_lsit_block = self.db_manager.fetch_block_id(user_id)
        block_ids = {block_id[0] for block_id in fetch_lsit_block}
        #on block
        if partner_id in block_ids:
            self.db_manager.on_block_user(user_id, partner_id)
            await message.reply_text('کاربر مورد نظر از بلاک در اومد')
        else: 
            # set ids to table (block)
            self.db_manager.set_id_to_block_list(partner_id , user_id)
            #send message block users
            await message.reply_text('کاربر مورد نظر بلاک شد')

