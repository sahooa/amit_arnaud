#!/usr/bin/python
import urllib2
import json,subprocess
import MySQLdb

url = "http://assessment.skubana.com/orders"

contents = json.load(urllib2.urlopen(url))
db = MySQLdb.connect(host= "test.c0xemrcczxat.us-east-2.rds.amazonaws.com",
                  user="admin",
                  passwd="password",
                  db="test")
cur = db.cursor()

#cur.execute("""TRUNCATE TABLE ORDERS""")
#cur.execute("""TRUNCATE TABLE ORDERITEMS""")
for i in range(len(contents)):
    order_no = contents[i]["orderNumber"]
    ship_country = contents[i]['shipToAddress']['country']
    ship_addr_1 = contents[i]['shipToAddress']['line1']
    ship_addr_2 = contents[i]['shipToAddress']['line2']
    name = contents[i]['shipToAddress']['name']
    postal_code = contents[i]['shipToAddress']['postalCode']
    state = contents[i]['shipToAddress']['stateProvince']
    cur.execute("""INSERT INTO ORDERS VALUES (%s,%s,%s,%s,%s,%s,%s)""",(order_no,name,ship_addr_1,ship_addr_2,state,postal_code,ship_country))
    db.commit()
    for j in range(len(contents[i]["orderItems"])):
        qty = contents[i]["orderItems"][j]["quantity"]
        sku = contents[i]["orderItems"][j]["sku"]
        cur.execute("""INSERT INTO ORDERITEMS VALUES (%s,%s,%s)""",(order_no,qty,sku))
        db.commit()

#        print qty,sku
#    print order_no,name,ship_country,ship_addr_1,ship_addr_2,state,postal_code
db.close()
command = 'sudo apachectl restart'
process = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
output, error = process.communicate()

