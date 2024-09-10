from pyromod import listen


#Waiting for the robot to answer the user
class Response:
    async def respons_text(self, bot, chat_id):
        return await bot.listen(chat_id)