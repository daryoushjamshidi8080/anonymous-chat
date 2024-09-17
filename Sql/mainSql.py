import psycopg2 # libary connect to databas


class DatabaseManager:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None #attribute connect to data base 
        self.cur = None
        self.open()

    # Open database
    def open(self):
        #connet database with library pycopg2
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
        self.cur =self.conn.cursor()#Database stability
    #close of database 
    def close(self):
        self.cur.close()
        self.conn.close()

    #fetc first name of chat id 
    def fetch_chat_id(self, chat_id):
        try:
            self.open()
            self.cur.execute("SELECT firstname FROM users WHERE cach_id = %s",(chat_id,))
            results_data = self.cur.fetchall()
            return results_data
        finally:
            self.close()
    #fetch user_id of users table
    def fetch_user_id_of_users(self, chat_id):
        try:
            self.open()
            self.cur.execute("SELECT user_id FROM users WHERE cach_id = %s",(chat_id,))
            results_data = self.cur.fetchall()
            return results_data
        except Exception as e :
            print(f'Error in fetch user_id is : {e}')
        finally:
            self.close()
    # fetch user_id of chat_id table
    def fetch_user_id_of_show_id(self, show_id):
        try:
            self.open()
            self.cur.execute("SELECT user_id FROM chat_id WHERE show_id = %s", (show_id,))
            results_data = self.cur.fetchall()
            return results_data
        except Exception as e :
            print('Error in fetch user_id of show id is : ',e)
        finally:
            self.close()
    #fetch  province id 
    def fetch_province_id(self, province):
        try:
            self.open()
            self.cur.execute("SELECT province_id FROM provinces WHERE  province = %s", (province,))
            results_data = self.cur.fetchall()
            return results_data
        except Exception as e :
            print("error in  fetch provinces and city is ==> ",e)
        finally:
            self.close()
    #fetch city id 
    def fetch_city_id(self, city):
        try:
            self.open()
            self.cur.execute("SELECT city_id FROM cities WHERE  city = %s", (city,))
            results_data = self.cur.fetchall()
            return results_data
        except Exception as e :
            print("error in  fetch city and city is ==> ",e)
        finally:
            self.close()
    #insert data During initial startup to users table 
    def insert_data_new_start(self, information):
        try:
            self.open()
            self.cur.execute("INSERT INTO users (cach_id, firstname, age, province_id, city_id, gender) VALUES (%s, %s, %s, %s, %s, %s)", tuple(information))
            self.conn.commit()#seting qeury to database
        except Exception as e :
            print(f"Error insert new user: {e}")
            self.conn.rollback()#Remove half operations
        finally:
            self.close()

    #create show id 
    def create_show_id(self, data):
        try:
            self.open()
            self.cur.execute("INSERT INTO chat_id(show_id, user_id) VALUES (%s, %s)", tuple(data))
            self.conn.commit()
        except Exception as e :
            print('error in insert show id : ', e )
            self.rollback()
        finally:
            self.close()
    #fetch show id of database of user id
    def fetch_show_id(self, user_id):
        try:
            self.open()
            self.cur.execute("SELECT show_id FROM chat_id WHERE user_id = %s", (user_id,))
            results_data = self.cur.fetchall()
            return(results_data)
        except Exception as e :
            print(f'Error in fetch show id is : {e}')
        finally:
            self.close()
    #fetch chat id of chat id in users table
    def fetch_chat_id_of_user_id(self, user_id):
        try:
            self.open()
            self.cur.execute("SELECT cach_id from users WHERE user_id = %s", (user_id,))
            resualt_data = self.cur.fetchall()
            return resualt_data
        except Exception as e :
            print("Error in fetch chat id of users table is : ", e)
        finally:
            self.close()

    #insert data If the city is not in the database
    def insert_new_city(self, new_city):
        try:
            self.open()
            self.cur.execute("INSERT INTO cities(city, province_id) VALUES (%s, %s)", tuple(new_city))
            self.conn.commit()  # Save the changes
        except Exception as e:
            print('error in insert new city to database is: ', e)
            self.conn.rollback()
        finally:
            self.close()
    #fetch all profile of database
    def fetch_all_profile(self, chat_id=None, user_id=None):
        try:
            self.open()

            if chat_id is not None:
                self.cur.execute("SELECT firstname, age, province_id, city_id, biography, gender, status, picture FROM users WHERE cach_id = %s", (chat_id,))
            elif user_id is not None:
                self.cur.execute("SELECT firstname, age, province_id, city_id, biography, gender, status, picture FROM users WHERE user_id = %s", (user_id,))
            results_data = self.cur.fetchall()
            return results_data
        except Exception as e :
            print(f'Error in fetch data all profile {e}')
        finally:
            self.close()
    # fetch city name 
    def fetch_name_city(self, city_id):
        try:
            self.open()
            self.cur.execute("SELECT city FROM cities WHERE city_id = %s", (city_id,))
            results_data = self.cur.fetchall()
            return results_data
        except Exception as e:
            print('Error in fetch name city is:', e)
        finally:
            self.close()
    #set or update path profile to columne picture in the users tabel
    def set_path_photo(self, value, chat_id):
        try:
            self.open()
            self.cur.execute('UPDATE users SET picture = %s WHERE cach_id = %s ',(value, chat_id))
            self.conn.commit()
        except Exception as e :
            print('error set or update in is : ', e)
            self.conn.rollback()
        finally:
            self.close()

    # edit name ,age ,province ,city, biogrphy, gender
    def edit_all_profile(self, chat_id, name=None, age=None, province=None, city=None, biography=None, gender=None):
        try:
            self.open()
            if name:
                self.cur.execute('UPDATE users SET firstname = %s WHERE cach_id = %s ', (name, chat_id))
            elif age:
                self.cur.execute('UPDATE users SET age = %s WHERE cach_id = %s ', (age, chat_id))
            elif not(province == None):
                self.cur.execute('UPDATE users SET province_id = %s WHERE cach_id = %s ', (province, chat_id))
            elif not(city == None):
                self.cur.execute('UPDATE users SET city_id = %s WHERE cach_id = %s ', (city, chat_id))
            elif not(biography ==  None):
                self.cur.execute('UPDATE users SET biography = %s WHERE cach_id = %s ', (biography, chat_id))
            elif not(gender == None):
                self.cur.execute('UPDATE users SET gender = %s WHERE cach_id = %s ', (gender, chat_id))
            self.conn.commit()
        except Exception as e :
            print('Error in the edit all profile is : ', e)
            self.conn.rollback()
        finally:
            self.close()
    # update and set time login in login last login
    def update_set_time_login(self, value, user_id, chat_id=None):
        try:
            self.open()
            if not(chat_id == None):
                self.cur.execute("INSERT INTO lastlogin(lastloin, user_id) VALUES (%s, %s)", (value, user_id))
            else:
                self.cur.execute("UPDATE lastlogin SET lastloin = %s WHERE user_id = %s", (value,user_id))
            self.conn.commit()
        except Exception as e :
            print('Error in update time login is :', e)
            self.conn.rollback()
        finally:
            self.close()
    #fetch last login time 
    def fetch_last_login_time(self, user_id):
        try:
            self.open()
            self.cur.execute("SELECT lastloin FROM lastlogin WHERE user_id = %s", (user_id,))
            resulte_date = self.cur.fetchall()
            return resulte_date
        except Exception as e :
            print('Error in fetch last login time is : ', e)
        finally :
            self.close()

    # set id to block in blocklist table (block)
    def set_id_to_block_list(self, block_id_user, user_id):
        try:
            self.open()
            self.cur.execute("INSERT INTO blockedlist(block_id_user, user_id) VALUES (%s, %s)", (block_id_user, user_id))
            self.conn.commit() 
        except Exception as e:
            print("Error in set block list table is:", e)
            self.conn.rollback()
        finally:
            self.close()
    # fetcu block id of blockedlist table 
    def fetch_block_id(self, user_id):
        try:
            self.open()
            self.cur.execute("SELECT block_id_user FROM blockedlist WHERE user_id = %s", (user_id,))
            resulte_data = self.cur.fetchall()
            return resulte_data
        except Exception as e :
            print('Error in Fetch block id is:', e)
        finally:
            self.close()
    # delete user id of block id (on block)
    def on_block_user(self, user_id, block_id_user):
        try:
            self.open()
            self.cur.execute("DELETE FROM blockedlist WHERE user_id = %s and block_id_user = %s", (user_id, block_id_user))
            self.conn.commit()
        except Exception as e :
            print('Error in Delete id of block in blockedlist table is : ', e)
        finally:
            self.close()

    #add status user to database 
    def add_status_user(self, value, chat_id):
        try:
            self.open()
            self.cur.execute('UPDATE users SET status = %s WHERE cach_id = %s', (value, chat_id))
            self.conn.commit()
        except Exception as e :
            print('Error add status user to database is : ', e)
            self.conn.rollback()
        finally:
            self.close()




if __name__ == '__main__':
    print('ok test fill')
