# gpe-shift-parser
Parse shifts from CSV and put them in a google sheets document.

# Requirements
* Python 2
* `pip install urllib2`
* [Google Cloud](https://console.cloud.google.com/) 'WAP Client' credentials (for editing gdrive/gsheets) as `./credentials.json`
* [Babalooey](https://www.babalooey.com/) Admin Credentials stored in `./babalooey-cred` as `*username*,*password*`. Example: `johnsmith@gmail.com,Appl3`
: 

# Run
`python main.py`
