#!/usr/bin/python
# -*- coding: utf-8 -*-
############################################################################################
# File:     connectDB.py
# Author:   Kaia Chapman
# Version:  2.0
# Purpose:  Connect to database and create queries to:
#           1) Insert new reservation information
#           2) Cancel a reservation
#           3) Retrieve Information on a reservation by varius search criteria
#           4) Search for a flight matching parameters given throughout app
"""##########################################db_flyright####################################
PAYMENT:
+-----------+--------------+------+-----+---------------------+----------------+
| Field     | Type         | Null | Key | Default             | Extra          |
+-----------+--------------+------+-----+---------------------+----------------+
| id        | mediumint(9) |      | PRI | NULL                | auto_increment |
| amount    | decimal(7,2) |      |     | 0.00                |                |
| day       | datetime     |      |     | 0000-00-00 00:00:00 |                |
| method    | varchar(11)  |      |     |                     |                |
| number    | bigint(20)   |      |     | 0                   |                |
| ccv       | smallint(6)  |      |     | 0                   |                |
| card_date | datetime     |      |     | 0000-00-00 00:00:00 |                |
| card_name | varchar(30)  |      |     |                     |                |
+-----------+--------------+------+-----+---------------------+----------------+
RESERVATION:
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| id         | mediumint(9) |      | PRI | NULL    | auto_increment |
| payment_id | mediumint(9) |      | MUL | 0       |                |
+------------+--------------+------+-----+---------+----------------+
+----------------+--------------+------+-----+---------+----------------+
| Field          | Type         | Null | Key | Default | Extra          |
+----------------+--------------+------+-----+---------+----------------+
| id             | mediumint(9) |      | PRI | NULL    | auto_increment |
| customer_id    | mediumint(9) |      | MUL | 0       |                |
| reservation_id | mediumint(9) |      | MUL | 0       |                |
| seat_id        | mediumint(9) |      | MUL | 0       |                |
| meal           | tinyint(1)   |      |     | 0       |                |
| bags           | int(2)       |      |     | 0       |                |
| assist         | tinyint(1)   |      |     | 0       |                |
| comment        | varchar(200) | YES  |     | NULL    |                |
| class          | tinyint(1)   |      |     | 0       |                |
+----------------+--------------+------+-----+---------+----------------+
CUSTOMER:    
+---------+--------------+------+-----+---------+----------------+
| Field   | Type         | Null | Key | Default | Extra          |
+---------+--------------+------+-----+---------+----------------+
| id      | mediumint(9) |      | PRI | NULL    | auto_increment |
| fname   | varchar(20)  |      |     |         |                |
| lname   | varchar(30)  |      |     |         |                |
| address | varchar(200) |      |     |         |                |
| city    | varchar(50)  |      |     |         |                |
| zip     | int(11)      |      |     | 0       |                |
| email   | varchar(100) | YES  |     | NULL    |                |
+---------+--------------+------+-----+---------+----------------+
SEAT:
+-----------+--------------+------+-----+---------+----------------+
| Field     | Type         | Null | Key | Default | Extra          |
+-----------+--------------+------+-----+---------+----------------+
| id        | mediumint(9) |      | PRI | NULL    | auto_increment |
| position  | char(1)      |      |     |         |                |
| flight_id | mediumint(9) |      | MUL | 0       |                |
| available | tinyint(1)   |      |     | 1       |                |
+-----------+--------------+------+-----+---------+----------------+
FLIGHT:
+-------------------+--------------+------+-----+---------------------+----------------+
| Field             | Type         | Null | Key | Default             | Extra          |
+-------------------+--------------+------+-----+---------------------+----------------+
| id                | mediumint(9) |      | PRI | NULL                | auto_increment |
| depart_airport_id | mediumint(9) |      | MUL | 0                   |                |
| arrive_airport_id | mediumint(9) |      | MUL | 0                   |                |
| depart_dt         | datetime     |      |     | 0000-00-00 00:00:00 |                |
| arrive_dt         | datetime     |      |     | 0000-00-00 00:00:00 |                |
| rate_id           | mediumint(9) |      | MUL | 0                   |                |
+-------------------+--------------+------+-----+---------------------+----------------+
AIRPORT:
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | mediumint(9) |      | PRI | NULL    | auto_increment |
| city  | varchar(20)  |      |     |         |                |
| state | char(3)      |      |     |         |                |
| name  | varchar(4)   |      |     |         |                |
+-------+--------------+------+-----+---------+----------------+
RATE:
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| id         | mediumint(9) |      | PRI | NULL    | auto_increment |
| coach      | decimal(8,2) | YES  |     | NULL    |                |
| firstclass | decimal(8,2) | YES  |     | NULL    |                |
| adjust     | decimal(4,2) | YES  |     | 0.00    |                |
+------------+--------------+------+-----+---------+----------------+
"""#########################################################################################
import datetime
import pymysql
from time import sleep

class connectDB:
    ###########################
    def __init__(self): #constuctor
        self.cnx = pymysql.connect(user='root', passwd='Redfox1!',
                                      host='127.0.0.1',
                                      db='db_flyright', port=3306)
        #declare vars to store in self
        self.cursor=self.cnx.cursor()
        self.customerIds=[]
        self.paymentId=0
        self.reservationId=0
        self.seatIds=[]
    ###########################

    ###########################
    def reset(self):
        """closes connection and resets self"""
        self.cnx.close()
        self.__init__()
    ###########################

    ##########################################################START lookups
    ###########################    
    def lookupId(self, resId):
        """Arg: a reservation id.
Returns nested arrays containing information on flight details such as:
flightNum, deptDate, deptTime, deptLoc, destDate, destTime, destLoc, passCount"""
        ###########################
        data=[]
        #TEST OPTIONS - DELETE vvv
        """
JOIN (
  SELECT count(cid) AS passenger_count, id
  FROM(
    SELECT c.id AS cid, r.id
    FROM reservation AS r
    JOIN passenger AS p ON r.id=p.reservation_id
    JOIN customer AS c ON c.id=p.customer_id
    GROUP BY c.id) AS dt
  GROUP BY id) AS pc
  """
        """
JOIN (
    SELECT r.id, count(p.id) AS passenger_count
    FROM reservation AS r
    JOIN passenger AS p ON p.reservation_id=r.id
    GROUP BY r.id) AS pc
"""
        self.cursor.execute("""SELECT r.id AS res_id,
f.depart_dt, da.city AS depart_city, da.state AS depart_state, da.name AS depart_name,
f.arrive_dt, aa.city AS arrive_city, aa.state AS arrive_state, aa.name AS arrive_name,
pc.passenger_count
FROM passenger AS p
JOIN seat AS s ON s.id=p.seat_id
JOIN flight AS f on f.id=s.flight_id
JOIN airport AS da ON da.id=f.depart_airport_id
JOIN airport AS aa on aa.id=f.arrive_airport_id
JOIN reservation AS r ON r.id=p.reservation_id
JOIN (
  SELECT count(cid) AS passenger_count, id
  FROM(
    SELECT c.id AS cid, r.id
    FROM reservation AS r
    JOIN passenger AS p ON r.id=p.reservation_id
    JOIN customer AS c ON c.id=p.customer_id
    GROUP BY c.id) AS dt
  GROUP BY id) AS pc
ON pc.id=r.id
WHERE r.id=%s
GROUP BY r.id""", (resId))
        for i in self.cursor:
            #print(i)
            data.append([str(i[0]),str(i[1]).split(" ")[0], str(i[1]).split(" ")[1], i[2]+", "+i[3]+" ("+i[4]+")", str(i[5]).split(" ")[0], str(i[5]).split(" ")[1], i[6]+", "+i[7]+" ("+i[8]+")", str(i[9])])
        [print(i) for i in data]
        return data
    ###########################END lookupId

    ###########################
    def lookupName(self, first, last, zipCode):
        """Arg: string first, string last, int zipCode
Returns nested arrays containing information on flight details such as:
flightNum, deptDate, deptTime, deptLoc, destDate, destTime, destLoc, passCount"""
        ###########################
        data=[]
        self.cursor.execute("""SELECT r.id AS res_id,
f.depart_dt, da.city AS depart_city, da.state AS depart_state, da.name AS depart_name,
f.arrive_dt, aa.city AS arrive_city, aa.state AS arrive_state, aa.name AS arrive_name,
pc.passenger_count
FROM customer AS c
JOIN passenger AS p ON p.customer_id=c.id
JOIN seat AS s ON s.id=p.seat_id
JOIN flight AS f on f.id=s.flight_id
JOIN airport AS da ON da.id=f.depart_airport_id
JOIN airport AS aa on aa.id=f.arrive_airport_id
JOIN reservation AS r ON r.id=p.reservation_id
JOIN (
  SELECT count(cid) AS passenger_count, id
  FROM(
    SELECT c.id AS cid, r.id
    FROM reservation AS r
    JOIN passenger AS p ON r.id=p.reservation_id
    JOIN customer AS c ON c.id=p.customer_id
    GROUP BY c.id) AS dt
  GROUP BY id) AS pc
ON pc.id=r.id
WHERE LOWER(fname) =LOWER(%s) AND LOWER(lname)=LOWER(%s) AND zip=%s
GROUP BY r.id""", (first, last, zipCode))
        for i in self.cursor:
            #print(i)
            data.append([str(i[0]),str(i[1]).split(" ")[0], str(i[1]).split(" ")[1], i[2]+", "+i[3]+" ("+i[4]+")", str(i[5]).split(" ")[0], str(i[5]).split(" ")[1], i[6]+", "+i[7]+" ("+i[8]+")", str(i[9])])
        [print(i) for i in data]
        return data
        ###########################END lookupName
    ##########################################################END lookups
    
    ##########################################################START confirm reservation
        ###########################    
    def confirmId(self, resId):
        """Arg: a reservation id.
Returns nested arrays containing information on:
s.class, depart_dt, depart_name,  depart_city,  depart_state,arrive_dt, arrive_name, arrive_city,  arrive_state
for 1 or more flights,
fname, lname, meal, bags, assist, comment
for 1 or more passengers
for use in confrim reservation dialog"""
        ########################### 
        flights=[]
        self.cursor.execute("""SELECT s.class,
depart_dt, da.name AS depart_name, da.city AS depart_city, da.state AS depart_state,
arrive_dt, aa.name AS arrive_name, aa.city AS arrive_city, aa.state AS arrive_state
FROM reservation AS r
JOIN passenger AS p ON p.reservation_id=r.id
JOIN seat AS s ON s.id=p.seat_id
JOIN flight AS f ON f.id=s.flight_id
JOIN airport AS da ON da.id=f.depart_airport_id
JOIN airport AS aa ON aa.id=f.arrive_airport_id
WHERE r.id=%s
GROUP BY f.id""",(resId))
        for i in self.cursor:
            flights.append([j for j in i])
        passengers=[]
        self.cursor.execute("""SELECT fname, lname, meal, bags, assist, comment
FROM reservation AS r
JOIN passenger AS p ON p.reservation_id=r.id
JOIN customer AS c ON c.id=p.customer_id
WHERE r.id=%s
GROUP BY c.id""",(resId))
        for i in self.cursor:
            passengers.append([j for j in i])
        if len(flights)>0 and len(passengers)>0:
            return flights, passengers
        else:
            print("Error in confirmID")
    ###########################END confirmID
    ##########################################################START confirm reservation
    
    ##########################################################START cancel reservation stack
    ###########################
    def cancelRes(self, resId):
        """Calls the sql procedures in order required to remove res info from all tables"""
        payDetails=self.selectPayment(resId)
        if payDetails:
            seatsAffected=self.freeSeats(resId)
            if seatsAffected:
                refundId=self.refundPayment(payDetails)
                if refundId:
                    lastPassId=self.deletePassenger(resId)
                    if lastPassId:
                        resAffected=self.deleteRes(resId)
                        if resAffected:
                            return payDetails
                        else:
                            print("!resAffected")
                    else:
                        print("!lastPassId")
                else:
                    print("!refundId")
            else:
                print("!seatsAffected")
        else:
            print("!payDetails")
    ###########################END cancelRes            
        
    ###########################
    def selectPayment(self, resId):
        """Finds a payment by resId and returns details on it for final cancel confirmation| false if not found"""
        ###########################
        self.cursor.execute("""SELECT p.id, amount,  method, number, ccv, card_date, card_name
FROM payment AS p JOIN reservation AS r ON r.payment_id=p.id
WHERE r.id=%s LIMIT 1""", (resId))
        for i in self.cursor:
            return i
        else:
            return False
    ###########################

    ###########################
    def freeSeats(self, resId):
        """finds seats by resId and puts in a temp table, updates those seats available column=0,
drops temp table, returns update statements' affectedCount for verification"""
        self.cursor.execute("""CREATE TEMPORARY TABLE sq (
    SELECT s.id, s.available FROM seat AS s
    JOIN passenger AS p ON p.seat_id=s.id
    JOIN reservation AS r ON r.id=p.reservation_id
    WHERE r.id=%s)""",(resId))
        self.cnx.commit()
        sleep(0.2)
        self.cursor.execute("SELECT available FROM sq")
        #for i in self.cursor:
            #print("i=",i)
        affectedCount=self.cursor.execute("UPDATE seat SET available=1 WHERE id IN(SELECT id FROM sq)")
        self.cnx.commit()
        sleep(0.2)
        #print("affectedCount=",affectedCount, " self.cursor.lastrowid=",self.cursor.lastrowid)
        self.cursor.execute("DROP TABLE sq")
        self.cnx.commit()
        return affectedCount
    ###########################END freeSeats

    ###########################
    def refundPayment(self, payDetails):
        """Inserts a new row in payment a new row with a negative dollar amount for the amount credited"""
        ###########################
        self.cursor.execute("""INSERT INTO payment
(amount, day, method, number, ccv, card_date, card_name)
VALUES (%s, %s, %s, %s, %s, %s, %s)
""",(float(payDetails[1]*(-1)), datetime.datetime.now().time().isoformat(), payDetails[2], payDetails[3], payDetails[4], payDetails[5], payDetails[6]))
        self.cnx.commit()
        return self.cursor.lastrowid
    ###########################

    ###########################
    def deletePassenger(self, resId):
        """finds passengers by resId, puts in temp table, deletes passengers in the table,
drops temp table, returns the affectedRows count of DELETE statement"""
        ###########################
        self.cursor.execute("""CREATE TEMPORARY TABLE sq (
SELECT p.id
FROM seat AS s JOIN passenger AS p ON p.seat_id=s.id
JOIN reservation AS r ON r.id=p.reservation_id
WHERE r.id=%s)
""",(resId))
        self.cnx.commit()
        affectedRows=self.cursor.execute("DELETE FROM passenger WHERE id IN(SELECT id FROM sq)")
        self.cnx.commit()
        self.cursor.execute("DROP TABLE sq")
        self.cnx.commit()
        return affectedRows
    ###########################
    
    ###########################
    def deleteRes(self, resId):
        """Wraps up reservation cancellation by finally deleting from reservation table"""
        ###########################
        affectedRows=self.cursor.execute("DELETE FROM reservation WHERE id=%s",(resId))
        self.cnx.commit()
        return affectedRows
    ###########################
    ##########################################################END cancel reservation stack

    ##########################################################START flight search
    ###########################        
    def flightSelectTableData(self, departAirport="LAX", departDate="", departTime="", arriveAirport="DFW", numPass=0, rate="C"):
        """parameters: departAirport, departDT(str), departTime(str), arriveAirport, numPass, rate(str='coach'||'firstclass')
    postcondition: returnsnested flightdata arras shaped like:
    [[[direct flight data]][[leg 1 of flight data][leg 2 of flight data]]]
    with each nested flight option data array will be ordered like:
    [departLoc, departTime, departDate, arriveLoc, arriveTime, arriveDate, coachCost||firstClassCost, flightID]"""
        rate="C" if rate=="coach" else "F"
        self.flightOpt=[]

        #select 1 leg table data from flights with depart & arrive airports matching provided params
        #and where available seats of right rate class >= numPass
        #TODO: need to check date provided = f.date when i put in more data to test
        self.cursor.execute("""
SELECT f.depart_dt, da.city AS depart_city, da.state AS depart_state, da.name AS depart_airport,
f.arrive_dt, aa.city AS arrive_city, aa.state AS arrive_state, aa.name AS arrive_airport, r.coach, r.firstclass, f.id
FROM flight AS f JOIN airport AS aa ON f.arrive_airport_id=aa.id
JOIN airport AS da ON f.depart_airport_id=da.id
JOIN rate AS r ON r.id=f.rate_id
JOIN(
    SELECT flight_id, count(flight_id) AS num_seats
    FROM seat AS s2 JOIN flight AS f2 ON s2.flight_id=f2.id
    JOIN airport AS aa2 ON f2.arrive_airport_id=aa2.id
    JOIN airport AS da2 ON f2.depart_airport_id=da2.id
    WHERE da2.name=%s AND aa2.name=%s
    AND s2.available='1'
    AND s2.class=%s
    GROUP BY flight_id) AS ns
ON f.id=ns.flight_id
WHERE ns.num_seats >= %s;
""" , (departAirport, arriveAirport, rate, numPass))

        self.appendFlightData(self.cursor, rate, 3)                   
        
        #select both of 2 leg table data from flights with first depart & second arrive airports matching provided params
        #and first arrive ariport=secord depart airport and where available seats of right rate class >= numPass
        #TODO: need to check date provided = f.date and add back in timing between legs when i put in more data to test
        self.cursor.execute("""
SELECT f1.depart_dt, f1da.city AS depart_city, f1da.state AS depart_state, f1da.name AS depart_airport,
f1.arrive_dt, f1aa.city AS arrive_city, f1aa.state AS arrive_state, f1aa.name AS arrive_airport, f1r.coach,
f1r.firstclass, f1.id, next_leg.depart_dt, next_leg.depart_city, next_leg.depart_state, next_leg.depart_airport,
next_leg.arrive_dt, next_leg.arrive_city, next_leg.arrive_state, next_leg.arrive_airport, next_leg.coach,
next_leg.firstclass, next_leg.id
FROM flight AS f1 JOIN airport AS f1aa ON f1.arrive_airport_id=f1aa.id
JOIN airport AS f1da ON f1.depart_airport_id=f1da.id
JOIN rate AS f1r ON f1r.id=f1.rate_id
JOIN(
    SELECT flight_id, count(flight_id) AS num_seats
    FROM seat AS s2 JOIN flight AS f2 ON s2.flight_id=f2.id
    JOIN airport AS aa2 ON f2.arrive_airport_id=aa2.id
    JOIN airport AS da2 ON f2.depart_airport_id=da2.id
    WHERE da2.name=%s
    AND  aa2.name!=%s
    AND s2.available='1'
    AND s2.class=%s
    GROUP BY flight_id) AS ns
ON f1.id=ns.flight_id
JOIN (
  SELECT f.id, f.depart_dt, da.city AS depart_city, da.state AS depart_state, da.name AS depart_airport,
  f.arrive_dt, aa.city AS arrive_city, aa.state AS arrive_state, aa.name AS arrive_airport, r.coach, r.firstclass
  FROM flight AS f JOIN airport AS aa ON f.arrive_airport_id=aa.id
  JOIN airport AS da ON f.depart_airport_id=da.id
  JOIN rate AS r ON r.id=f.rate_id
  JOIN(
    SELECT flight_id, count(flight_id) AS num_seats
    FROM seat AS s2 JOIN flight AS f2 ON s2.flight_id=f2.id
    JOIN airport AS aa2 ON f2.arrive_airport_id=aa2.id
    JOIN airport AS da2 ON f2.depart_airport_id=da2.id
    WHERE aa2.name=%s
    AND da2.name!=%s
    AND s2.available='1'
    AND s2.class=%s
    GROUP BY flight_id) AS ns
  ON f.id=ns.flight_id
  WHERE ns.num_seats >= %s) AS next_leg
ON f1aa.name=next_leg.depart_airport
WHERE ns.num_seats >= %s
AND f1aa.name=next_leg.depart_airport
AND next_leg.depart_dt > f1.arrive_dt
""",(departAirport,arriveAirport, rate, arriveAirport, departAirport, rate, numPass, numPass))

        self.appendFlightData(self.cursor, rate, 2)
        #print("returning db.self.flightOpt=",self.flightOpt)
        return self.flightOpt
    ###########################END flightSelectTableData
    
    ###########################
    def appendFlightData(self, cursor, rate, layer):
        """format data in cursor and append to self.flightOpt, to make data stucture like:
    [[[direct flight data]][[leg 1 of flight data][leg 2 of flight data]]]
    each nested flight option data array will be ordered like:
    [departLoc, departTime, departDate, arriveLoc, arriveTime, arriveDate, coachCost||firstClassCost, flightID]"""
        for i in cursor:
            #print(i)
            departDate=str(i[0].date())
            departTime=str(i[0].time())
            departLoc=i[1]+", "+i[2]
            departAirport=i[3]
            arriveDate=str(i[4].date())
            arriveTime=str(i[4].time())
            arriveLoc=i[5]+", "+i[6]
            arriveAirport=i[7]
            coachCost="{:.2f}".format(float(i[8]))
            firstClassCost="{:.2f}".format(float(i[9]))
            flightID=int(i[10])
            if layer == 2:
                departDate2=str(i[11].date())
                departTime2=str(i[11].time())
                departLoc2=i[12]+", "+i[13]
                departAirport2=i[14]
                arriveDate2=str(i[15].date())
                arriveTime2=str(i[15].time())
                arriveLoc2=i[16]+", "+i[17]
                arriveAirport2=i[18]
                coachCost2="{:.2f}".format(float(i[19]))
                firstClassCost2="{:.2f}".format(float(i[20]))
                flightID2=int(i[21])
                if rate == "C":
                    self.flightOpt.append([[departLoc, departTime, departDate, arriveLoc, arriveTime, arriveDate, coachCost, flightID],[departLoc2, departTime2, departDate2, arriveLoc2, arriveTime2, arriveDate2, coachCost2, flightID2]])
                else:
                    self.flightOpt.append([[departLoc, departTime, departDate, arriveLoc, arriveTime, arriveDate, firstClassCost, flightID],[departLoc2, departTime2, departDate2, arriveLoc2, arriveTime2, arriveDate2, coachCost2, flightID2]])
            if layer == 3:
                if rate == "C":
                    self.flightOpt.append([[departLoc, departTime, departDate, arriveLoc, arriveTime, arriveDate, coachCost, flightID]])
                else:
                    self.flightOpt.append([[departLoc, departTime, departDate, arriveLoc, arriveTime, arriveDate, firstClassCost, flightID]])
    ###########################END appendFlightData
    ##########################################################END flight search    

    ##########################################################START insert reservation stack
    ###########################
    def insertCustomer(self, first, last, addr, cty, zipCode, email=None):
        """called in lanchFlyRight,
    for i in range(passCount):
    db.insertCustomer(passInfoInput["passFirstLineEdit"+str(i)],passInfoInput["passLastLineEdit"+str(i)],
    passInfoInput["passAddressLineEdit"+str(i)],passInfoInput["passCityLineEdit"+str(i)],
    passInfoInput["passZipLineEdit"+str(i)])
Function looks for existing customer with matching info fields and records those customer ids in self.customerIds
if found and exits. Else inserts a new customer and records their ids in self.customerIds
"""
        existingCustomer=False
        self.cursor.execute("""SELECT id FROM customer
                         WHERE LOWER(fname)=LOWER(%s) AND LOWER(lname)=LOWER(%s) AND LOWER(address)=LOWER(%s) AND LOWER(city)=LOWER(%s) AND zip=%s
                         LIMIT 1""",(first, last, addr, cty, zipCode));
        for i in self.cursor:
            try:
                existingCustomer=i[0]   #if this value is there we got results of matching customer already in db
                existingCustomer=True
                self.customerIds.append(i[0])
                #print("self.customerIds!")
                [print(i) for i in self.customerIds]
            except:
                pass
        if existingCustomer:
            return True
        try:
            #print("first, last, addr, cty, zipCode==",first, last, addr, cty, zipCode)
            self.cursor=self.cnx.cursor()
            self.cursor.execute("INSERT INTO customer (fname, lname, address, city, zip) VALUES (%s, %s, %s, %s, %s)",(first, last, addr, cty, zipCode))
            self.cnx.commit()
            self.customerIds.append(self.cursor.lastrowid)
            #print("self.customerIds!")
            [print("lastrowid", i) for i in self.customerIds]
            return True
        except:
            #print("Returning false from insertCustomer")
            return False
    ###########################END insertCustomer

    ###########################  
    def insertPayment(self, amount, method, number, ccv, cardDate, cardName):
        """called in lanchFlyRight,
db.insertPayment(346.28, paymentInput["visaRadioButton"], method, paymentInput["cardNumberLineEdit"],
paymentInput["cvvLineEdit"],paymentInput["creditDateEdit"],paymentInput["creditNameLineEdit"])
Converts data and inserts into payment table"""
        try:
            self.cursor=self.cnx.cursor()
            #print("cardDate1=",cardDate)
            cardDate=cardDate+' 12:00AM'
            #print("cardDate2=",cardDate)
            cardDate=datetime.datetime.strptime(cardDate, '%m/%d/%Y %I:%M%p').strftime("%Y-%m-%dT%H:%M:%SZ")
            #print("cardDate3=",cardDate)
            #print("str(datetime.datetime())=",datetime.datetime.now().time().isoformat(), " cardDate=",cardDate)
            self.cursor.execute("""
INSERT INTO payment (amount, day, method, number, ccv, card_date, card_name)
VALUES (%s, %s, %s, %s, %s, %s, %s)
""",(amount, datetime.datetime.now().strftime("%Y:%m:%dT%H:%M:%SZ"), method, int(number.replace(" ","").replace("-","")), int(ccv.strip(" ")), cardDate, cardName))
            self.cnx.commit()
            self.paymentId=self.cursor.lastrowid
            #print("Sucess on insertPayment lastid=", self.paymentId)
            self.insertRes()
            return True
        except:
            #print("Failed in insertPayment")
            return False
    ###########################END insertPayment
        
    ###########################
    def insertRes(self):
        """called by self.insertPayment
Inserts into reservation table"""
        try:
            self.cursor=self.cnx.cursor()
            self.cursor.execute("""INSERT INTO reservation (payment_id) VALUES (%s)""",(self.paymentId))
            self.cnx.commit()
            self.reservationId=self.cursor.lastrowid
            #print("Sucess on insertRes lastid=", self.reservationId)
            return True
        except:
            #print("Failed in insertRes")
            return False
    ###########################END insertRes

    ###########################    
    def updateSeat(self, flightId):
        """called in lanchFlyRight,
for i in range(passCount):
    for flight in flightSelectionInput:
        db.updateSeat(flight)

Function updates deat setting avialable=0 where booked
"""
        #print("Entering updateseat with flight id=",flightId)
        try:
            self.cursor=self.cnx.cursor()
            print("flightId=",flightId)
            self.cursor.execute("SELECT id FROM seat WHERE flight_id=%s AND seat.available='1' LIMIT 1", (flightId))
            for i in self.cursor.fetchone():
                seatId=i
            print("seatId=",seatId)
            self.seatIds.append(seatId)
            try:
                self.cursor.execute("UPDATE seat SET available=0 WHERE id=%s", (seatId))
                self.cnx.commit()
                return True
            except:
                print("""Failure on UPDATE seat""")
                return False
        except:
            #print("""Failure on SELECT id FROM seat""")
            return False
    ###########################END updateSeat
        
    ###########################
    def insertPassenger(self,i, hasMeal, numBags, hasAssist, isComment, rateClass):
        """TODO:CHANGE class to char(1) to hold "F" or "C" and fix db & this function
called in lanchFlyRight,
for i in range(self.passCount):
    try:
        rateClass=flightInfoInput["firstRadioButton"]
        rateClass=1
    except:
        rateClass=0
    db.insertPassenger(0,1,0,None,rateClass)
Function is called once a passenger. It iterates once in count of seats / count of passengers=j
so it inserts each seat for each passenger"""
        print("int(self.seatIds/len(self.customerIds))=",int(len(self.seatIds)/len(self.customerIds)))
        flightsPerPass=int(len(self.seatIds)/len(self.customerIds))
        for j in range(flightsPerPass):
            try:
                self.cursor=self.cnx.cursor()
                if(isComment):
                    self.cursor.execute("""INSERT INTO passenger (customer_id, reservation_id, seat_id, meal, bags, assist, comment, class)
    VALUES (%s,%s,%s, %s, %s, %s, %s, %s)""", (self.customerIds[i], self.reservationId, self.seatIds[(i*flightsPerPass)+j], hasMeal, numBags, hasAssist, isComment, rateClass))
                else:
                    self.cursor.execute("""INSERT INTO passenger (customer_id, reservation_id, seat_id, meal, bags, assist, class)
    VALUES (%s,%s,%s,%s,%s,%s,%s)""", (self.customerIds[i], self.reservationId, self.seatIds[(i*flightsPerPass)+j], hasMeal, numBags, hasAssist, rateClass))
                self.cursor.execute("SELECT * FROM passenger")
                print("Inserted passenger RESULT:")
                for k in self.cursor.fetchall():
                    print(k)
                self.cnx.commit()
            except:
                print("Failure on insertPassenger at i=",i)
                print("self.customerIds[i], self.reservationId, self.seatIds[(i*flightsPerPass)+j], hasMeal, numBags, hasAssist, rateClass===",self.customerIds[i], self.reservationId, self.seatIds[(i*flightsPerPass)+j], hasMeal, numBags, hasAssist, rateClass)
                return False
        return self.reservationId
    ###########################END insertPassenger
    ##########################################################START insert reservation stack
###########################END connectDB
