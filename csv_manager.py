import csv
import os



class CSVManager:
    def __init__(self, file_path):
        self.file_path = file_path

    #Checking ID Chat in CSV file
    def is_chat_in_csv(self, chat_id):
        with open(self.file_path, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if str(chat_id) in row:
                    return True
        return False
    
    # Add data(chat id) to CSV file
    def add_to_data(self, data):
        with open(self.file_path, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data)

    # remove chat id of CSV file
    def remove_chat_id_from_csv(self, chat_id):
        temp_file_path = self.file_path + '.temp'
        with open(self.file_path, 'r', newline='') as csv_file, open(temp_file_path, 'w', newline='') as temp_file:
            reader = csv.reader(csv_file)
            writer = csv.writer(temp_file)
            found = False
            for row in reader :
                if str(chat_id) in row:
                    found =True
                    continue
                writer.writerow(row)
            #Replace the original file with a temporary file
            if found: 
                os.replace(temp_file_path, self.file_path)
            else:
                os.remove(temp_file_path)
                
    # search partner id of chat id 
    def search_partner_id(self, chat_id):
        try:
            with open(self.file_path, 'r', newline='') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    if row[0] == str(chat_id):
                        return row[1]
        except FileNotFoundError:
            print(f'File not found: {self.file_path}')

        except Exception as e :
            print(f'Error searching partner_id in CSV: {e}')
        return None # not found chat id

