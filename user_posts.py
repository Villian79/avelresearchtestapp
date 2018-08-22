#! python3
#This is the script to access data from the Facebook user profile
#In order to use the Graph API we should register our app on https://developers.facebook.com
#After the registration and confirmation process is finished we can obtain ACCESS TOKEN

#To run this script make sure to install 3rd party Python module Facepy: https://github.com/jgorset/facepy
#To do so run this command in your command line: `pip install facepy`

from facepy import GraphAPI
import os, re
from pprint import pprint

# Initialize the Graph API with a valid access token (optional, but will allow you to do all sorts of fun stuff).
graph = GraphAPI('EAAeZATZBKTs2oBAC3i7OVytZBLfYVIoUQYuucMas2F0SoBuyqDxkfo9tv0G7w44wZApCi0GE2ZAgpZCzkTqUblCctdaE76BcMl5FLku0UZAaxcKHbpoMwfWVN5ctIL8YK2PELIWALzZCcT4My8bwLqmhJtlkRrbcaKcZD')

# Get the User profile
# Numerical '2091816324224785' part of the query is the User Facebook id
# At the moment owner of the current app has access only to his personal data
# To get full access to FB Graph API endpoints potentional real app owner has to submit additional
# information to FB. After review permissions to use certain query endpoints will be granted by FB.

profile = graph.get('2091816324224785?fields=id,name,location,hometown,email')

# Get my latest posts 100 posts
feed = graph.get('2091816324224785?fields=feed.order(chronological).limit(100)')

#********************Functions to run the script*************************************************

#--------------------Start of createfile() function----------------------------------------------
#Creating userdata.txt file in case it is not in cwd
def createfile():
  #Writing User data and Latest posts to a .txt file
  user_data_file = open('./userdata.txt', 'w')
  user_data_file.write(
    'Name: ' + profile['name'] +
    '\nFB User ID: ' + profile['id'] +
    '\nEmail: ' + profile['email'] + 
    '\nHometown: ' + profile['hometown']['name'] +
    '\nCurrent Location: ' + profile['location']['name'] +
    '\n' + ('-' * 35))

  #Check all posts from FB and choose those that include 'message' key
  user_posts = []
  for post in feed['feed']['data']:
    if 'message' in post:
      user_posts.append(post)

  #Write chosen posts to userdata.txt file
  for post in user_posts:
    user_data_file.write(
      '\nDate&Time created: ' + post['created_time'] +
      '\nPost ID: ' + post['id'] +
      '\n' + post['message'] + 
      '\n'+('-')*80)

  user_data_file.close()

  #Print out results to console
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
  #Open userdata.txt to read it's contents
  f = open('./userdata.txt', 'r')
  content = f.read()
  f.close()

  #Check all posts from FB and choose those that have 'message' key
  for post in feed['feed']['data']:
    if 'message' in post:
      #Check if the post with a given 'id' exists in the userdata.txt file using RegEx
      id_user_regex = re.compile(post['id'])
      #If the post is not included in the userdata.txt file - create a new entry
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



#Check if the userdata.txt file to store our information exists in the cwd
#If id doesn't exist - Create one
#If it exists - Manage data in it
if not os.path.isfile('./userdata.txt'):
  createfile()
  print('Successfully created userdata.txt file')
else:
  print('File userdata.txt already exists')
  manage_posts()
