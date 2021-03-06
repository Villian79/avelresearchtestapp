#! python3
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.methods.posts import NewPost

from facepy import GraphAPI
from configparser import ConfigParser

#Get config data
if __name__ == '__main__':
  cfg = ConfigParser()
  cfg.read('config.ini')
  ACCESS_TOKEN = cfg.get('App','access_token')
  FILE_PATH = cfg.get('App', 'file_path')
  USER_ID = cfg.get('User', 'id')
  WP_USERNAME = cfg.get('WP_User', 'username')
  WP_PASSWORD = cfg.get('WP_User', 'password')
  WP_SITE_LINK = cfg.get('WP_User', 'wp_site_link')

# Initialize the Graph API with a valid access token (optional, but will allow you to do all sorts of fun stuff).
graph = GraphAPI(ACCESS_TOKEN)
# Get the User profile
profile = graph.get(USER_ID + '?fields=id,name,location,hometown,email')

# Get my latest posts 100 posts
feed = graph.get(USER_ID + '?fields=feed.order(chronological).limit(100)')

#Create an instance of WP client
wp = Client(WP_SITE_LINK, WP_USERNAME, WP_PASSWORD)

wp_posts = wp.call(posts.GetPosts({'number': 1000, 'orderby': 'date', 'order': 'DESC', 'post_status': 'publish'}))

#Create a list of all existing FB ids in our blog
wp_post_fb_ids = []
for wp_post in wp_posts:
  wp_post_fb_ids.append(wp_post.custom_fields[0]['value'])

#Check if FB post contains 'message' field 
user_posts = []
for post in feed['feed']['data']:
  if post['id'] in wp_post_fb_ids:
    print('Post is already in database')
  else:
    if 'message' in post:
      user_posts.append(post)
      print('Post with id ' + post['id'] + ' was added to the database')

for user_post in user_posts:
  #Post creation and publishing
  post = WordPressPost()
  post.title = 'Exciting new post: ' + user_post['id']
  post.content = user_post['message']
  post.post_status = 'publish'
  post.custom_fields = [{'key': 'facebook_id', 'value': user_post['id']}]
  wp.call(NewPost(post))
