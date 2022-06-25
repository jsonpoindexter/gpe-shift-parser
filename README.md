# gpe-shift-parser
Parse shifts from an online Babalooey CSV and save the WAP status to a local CSV and put them in a Google Sheets document hosted on Google Drive.

# Requirements
* Python 2
* `pip install -r requirements.txt`
* [Google Cloud](https://console.cloud.google.com/) 'WAP Client' credentials (for editing gdrive/gsheets) as `./credentials.json`
* [Babalooey](https://www.babalooey.com/) Admin Credentials stored in `./babalooey-cred` as `*username*,*password*`. Example: `johnsmith@gmail.com,Appl3`


# Run
`python main.py`

The script will then connect to Babalooey, download the current volunteer shifts, apply logic to shifts to calculate WAP status, and then output a local CSV of results as well as create a new gsheet. 