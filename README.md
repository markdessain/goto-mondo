# GoToMondo

####Built by:
- https://www.github.com/markdessain
- https://www.github.com/scottrobertson

####Description:
GoToMondo was built during the third hackathon run by https://getmondo.co.uk/. It uses the Mondo API which provides realtime data, enriches it with FourSquare data to suggest alternative places to go to, stopping you from falling into a routine. 

![Preview](https://raw.githubusercontent.com/markdessain/gotomondo/master/preview.png)

####Caution:
 - To be used by *developers only*. You need to manually add your account_id and access_tokens into the environment and run your own server. Please do not do this if you're unsure what you're doing. The app will post items to your feed.

####Install:
- Install Python 3.x and pip
  - https://www.python.org/downloads/
- Install redis 3.x
  - http://redis.io/download 
  - http://redis.io/topics/quickstart
- pip install -r python/requirements.txt
- Set the environment variables
  - Add to .env or export into shell

####Run:
- honcho start

####Environment Variables:
- LOG_LEVEL: 
  - The Python log level. Set to debug when developing.
- MONDO_ENV: 
  - The URL to the Mondo API
  - https://staging-api.getmondo.co.uk
  - https://api.getmondo.co.uk/
- MONDO_VISIT_COUNT:
  - After how many visits do you want the feed alerts to start happening
- MONDO_ACCOUNT_1:
  - Currently hardcode 
  - [account_id]:[account_access_token]
- MONDO_ACCOUNT_2:
  - Currently hardcode 
  - [account_id]:[account_access_token]
- MONDO_ACCOUNT_3:
  - Currently hardcode 
  - [account_id]:[account_access_token]
- MONDO_ACCOUNT_4:
  - Currently hardcode 
  - [account_id]:[account_access_token]
- FOURSQUARE_CLIENT_ID: 
  - https://developer.foursquare.com/
- FOURSQUARE_CLIENT_SECRET
  - https://developer.foursquare.com/
- FOURSQUARE_API_VERSION
  - Default: 20160109
- REDIS_URL
  - Default: redis://localhost:6379 
- PAGE_URL
  - Path to view your . The suggestions will direct back to the /suggestions page
