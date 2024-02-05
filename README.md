[@StatsWiki](https://twitter.com/StatsWiki) (X/Twitter) & [@StatsWiki](https://www.instagram.com/statswiki/) (Instagram)

To install and run it:
* Open appTwitter.py, replace with your IDs.
* Open appInstagram.py, replace with your IDs.
* ```git clone https://github.com/benprieur/Twitbot-StatsWiki-WikiCommons.git```
* ```virtualenv venv```
* ```source venv/bin/activate```
* ```pip install -r requirements.txt```
* ```crontab -e```
```
* * * * * [your_directory]/venv/bin/python3 [your_directory]/appTwitter.py
0 1 * * * [your_directory]/venv/bin/python3 [your_directory]/appInstagram.py
```
