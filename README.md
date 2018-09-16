# avelresearchtestapp
## Automate your WP posts from the comfort of your terminal!
### Sample codebase to access FB Graph API and post on WP site without even opening wp-admin

If you work closely with WP sites content management and write posts for more and more clients, you may feel that it takes more and more time to write all those new posts and add new content. The scripts we provide allow you to optimize your workflow to certain extend. If you follow closely certain FB users, pages, or organizations and re-post their public messages then you should consider using our script which is created to allow busy people like you to add new posts to the sites you are in charge of in a matter of seconds.

This script accesses data from the Facebook user profile.<br/>
In order to use the Graph API we should register our app on [developers.facebook.com](https://developers.facebook.com)<br/>
After the registration and confirmation process is finished we can obtain `ACCESS TOKEN`.<br/>
`user_posts.py` script allows to extract FB User's public personal data and public posts and creates a text file where all the extracted data is stored.<br/>
`wp_posts.py` script allows to extract FB User's public messages and adds them as posts to your WP site

---
### Running the script

Make sure to run this script in Python.3.x environment

Executing the script:
- `git clone https://github.com/Villian79/avelresearchtestapp.git`
- `cd avelresearchtestapp`
- `pip install facepy` - installing 3rd party Python module [Facepy](https://github.com/jgorset/facepy)
- `pip install python-wordpress-xmlrpc` - installing 3rd party Python module [python-wordpress-xmlrpc](https://python-wordpress-xmlrpc.readthedocs.io/en/latest/)
- `python wp_posts.py` - to add posts to your WP site
- or `python user_posts.py` - to simply extract data and add save it in .txt file

Add configuration details in `config.ini` file:
- [App] `access_token` - current value of the access token issued by Graph API
- [User] `id` - target User's FB id
- [WP_User] `username` - username for the WP site you work with
- [WP_User] `password` - password for the WP site you work with

Note:<br/>
At the moment owner of the current app has access only to his personal data.<br/>
To get full access to FB Graph API endpoints potentional real app owner has to submit additional.<br/>
information to FB. After review permissions to use certain query endpoints will be granted by FB.<br/>

---
### Usage

`wp_posts.py`

Make sure to input all the required config details in `config.ini` file

On each run of the script the target FB User's data is collected and added to your WP site in form of posts.

<hr>

`user_posts.py`

On the first run of the script a new userdata.txt file is created in cwd where target User's data is pushed

On each next run of the script the target FB User's data is collected and checked agains data existing in userdata.txt. If new posts exist - they are automatically added

While running the script we send GET requests to various Graph API endpoints using Facepy Graph API module.<br/>
Requests are passed to the `graph.facebook.com` host URL.

Reading operations almost always begin with a node. A node is an individual object with a unique ID.<br/>
`GET https://graph.facebook.com/820882001277849`<br/>
Result of such GET request is as follows:

```
{
  "name": "Coca-Cola",
  "id": "820882001277849"
}
```

<hr>

In this app we used two main GET requests paths:
- `GET https://graph.facebook.com/XXXXXXXXXXXXXX?fields=id,name,location,hometown,email` - extracting User's public personal information
- `GET https://graph.facebook.com/XXXXXXXXXXXXXX?fields=feed.order(chronological).limit(100)` - extracting User's latest 100 public posts



