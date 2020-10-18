from flask import *
import csv
from datetime import date
from pprint import pprint

filename = "grocery_inventory_1.csv"

app = Flask(__name__, template_folder="templates")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/index.html')
def ohome():
    return render_template("index.html")

@app.route('/data.html')
def data():
    if request.method == "POST":
      name = request.form["Product Name"]
      exp = request.form["Expiration Date"]
      price = request.form["Price"]
      adict = {'Date Received': datetime.today(),
              'Expiration Date': exp,
              'Normal Total Price': '',
              'Normal Unit Price': price,
              'Product Name': name,
              'Quantity': '',
              'Sale Percentage': '',
              'Sale Total Price': '',
              'Sale Unit Price': '',
              'Shipment ID': ''}
      with open(filename, "a", newline="") as fout:
        writer = csv.DictWriter(fout, fieldnames=adict.keys())
        writer.writerow(adict)
    else:
      return render_template("data.html")

@app.route('/products.html')
def products():
    tup = sale(filename)
    return render_template("products.html", exp=tup[0], name=tup[1], oprice=tup[2], nprice=tup[3], save=tup[4])

@app.route('/login.html', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    else:
        return render_template("login.html")

# def join_csv(old, new):
#     biglist = []
#     with open(new, encoding="utf8") as fin:
#         reader = csv.DictReader(fin)
#         reader = [dict(i) for i in reader if dict(i)["Shipment ID"]]
#         biglist += reader

#     with open(old, "a", newline="") as fout:
#         writer = csv.DictWriter(fout, fieldnames=biglist[0].keys())
#         writer.writerows(biglist)

#     return biglist

def sale(file):
    with open(file, encoding="utf-8") as fin:
        reader = csv.DictReader(fin)
        reader = [dict(i) for i in reader]

    biglist = []
    today = date.today()

    for i in reader:
        day = i["Expiration Date"].split("/")[1]
        month = i["Expiration Date"].split("/")[0]
        year = i["Expiration Date"].split("/")[2]
        d = date(int(year), int(month), int(day))

        if (d - today).days <= 3:
            up = round(float(i["Normal Unit Price"].strip())*0.6, 2)
            tp = round(float(i["Normal Total Price"].strip())*0.6, 2)
            us = round(float(i["Normal Unit Price"].strip())*0.4, 2)
            ts = round(float(i["Normal Total Price"].strip())*0.4, 2)
            biglist.append({"Shipment ID":i["Shipment ID"], "Product Name":i["Product Name"], "Quantity":i["Quantity"], \
                            "Date Received":i["Date Received"], "Expiration Date":i["Expiration Date"], "Normal Unit Price":i["Normal Unit Price"], "Normal Total Price":i["Normal Total Price"], \
                            "Sale Percentage":50, "Sale Unit Price":up, "Sale Total Price":tp, "Unit Savings":us, "Total Savings":ts})
        elif (d - today).days <= 7:
            up = round(float(i["Normal Unit Price"].strip())*0.8, 2)
            tp = round(float(i["Normal Total Price"].strip())*0.8, 2)
            us = round(float(i["Normal Unit Price"].strip())*0.2, 2)
            ts = round(float(i["Normal Total Price"].strip())*0.2, 2)
            biglist.append({"Shipment ID":i["Shipment ID"], "Product Name":i["Product Name"], "Quantity":i["Quantity"], \
                            "Date Received":i["Date Received"], "Expiration Date":i["Expiration Date"], "Normal Unit Price":i["Normal Unit Price"], "Normal Total Price":i["Normal Total Price"], \
                            "Sale Percentage":20, "Sale Unit Price":up, "Sale Total Price":tp, "Unit Savings":us, "Total Savings":ts})

    biglist.sort(key=lambda x:x["Expiration Date"])

    name = []
    oprice = []
    nprice = []
    exp = []
    save = []

    for adict in biglist:
        name.append(adict["Product Name"])
        oprice.append(adict["Normal Unit Price"])
        nprice.append(adict["Sale Unit Price"])
        exp.append(adict["Expiration Date"])
        save.append(adict["Unit Savings"])

    return (exp, name, oprice, nprice, save)

app.run(debug=True)