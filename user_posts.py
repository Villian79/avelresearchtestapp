#! python3

from facepy import GraphAPI
import os, re
from pprint import pprint
from configparser import ConfigParser

#Get config data
if __name__ == '__main__':
  cfg = ConfigParser()
  cfg.read('config.ini')
  ACCESS_TOKEN = cfg.get('App','access_token')
  FILE_PATH = cfg.get('App', 'file_path')
  USER_ID = cfg.get('User', 'id')

# Initialize the Graph API with a valid access token (optional, but will allow you to do all sorts of fun stuff).
graph = GraphAPI(ACCESS_TOKEN)
# Get the User profile
profile = graph.get(USER_ID + '?fields=id,name,location,hometown,email')

# Get my latest posts 100 posts
feed = graph.get(USER_ID + '?fields=feed.order(chronological).limit(100)')

#********************Functions to run the script*************************************************

#--------------------Start of createfile() function----------------------------------------------
#Creating userdata.txt file in case it is not in cwd
def createfile():
  user_data_file = open(os.getcwd() + FILE_PATH, 'w')
  user_data_file.write(
    'Name: ' + profile['name'] +
    '\nFB User ID: ' + profile['id'] +
    '\nEmail: ' + profile['email'] + 
    '\nHometown: ' + profile['hometown']['name'] +
    '\nCurrent Location: ' + profile['location']['name'] +
    '\n' + ('-' * 35))

  user_posts = []
  for post in feed['feed']['data']:
    if 'message' in post:
      user_posts.append(post)

  for post in user_posts:
    user_data_file.write(
      '\nDate&Time created: ' + post['created_time'] +
      '\nPost ID: ' + post['id'] +
      '\n' + post['message'] + 
      '\n'+('-')*80)

  user_data_file.close()

  print(
    'Name: ' + profile['name'] +
    '\nFB User ID: ' + profile['id'] +
    '\nEmail: ' + profile['email'] + 
    '\nHometown: ' + profile['hometown']['name'] +
    '\nCurrent Location: ' + profile['location']['name'] +
    '\n'+('-')*80)

  for post in user_posts:
    print('\nDate&Time created: ' + post['created_time'])
    print('\nPost ID: ' + post['id'])
    print('\n' + post['message'])
    print('\n'+('-')*80)
#--------------------------------End of createfile() function--------------------------------------------

#--------------------------------Start of manage_posts() function----------------------------------------

def manage_posts():
  f = open(FILE_PATH, 'r')
  content = f.read()
  f.close()

  for post in feed['feed']['data']:
    if 'message' in post:
      id_user_regex = re.compile(post['id'])
      if not id_user_regex.search(content):
        f = open('./userdata.txt', 'r')
        lines_list = f.readlines()
        f.close()
        lines_list.insert(6, 'Date&Time created: ' + post['created_time'] +
          '\nPost ID: ' + post['id'] +
                          '\n' + post['message'] + 
                          '\n'+('-')*80+'\n')
        user_data_file = open('./userdata.txt', 'w')
        user_data_file.writelines(lines_list)
        user_data_file.close()
        print('...............New entry was added.........................')
      else:
        print('This post is already in userdata.txt file. Post id: ' + post['id'])


#--------------------------------End of manage_posts() function------------------------------------------

#********************************End of Functions Section************************************************


if not os.path.isfile('./userdata.txt'):
  createfile()
  print('Successfully created userdata.txt file')
else:
  print('File userdata.txt already exists')
  manage_posts()
