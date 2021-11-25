from MySQLdb.cursors import Cursor
from flask import Flask, render_template, request,jsonify
from flask_mysqldb import MySQL
import pandas as pd
import numpy as np
import pymysql

app = Flask(__name__)

app.config['SECRET_KEY'] = 'otp'

app.config['MYSQL_HOST'] = 'clinicalfirst.com'
app.config['MYSQL_USER'] = 'u6hsxtqez2n9d'
app.config['MYSQL_PASSWORD'] = 'cfdbdev@3210'
app.config['MYSQL_DB'] = 'dbsoooy7zbgd0x'

mysql = MySQL(app)
ID = "null"

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("Df_Messenger.html")


@app.route('/customerdetails', methods=['GET', "POST"])  # URL pattern
def customerdetails():
    req = request.get_json()
    try:
        var = {
            "queryInput": {
                "text": {
                    "text": "END_USER_INPUT"
                },
                "languageCode": "en"
            },
            "queryParams": {
                "timeZone": "America/Los_Angeles"
            }
        }
        global ID
        ID = req.get("text")
        print(ID)
        cur = mysql.connection.cursor()
        print("cur")
        cur.execute("select telephone from cf_2_customer where telephone=%s",(ID,))
        print("excuted")
        mysql.connection.commit()
        fetchdata = cur.fetchone()
        if fetchdata:
            print(fetchdata)
            if ID == fetchdata[0]:
                response = {
                    "fulfillment_response": {
                        "messages": [{
                            "payload":
                                {
                                    "richContent": [
                                        [
                                            {
                                                "title": "Our Services",
                                                "type": "info",
                                                "subtitle": "Please choose one of the services below."
                                            },
                                            {
                                                "type": "chips",
                                                "options": [
                                                    {
                                                        "text": [
                                                            "Order Tracking"
                                                        ]
                                                    },
                                                    {
                                                        "text": [
                                                            "My Orders"
                                                        ]
                                                    },
                                                    {
                                                        "text": [
                                                            "Notifications"
                                                        ]
                                                    },
                                                    {
                                                        "text": [
                                                            "Support"
                                                        ]
                                                    }

                                                ]
                                            }
                                        ]
                                    ]
                                }
                        }]
                    }
                }
                return response
        else:
            response = {
                "fulfillment_response": {
                    "messages": [{
                        "payload":
                            {
                                "richContent": [
                                    [
                                        {
                                            "type": "description",
                                            "title": "Mobile Number Varification status",
                                            "text": [
                                                "Sorry it seems like you are not registered with us. if you want to use the service you have to register with clinicalfirst Ecommerce website"]
                                        }
                                    ]
                                ]
                            }
                    }]
                }
            }
        return response
    except:
        return ("exception occured")

@app.route('/customerconformation', methods=['GET', "POST"])  # URL pattern
def customerconformation():
    req = request.get_json()
    try:
        global ID
        print(ID)
        if request.method == "POST":
            cur = mysql.connection.cursor()
            print("cur")
            P_D = '"' + ID + '"'
            P_D = ''.join('(' + P_D + ')')
            print(P_D)
            cur.execute("select order_id from cf_2_order as cfo inner join cf_2_customer as cfc on cfo.customer_id = cfc.customer_id where cfc.telephone in" +P_D)
            print("cur")
            mysql.connection.commit()
            info = cur.fetchall()
            print(info)
            cur.close()
            response = {
                "fulfillment_response": {
                    "messages": [{
                        "payload":
                            {
                                "richContent": [
                                    [
                                        {
                                            "title": "Orders List",
                                            "type": "info",
                                            "subtitle": "select particular Order Id which you want to track the details from the given OrderIds"
                                    },
                                    {
                                        "type": "chips",
                                        "options": [

                                        ]
                                    }
                                ]
                            ]
                        }
                }]
            }
        }
        for i in info:
            response['fulfillment_response']['messages'][0]['payload']['richContent'][0][1]['options'].append(
                {'text': i})
        # time.sleep(3)
        return response
    except:
        return ("exception occured")

@app.route('/order_tracking', methods=["POST"])
def order_tracking():
    req = request.get_json()
    try:
        status = req.get("text")
        print(status)
        if request.method == "POST":
            cur = mysql.connection.cursor()
            print("cur")
            order_id = '"' + status + '"'
            order_id = ''.join('(' + order_id + ')')
            print(order_id)
            cur.execute("select cf2s.name from cf_2_order_status as cf2s inner join cf_2_order_history as cf2h on cf2s.order_status_id= cf2h.order_status_id where order_id  in" + order_id)
            print("executed")
            mysql.connection.commit()
            info = cur.fetchone()
            print(info)
            cur.close()
            response = {
                "fulfillment_response": {
                    "messages": [{
                        "payload":
                            {
                                "richContent": [
                                    [
                                        {
                                            "type": "description",
                                            "title": "Here is the status of your selected order",
                                            "text": []
                                        }
                                    ]
                                ]
                            }
                    }]
                }
            }
            for i in info:
                response['fulfillment_response']['messages'][0]['payload']['richContent'][0][0]['text'].append(i)
            #time.sleep(3)
            return response
        return jsonify('tests added successfully')
    except:
        return "Exception occure"


@app.route('/orderhistory', methods=['GET', "POST"])
def orderhistory():
    try:
        if request.method == "POST":
            cur = mysql.connection.cursor()
            print("cur")
            P_D = '"' + ID + '"'
            P_D = ''.join('(' + P_D + ')')
            print(P_D)
            cur.execute("select order_id from cf_2_order as cfo inner join cf_2_customer as cfc on cfo.customer_id = cfc.customer_id where cfc.telephone in" +P_D)
            print(cur)
            mysql.connection.commit()
            info = cur.fetchall()
            print(info)
            cur.close()
            response = {
                "fulfillment_response": {
                    "messages": [{
                        "payload":
                            {
                                "richContent": [
                                    [
                                        {
                                            "title": "Orders List",
                                            "type": "info",
                                            "subtitle": "select particular Order Id which you want to know the details from the given OrderIds"
                                        },
                                        {
                                            "type": "chips",
                                            "options": [

                                            ]
                                        }
                                    ]
                                ]
                            }
                    }]
                }
            }
            for i in info:
                response['fulfillment_response']['messages'][0]['payload']['richContent'][0][1]['options'].append(
                    {'text': i})
            # time.sleep(3)
            return response
    except:
        return ("exception occured")

@app.route('/orderinfo', methods=["POST"])
def orderinfo():
    req = request.get_json()
    try:
        status = req.get("text")
        print(status)
        if request.method == "POST":
            cur = mysql.connection.cursor()
            print("cur")
            order_id = '"' + status + '"'
            order_id = ''.join('(' + order_id + ')')
            print(order_id)
            cur.execute("select cf_2_order.order_id,cf_2_order_product.name,cf_2_order_product.quantity,cf_2_order_product.price,cf_2_order_product.total,cf_2_order.date_added, cf2os.name from cf_2_order join cf_2_order_product on cf_2_order.order_id = cf_2_order_product.order_id join cf_2_order_status as cf2os on cf_2_order.order_status_id = cf2os.order_status_id where cf_2_order.order_id in" + order_id)
            print("executed")
            mysql.connection.commit()
            info = cur.fetchone()
            #keys = ("OrderID", "Product_Name", "Quantity", "Unit_Price", "Total_Price", "Date_time")
            #print(info)
            #data = get_list_of_dict(keys, info)
            #print(data)
            cur.close()
            response = {
                "fulfillment_response": {
                    "messages": [{
                        "payload":
                            {
                                "richContent": [
                                    [
                                        {
                                            "type": "description",
                                            "title": "Here is the information of your selected order",
                                            "text": []
                                        }
                                    ]
                                ]
                            }
                    }]
                }
            }
            for i in info:
                response['fulfillment_response']['messages'][0]['payload']['richContent'][0][0]['text'].append(i)
            #time.sleep(3)
            return response
        return jsonify('tests added successfully')
    except:
        return "Exception occure"

#def get_list_of_dict(keys, list_of_tuples):
    #list_of_dict = [dict(zip(keys, values)) for values in list_of_tuples]
    #return list_of_dict


if __name__ == '__main__':
    app.run(debug=True)

