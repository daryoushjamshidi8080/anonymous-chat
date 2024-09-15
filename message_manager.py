import re


class MessageManager:
    #fetch show id of caption
    def fetch_show_id_of_caption(self, message_caption):
          pattern = r"/user_(\d+)"
          show_id = re.search(pattern, message_caption).group(1)

          return 'user_' + show_id