import requests
import csv
from flask import Flask,send_file
import flask

app = Flask(__name__)

def scrape_data():
    try:
        columns = ["open", "high", "low", "ltP","ptsC","per","trdVol","ntP","symbol"]
        column_dict = {"open": "Open", "high": "High", "low": "Low", "ltP": "LTP", "ptsC": "Chng", "per": "% Chng",
               "trdVol": "Volume-lacs", "ntP": "Turnover-crs","symbol":"Company Name"}
        response = requests.get("https://www.nseindia.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json")

        excel_sheet = []
        for i in response.json()['data']:
            excel_sheet.append({column_dict[f]: i.get(f) for f in columns})
        with open('stock.csv', 'w',newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, excel_sheet[0].keys())
            dict_writer.writeheader()
            print(excel_sheet)
            dict_writer.writerows(excel_sheet)
            print("test")
    except Exception as e:
        print(e)
        return flask.jsonify({"message":"No internet connection"})
    # send_file()
# import time
# while 1:
#     scrape_data()
#     time.sleep(10)
@app.route("/stock")
def download():
    data = scrape_data()
    if(data):
        return data
    return send_file("stock.csv", as_attachment=True)

if __name__ =='__main__':
    app.run()
