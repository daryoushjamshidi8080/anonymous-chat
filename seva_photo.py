import os

class Photo:
    #Photo storage decorator
    async def save_photo(self,message, clinet, db_manager):
        # ID of the photo file sent by the user
        file_id = message.photo.file_id

        # Download file  send by the user 
        downloadedـfile = await clinet.download_media(file_id)

        if file_id :
            # File storage path to server
            saved_photo_path = f"/home/daryoush/Codes/chatAnonymous/Pictures/{os.path.basename(str(message.chat.id)+ '.jpg')}"

            #If not, open the folder
            os.makedirs(os.path.dirname(saved_photo_path), exist_ok=True)

            # Move the file to the final path
            os.rename(downloadedـfile, saved_photo_path)

            #Save success message
            await message.reply_text(f"عکس با موفقیت ذخیره شد: {message.chat.first_name}")
            db_manager.set_path_photo(saved_photo_path, message.chat.id)

        else:
            await message.reply_text('ذخیره نشد دوباره امتحان کن')
        