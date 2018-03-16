import MySQLdb
from flask import Flask,request,g
app = Flask(__name__)


db = MySQLdb.connect(host= "test.c0xemrcczxat.us-east-2.rds.amazonaws.com",
                  user="admin",
                  passwd="password",
                  db="test")
cur = db.cursor()

@app.route('/topsku/<input_int>')
def viewdb(input_int):
        cur.execute("select * from (SELECT sku,sum(qty) FROM test.ORDERITEMS group by sku order by sum(qty) desc) A limit %s",(int(input_int),))
        #return "Hi"
        data = cur.fetchall()
        return_data = '<br>'.join(str(row) for row in data)
        return return_data

@app.route('/topskubycountry/<input_int>')
def viewdb_bysku(input_int):
        cur.execute("select * from (SELECT country,sku,sum(qty) FROM test.ORDERITEMS A join test.ORDERS B on A.Order_No=B.Order_No where B.country IN ('United States','Canada','Mexico') group by country,sku order by B.country,sum(qty) desc) C limit %s",(int(input_int),))
        #return "Hi"
        data = cur.fetchall()
        return_data = '<br>'.join(str(row) for row in data)
        return return_data

@app.route('/avgorders')
def avg_orders():
	cur.execute("select count(Order_No)/count(distinct Order_No) from test.ORDERITEMS")
	data = cur.fetchall()
	return_data = '<br>'.join(str(row) for row in data)
        return return_data    



if __name__ == '__main__':
  app.run()
