import datetime 

class Time:
    def __init__(self) :
        self.time_now = datetime.datetime.now()
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
        
        #Request to send user to user
        time_difference = self.time_now - last_logout_time

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
        