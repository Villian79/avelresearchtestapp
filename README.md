# avelresearchtestapp
## Sample codebase to test FB Graph API

This is the script to access data from the Facebook user profile.<br/>
In order to use the Graph API we should register our app on [developers.facebook.com](https://developers.facebook.com)<br/>
After the registration and confirmation process is finished we can obtain `ACCESS TOKEN`.<br/>
This script allows to extract FB User's public personal data and public posts and creates a text file where all the extracted data is stored.<br/>

---
### Running the script

Make sure to run this script in Python.3.x environment

Add configuration details in `config.ini` file:
- `access_token` - value of the access token issued by Graph API
- `user_id` - target User's FB id

Install 3rd party Python module [Facepy](https://github.com/jgorset/facepy)<br/>
To do so run this command in your command line: `pip install facepy`

Note:<br/>
At the moment owner of the current app has access only to his personal data.<br/>
To get full access to FB Graph API endpoints potentional real app owner has to submit additional.<br/>
information to FB. After review permissions to use certain query endpoints will be granted by FB.<br/>

---

Enter directory where the file user_posts.py is located.<br/>
Run command `python user_posts.py` from within that directory.<br/>


---
### Usage

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

In this app we used two main GET requests paths:
- `GET https://graph.facebook.com/XXXXXXXXXXXXXX?fields=id,name,location,hometown,email` - extracting User's public personal information
- `GET https://graph.facebook.com/XXXXXXXXXXXXXX?fields=feed.order(chronological).limit(100)` - extracting User's latest 100 public posts



