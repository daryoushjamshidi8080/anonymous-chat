
from csv_manager import CSVManager
from buttons import Button


# Object Button
button = Button()
# Object  CSV file Manager
csv_manager = CSVManager('/home/daryoush/Codes/chatAnonymous/connected_paris.csv')


# Add chat id contacts to CSV
class SaveToCSVFile:
    def __init__(self, csv_manager):
        self.csv_manager = csv_manager

    def add_chat_id_to_CSV(self, chat_id, partner_id):
        self.csv_manager.add_to_data([chat_id, partner_id])
        self.csv_manager.add_to_data([partner_id, chat_id])



# search all user
class SearchUsers:
    def __init__(self, db_manager):
        self.save_csv_file = SaveToCSVFile(csv_manager)# Chat id storage Object in CSV file
        self.db_manager = db_manager
        
    # deleted chat id of list 
    def delete_chat_id_of_list(sefl,chat_id, dict_waiting_all, dict_waiting_boy, dict_waiting_girl):
        dict_waiting_all.pop(chat_id, None)
        dict_waiting_boy.pop(chat_id, None)
        dict_waiting_girl.pop(chat_id, None)
    # looking for a girl
    async def search_girl_user(self, client, looking_girl, dict_waiting_girl, dict_waiting_boy, dict_waiting_all):
        
        looking_chat_id = looking_girl[0]
        looking_gender = looking_girl[1]
        partner_found = False
        
        # if user is girl lookking for girl
        if looking_gender == 1:
            # list waiting girl
            if dict_waiting_girl :
                for chat_id, gender in dict_waiting_girl.items():
                    if gender == 1 and int(chat_id) != looking_chat_id:
                        partner_id = int(chat_id) 
                        
                        #fetch user user_id and  partner user_id
                        user_id = self.db_manager.fetch_user_id_of_users(looking_chat_id)[0][0]
                        partner_user_id = self.db_manager.fetch_user_id_of_users(partner_id)[0][0]

                        #fetch user ids block list user
                        block_list_user = (self.db_manager.fetch_block_id(user_id))#fetch bluck id of block table
                        
                        #fetch user ids block list partner
                        block_list_partner = (self.db_manager.fetch_block_id(partner_user_id))#fetch bluck id of block table
                        


                        #check is block partner
                        if block_list_user:
                            block_ids = {block_id[0] for block_id in block_list_user} # create set of block ids
                            if partner_user_id in block_ids:
                                continue # skip to next partner if blocked
                        elif block_list_partner :
                            block_ids = {block_id[0] for block_id in block_list_partner} # create set of block ids
                            if user_id in block_ids:
                                continue # skip to next partner if blocked
                            

                        #delete all list waiting  self user
                        self.delete_chat_id_of_list(str(looking_chat_id), dict_waiting_all, dict_waiting_boy, dict_waiting_girl)
                        
                        #delete all list waiting  self user
                        self.delete_chat_id_of_list(chat_id, dict_waiting_all, dict_waiting_boy, dict_waiting_girl)

                        # Add chat IDs connected to csv file
                        self.save_csv_file.add_chat_id_to_CSV(looking_chat_id, partner_id)

                        # User connection function
                        await self.connect_users(client, looking_chat_id, partner_id)
                        
                        partner_found = True
                        break # end search

            #search dictionary all user
            if not partner_found and dict_waiting_all :

                for chat_id, gender in dict_waiting_all.items():
                    if gender == 1  and int(chat_id) != looking_chat_id:
                        partner_id = int(chat_id)


                        #fetch user user_id and  partner user_id
                        user_id = self.db_manager.fetch_user_id_of_users(looking_chat_id)[0][0]
                        partner_user_id = self.db_manager.fetch_user_id_of_users(partner_id)[0][0]

                        #fetch user ids block list user
                        block_list_user = (self.db_manager.fetch_block_id(user_id))#fetch bluck id of block table
                        
                        #fetch user ids block list partner
                        block_list_partner = (self.db_manager.fetch_block_id(partner_user_id))#fetch bluck id of block table
                        


                        #check is block partner
                        if block_list_user:
                            block_ids = {block_id[0] for block_id in block_list_user} # create set of block ids
                            if partner_user_id in block_ids:
                                continue # skip to next partner if blocked
                        elif block_list_partner :
                            block_ids = {block_id[0] for block_id in block_list_partner} # create set of block ids
                            if user_id in block_ids:
                                continue # skip to next partner if blocked

                        #delete all list waiting  self user
                        self.delete_chat_id_of_list(str(looking_chat_id), dict_waiting_all, dict_waiting_boy, dict_waiting_girl)
                        
                        #delete all list waiting  self user
                        self.delete_chat_id_of_list(chat_id, dict_waiting_all, dict_waiting_boy, dict_waiting_girl)

                        # Add chat IDs connected to csv file
                        self.save_csv_file.add_chat_id_to_CSV(looking_chat_id, partner_id)

                        # User connection function
                        await self.connect_users(client, looking_chat_id, partner_id)

                        partner_found = True
                        break # end search

            # If no partner is found, add the girl to the waiting list
            if not partner_found:
                dict_waiting_girl[str(looking_chat_id)] = looking_gender

                #send notification for waiting partner
                await self.notify_waiting(client ,looking_chat_id)
                
        # if user is boy looking a girl user
        elif looking_gender == 0:
            if dict_waiting_boy:
                for chat_id, gender in dict_waiting_boy.items():
                    if gender == 1 and int(chat_id) != looking_chat_id:
                        partner_id = int(chat_id)


                        #fetch user user_id and  partner user_id
                        user_id = self.db_manager.fetch_user_id_of_users(looking_chat_id)[0][0]
                        partner_user_id = self.db_manager.fetch_user_id_of_users(partner_id)[0][0]

                        #fetch user ids block list user
                        block_list_user = (self.db_manager.fetch_block_id(user_id))#fetch bluck id of block table
                        
                        #fetch user ids block list partner
                        block_list_partner = (self.db_manager.fetch_block_id(partner_user_id))#fetch bluck id of block table
                        


                        #check is block partner
                        if block_list_user:
                            block_ids = {block_id[0] for block_id in block_list_user} # create set of block ids
                            if partner_user_id in block_ids:
                                continue # skip to next partner if blocked
                        elif block_list_partner :
                            block_ids = {block_id[0] for block_id in block_list_partner} # create set of block ids
                            if user_id in block_ids:
                                continue # skip to next partner if blocked

                        #delete all list waiting  self user
                        self.delete_chat_id_of_list(str(looking_chat_id), dict_waiting_all, dict_waiting_boy, dict_waiting_girl)
                        
                        #delete all list waiting  self user
                        self.delete_chat_id_of_list(chat_id, dict_waiting_all, dict_waiting_boy, dict_waiting_girl)
                        
                        # Add chat IDs connected to csv file
                        self.save_csv_file.add_chat_id_to_CSV(looking_chat_id, partner_id)

                        # User connection function
                        await self.connect_users(client, looking_chat_id, partner_id)


                        partner_found = True
                        break # end search
            #search dictionary all user
            if not partner_found and dict_waiting_all :

                for chat_id, gender in dict_waiting_all.items():
                    if gender == 1 and int(chat_id) != looking_chat_id:
                        partner_id = int(chat_id)


                        #fetch user user_id and  partner user_id
                        user_id = self.db_manager.fetch_user_id_of_users(looking_chat_id)[0][0]
                        partner_user_id = self.db_manager.fetch_user_id_of_users(partner_id)[0][0]

                        #fetch user ids block list user
                        block_list_user = (self.db_manager.fetch_block_id(user_id))#fetch bluck id of block table
                        
                        #fetch user ids block list partner
                        block_list_partner = (self.db_manager.fetch_block_id(partner_user_id))#fetch bluck id of block table
                        


                        #check is block partner
                        if block_list_user:
                            block_ids = {block_id[0] for block_id in block_list_user} # create set of block ids
                            if partner_user_id in block_ids:
                                continue # skip to next partner if blocked
                        elif block_list_partner :
                            block_ids = {block_id[0] for block_id in block_list_partner} # create set of block ids
                            if user_id in block_ids:
                                continue # skip to next partner if blocked

                        #delete all list waiting  self user
                        self.delete_chat_id_of_list(str(looking_chat_id), dict_waiting_all, dict_waiting_boy, dict_waiting_girl)
                        
                        #delete all list waiting  self user
                        self.delete_chat_id_of_list(chat_id, dict_waiting_all, dict_waiting_boy, dict_waiting_girl)

                        
                        # Add chat IDs connected to csv file
                        self.save_csv_file.add_chat_id_to_CSV(looking_chat_id, partner_id)

                        # The function of connecting users to integrated
                        await self.connect_users(client, looking_chat_id, partner_id)

                        partner_found = True
                        break # end search
            # If no partner is found, add the girl to the waiting list
            if not partner_found:
                dict_waiting_girl[str(looking_chat_id)] = looking_gender
                print(dict_waiting_girl)
                #send notification for waiting partner
                await self.notify_waiting(client ,looking_chat_id)

    async def search_boy_user(self, client, looking_boy, dict_waiting_girl, dict_waiting_boy, dict_waiting_all):
        looking_chat_id = looking_boy[0]
        looking_gender = looking_boy[1]
        partner_found = False

        # if user is boy lookking for boy
        if looking_gender == 0:
            # lsit waiting  boy
            if dict_waiting_boy  :
                for chat_id, gender in dict_waiting_boy.items():
                    if gender == 0 and int(chat_id) != looking_chat_id:
                        partner_id = int(chat_id)



                        #fetch user user_id and  partner user_id
                        user_id = self.db_manager.fetch_user_id_of_users(looking_chat_id)[0][0]
                        partner_user_id = self.db_manager.fetch_user_id_of_users(partner_id)[0][0]

                        #fetch user ids block list user
                        block_list_user = (self.db_manager.fetch_block_id(user_id))#fetch bluck id of block table
                        
                        #fetch user ids block list partner
                        block_list_partner = (self.db_manager.fetch_block_id(partner_user_id))#fetch bluck id of block table
                        


                        #check is block partner
                        if block_list_user:
                            block_ids = {block_id[0] for block_id in block_list_user} # create set of block ids
                            if partner_user_id in block_ids:
                                continue # skip to next partner if blocked
                        elif block_list_partner :
                            block_ids = {block_id[0] for block_id in block_list_partner} # create set of block ids
                            if user_id in block_ids:
                                continue # skip to next partner if blocked


                        #delete all list waiting  self user
                        self.delete_chat_id_of_list(str(looking_chat_id), dict_waiting_all, dict_waiting_boy, dict_waiting_girl)
                        
                        #delete all list waiting  self user
                        self.delete_chat_id_of_list(chat_id, dict_waiting_all, dict_waiting_boy, dict_waiting_girl)

                        # User connection function
                        self.save_csv_file.add_chat_id_to_CSV(looking_chat_id, partner_id)

                        # The function of connecting users to integrated
                        await self.connect_users(client, looking_chat_id, partner_id)

                        partner_found = True
                        break #End search user

            if not partner_found and dict_waiting_all:
                for chat_id, gender in dict_waiting_all.items():
                    if gender == 0 and int(chat_id) != looking_chat_id :
                        partner_id = int(chat_id)



                        #fetch user user_id and  partner user_id
                        user_id = self.db_manager.fetch_user_id_of_users(looking_chat_id)[0][0]
                        partner_user_id = self.db_manager.fetch_user_id_of_users(partner_id)[0][0]

                        #fetch user ids block list user
                        block_list_user = (self.db_manager.fetch_block_id(user_id))#fetch bluck id of block table
                        
                        #fetch user ids block list partner
                        block_list_partner = (self.db_manager.fetch_block_id(partner_user_id))#fetch bluck id of block table
                        


                        #check is block partner
                        if block_list_user:
                            block_ids = {block_id[0] for block_id in block_list_user} # create set of block ids
                            if partner_user_id in block_ids:
                                continue # skip to next partner if blocked
                        elif block_list_partner :
                            block_ids = {block_id[0] for block_id in block_list_partner} # create set of block ids
                            if user_id in block_ids:
                                continue # skip to next partner if blocked


                        #delete all list waiting  self user
                        self.delete_chat_id_of_list(str(looking_chat_id), dict_waiting_all, dict_waiting_boy, dict_waiting_girl)
                        
                        #delete all list waiting  self user
                        self.delete_chat_id_of_list(chat_id, dict_waiting_all, dict_waiting_boy, dict_waiting_girl)

                        # User connection function
                        self.save_csv_file.add_chat_id_to_CSV(looking_chat_id, partner_id)
                        
                        # The function of connecting users to integrated
                        await self.connect_users(client, looking_chat_id, partner_id)

                        partner_found = True
                        break #End search user
            # If no partner is found, add the girl to the waiting list
            if not partner_found :
                dict_waiting_boy[str(looking_chat_id)] = looking_gender
                #send notification for waiting partner
                await self.notify_waiting(client ,looking_chat_id)
        
        # if user is girl lookking for boy
        if looking_gender == 1:
            # lsit waiting  boy
            print(dict_waiting_girl)
            if dict_waiting_girl:
                for chat_id, gender in dict_waiting_girl.items():
                    if gender == 0 and int(chat_id) != looking_chat_id:
                        partner_id = int(chat_id)
                        


                        #fetch user user_id and  partner user_id
                        user_id = self.db_manager.fetch_user_id_of_users(looking_chat_id)[0][0]
                        partner_user_id = self.db_manager.fetch_user_id_of_users(partner_id)[0][0]

                        #fetch user ids block list user
                        block_list_user = (self.db_manager.fetch_block_id(user_id))#fetch bluck id of block table
                        
                        #fetch user ids block list partner
                        block_list_partner = (self.db_manager.fetch_block_id(partner_user_id))#fetch bluck id of block table
                        


                        #check is block partner
                        if block_list_user:
                            block_ids = {block_id[0] for block_id in block_list_user} # create set of block ids
                            if partner_user_id in block_ids:
                                continue # skip to next partner if blocked
                        elif block_list_partner :
                            block_ids = {block_id[0] for block_id in block_list_partner} # create set of block ids
                            if user_id in block_ids:
                                continue # skip to next partner if blocked

                        
                        #delete all list waiting  self user
                        self.delete_chat_id_of_list(str(looking_chat_id), dict_waiting_all, dict_waiting_boy, dict_waiting_girl)
                        
                        #delete all list waiting  self user
                        self.delete_chat_id_of_list(chat_id, dict_waiting_all, dict_waiting_boy, dict_waiting_girl)

                        # User connection function
                        self.save_csv_file.add_chat_id_to_CSV(looking_chat_id, partner_id)

                        # The function of connecting users to integrated
                        await self.connect_users(client, looking_chat_id, partner_id)

                        partner_found = True
                        break  #End search user

            if not partner_found and dict_waiting_all:
                for chat_id, gender in dict_waiting_all.items():
                    if gender == 0 and int(chat_id) != looking_chat_id:
                        partner_id = int(chat_id)


                        #fetch user user_id and  partner user_id
                        user_id = self.db_manager.fetch_user_id_of_users(looking_chat_id)[0][0]
                        partner_user_id = self.db_manager.fetch_user_id_of_users(partner_id)[0][0]

                        #fetch user ids block list user
                        block_list_user = (self.db_manager.fetch_block_id(user_id))#fetch bluck id of block table
                        
                        #fetch user ids block list partner
                        block_list_partner = (self.db_manager.fetch_block_id(partner_user_id))#fetch bluck id of block table
                        


                        #check is block partner
                        if block_list_user:
                            block_ids = {block_id[0] for block_id in block_list_user} # create set of block ids
                            if partner_user_id in block_ids:
                                continue # skip to next partner if blocked
                        elif block_list_partner :
                            block_ids = {block_id[0] for block_id in block_list_partner} # create set of block ids
                            if user_id in block_ids:
                                continue # skip to next partner if blocked

                        #delete all list waiting  self user
                        self.delete_chat_id_of_list(str(looking_chat_id), dict_waiting_all, dict_waiting_boy, dict_waiting_girl)
                        
                        #delete all list waiting  self user
                        self.delete_chat_id_of_list(chat_id, dict_waiting_all, dict_waiting_boy, dict_waiting_girl)
                        

                        # User connection function
                        self.save_csv_file.add_chat_id_to_CSV(looking_chat_id, partner_id)

                        # The function of connecting users to integrated
                        await self.connect_users(client, looking_chat_id, partner_id)

                        partner_found = True
                        break #End search user
            # If no partner is found, add the girl to the waiting list
            if not partner_found :
                dict_waiting_boy[str(looking_chat_id)] = looking_gender
                #send notification for waiting partner
                await self.notify_waiting(client, looking_chat_id)
                        


    async def search_users(self, client, looking_user, dict_waiting_user_all, dict_waiting_boy, dict_waiting_girl):

        chat_id_user = looking_user[0]
        gender_user = looking_user[1]
        partner_found = False

        # If a user was expected in the list
        if dict_waiting_user_all:
            for first_item in list(dict_waiting_user_all.items()):
            
                partner_id = int(first_item[0])

                
                if chat_id_user == partner_id :
                    continue


                #fetch user user_id and  partner user_id
                user_id = self.db_manager.fetch_user_id_of_users(chat_id_user)[0][0]
                partner_user_id = self.db_manager.fetch_user_id_of_users(partner_id)[0][0]

                #fetch user ids block list user
                block_list_user = (self.db_manager.fetch_block_id(user_id))#fetch bluck id of block table
                
                #fetch user ids block list partner
                block_list_partner = (self.db_manager.fetch_block_id(partner_user_id))#fetch bluck id of block table
                


                #check is block partner
                if block_list_user:
                    block_ids = {block_id[0] for block_id in block_list_user} # create set of block ids
                    if partner_user_id in block_ids:
                        continue # skip to next partner if blocked
                elif block_list_partner :
                    block_ids = {block_id[0] for block_id in block_list_partner} # create set of block ids
                    if user_id in block_ids:
                        continue # skip to next partner if blocked


                #delete all list waiting  self user
                self.delete_chat_id_of_list(str(chat_id_user), dict_waiting_user_all, dict_waiting_boy, dict_waiting_girl)
                
                #delete all list waiting  self user
                self.delete_chat_id_of_list(str(partner_id), dict_waiting_user_all, dict_waiting_boy, dict_waiting_girl)
                
                # User connection function
                self.save_csv_file.add_chat_id_to_CSV(chat_id_user, partner_id)

                # The function of connecting users to integrated
                await self.connect_users(client, chat_id_user, partner_id)
                
                partner_found = True
                break #End code 

        if not partner_found:
            # If no partner is found, add the user to the waiting list 
            dict_waiting_user_all[str(chat_id_user)] = gender_user
            #send notification for waiting partner
            await self.notify_waiting(client ,chat_id_user)


    # The function of connecting users to integrated
    async def connect_users(self, client, user1, user2):
        
        # Connecting message to the user
        await client.send_message(user1, f"شما با کاربر {user2} متصل شدید.", reply_markup=button.menu_show_pro_end_caht_active())
        await client.send_message(user2, f"شما با کاربر {user1} متصل شدید.", reply_markup=button.menu_show_pro_end_caht_active())


     # Notifying the user that she is in the waiting queue
    async def notify_waiting(self, client, user):
        await client.send_message(user, "شما در صف انتظار قرار گرفتید. لطفا منتظر بمانید.")

        