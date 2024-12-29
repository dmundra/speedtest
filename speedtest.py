import os.path

from google.auth.transport.requests import Request
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import subprocess
import json
import sys

def main():
  creds = None
  if os.path.exists("credentials.json"):
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", [])

  try:
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
      
    result = subprocess.run(["speedtest-cli", "--json", "--bytes"], stdout=subprocess.PIPE)
    output_cli = result.stdout
    output_json = json.loads(output_cli)
    
    values = [[
      sys.argv[1],
      output_json["server"]["id"],
      output_json["server"]["name"],
      output_json["timestamp"],
      output_json["server"]["d"],
      output_json["server"]["latency"],
      output_json["download"] / (1024 * 1024),
      output_json["upload"] / (1024 * 1024),
      output_json["client"]["ip"],
    ]]

    body = {'values': values}
    result = service.spreadsheets().values().append(
        spreadsheetId="1Lle-HhKmeC5Q08U6GeLQjtsfP6GV4V7x8RacQws-jzA", range="Sheet1!A1:J",
        valueInputOption="RAW", body=body).execute()
    
  except HttpError as err:
    print(err)

if __name__ == "__main__":
  main()
