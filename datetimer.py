import datetime

class Time:
    
    #set first start time login user
    def set_first_time_log(self ,db_manager, chat_id):
        current_time = datetime.datetime.now()
        user_id = (db_manager.fetch_user_id_of_users(chat_id))[0][0]
        db_manager.update_set_time_login(current_time, user_id, chat_id= chat_id)
    #update time login user
    def update_time_login(self, db_manager, chat_id):
        current_time = datetime.datetime.now()
        user_id = (db_manager.fetch_user_id_of_users(chat_id))[0][0]
        db_manager.update_set_time_login(current_time, user_id)
        
    def time_difference_from_now(self, last_logout_time):
        print('in data base last time : ',last_logout_time)
        print('now time : ',datetime.datetime.now())
        #Request to send user to user
        time_difference = abs(datetime.datetime.now() - last_logout_time)
        # time_difference = abs(last_logout_time - datetime.datetime.now() )
        # print(time_difference)

        days = time_difference.days
        seconds = time_difference.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        
        if days > 0:
            return f"day:{days}"
        elif hours > 0:
            return f"hur:{hours}"
        elif minutes > 0:
            return f'min:{minutes}'
        elif seconds > 0:
            return f'scd:{seconds}'
        else:
            return f"scd:0"
        