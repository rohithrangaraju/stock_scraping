import requests
import csv
from flask import Flask,send_file

app = Flask(__name__)
# def send_file():
#     ################
#     r=requests.post(
#         "https://api.mailgun.net/v3/sandbox1fff490055d543bf9c519e6c0cd79f76.mailgun.org/messages",
#         auth=("api", "key-24b8fa4a57e82acb09510deae09baa57"),
#         files=[("attachment", open("stock.csv",'r'))],
#         data={"from": "Mailgun Sandbox <postmaster@sandbox1fff490055d543bf9c519e6c0cd79f76.mailgun.org>",
#               "to": "<malay.bhayani1994@gmail.com>",
#               "subject": "STOCK ATTACHMENT",
#               "text": "LATEST STOCKS"}
#     )
#     print(r.json())

def scrape_data():
    columns = ["open", "high", "low", "ltP","ptsC","per","trdVol","ntP","symbol"]
    column_dict = {"open": "Open", "high": "High", "low": "Low", "ltP": "LTP", "ptsC": "Chng", "per": "% Chng",
               "trdVol": "Volume-lacs", "ntP": "Turnover-crs","symbol":"Company Name"}
    response = requests.get("https://www.nseindia.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json")

    excel_sheet = []
    for i in response.json()['data']:
        excel_sheet.append({column_dict[f]: i.get(f) for f in columns})
    with open('stock.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, excel_sheet[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(excel_sheet)
    # send_file()
# import time
# while 1:
#     scrape_data()
#     time.sleep(10)
@app.route("/stock")
def download():
    scrape_data()
    return send_file("stock.csv", as_attachment=True)

if __name__ =='__main__':
    app.run()
