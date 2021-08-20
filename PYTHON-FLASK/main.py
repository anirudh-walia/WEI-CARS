from flask import Flask, render_template, request, redirect, session  # importing all the necessary libraries
import mysql.connector
import os
import hashlib
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)

conn = mysql.connector.connect(host="remotemysql.com", user="WPMK5cE25i", password="uLWkGKDOvW",
                               database="WPMK5cE25i")  # database connection
cursor = conn.cursor()  # cursors for the database

cursor_2 = conn.cursor()

cursor_3 = conn.cursor()


@app.route('/')  # loads the landing page
def index():
    return render_template('index.html')


@app.route('/signup')  # basic signup route
def signup():
    return render_template('signup.html')


@app.route('/signin')  # basic signin route
def login():
    return render_template('signin.html')


@app.route('/saveuserdata', methods=['POST'])  # saves the user data to the database
def saveuserdata():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('pass')
    re_password = request.form.get('repeat-pass')

    if password == re_password:
        cursor.execute(
            """INSERT INTO `User_data` (`user_id`,`fullname`,`email`,`username`,`password`) VALUES (null,'{}','{}','{}',
            '{}')""".format(
                fullname, email, username, password))
        conn.commit()
        username_hash = username
        hash_object = hashlib.sha256(str(username_hash).encode('utf-8'))
        username_sha = hash_object.hexdigest()
        print('Hash', username_sha)
        return redirect('/signinsucc')
    else:
        return redirect('/signupfail')


@app.route('/signupfail')  # redirect to this route when a problem with password authentication
def signupfail():
    msg_2 = "Passwords don't match"
    return render_template('signup.html', msg_2=msg_2)


@app.route('/signinsucc')  # redirect to this route after a succsessful new signup
def loginsucc():
    msg = 'user registered successfully'
    return render_template('signin.html', msg=msg)


@app.route('/signinvalidation', methods=['POST'])  # validates the user by checking credentials from the database
def signinvalidation():
    username = request.form.get('username')
    password = request.form.get('pass')

    cursor.execute(
        """SELECT * FROM `User_data` WHERE `username` LIKE '{}' AND `password` LIKE '{}'""".format(username, password))
    users = cursor.fetchall()

    if len(users) > 0:
        return redirect('/home')
    else:
        return redirect('/signin')


@app.route('/home')  # this renders the home page
def home():
    return render_template('home.html')


@app.route('/sharecar')  # opens the share car page
def share_car():
    return render_template('sharecar.html')


@app.route('/selectcar')  # opens the select car page
def select_car():
    return render_template('selectcar.html')


@app.route('/carreg')  # opens the share car registration window
def register_car():
    return render_template('carreg.html')


@app.route('/carregistration', methods=['POST'])  # used to save the car data on the database.
def save_car():
    username = request.form.get('username')
    carname = request.form.get('carname')
    carno = request.form.get('carno')
    yearofpur = request.form.get('yearofpur')
    yearofmanu = request.form.get('yearofmanu')
    kmsdriven = request.form.get('kmsdriven')
    curmil = request.form.get('curmil')
    fueltype = request.form.get('fueltype')
    regno = request.form.get('regno')

    cursor.execute(
        """INSERT INTO `car_details` (`username`,`carname`,`carno`,`yearofpur`,`yearofmanu`,`fuel_type`,`kmsdriven`,
        `curmil`,`regno`) VALUES ('{}','{}','{}', '{}','{}','{}','{}','{}','{}')""".format(username, carname, carno,
                                                                                           yearofpur, yearofmanu,
                                                                                           fueltype,
                                                                                           kmsdriven, curmil,
                                                                                           regno))
    conn.commit()
    return redirect('/mycars')


@app.route('/mycars')  # opens the my cars window
def my_collection():
    cursor.execute(
        """SELECT * FROM `car_details` """)
    data = cursor.fetchall()

    return render_template('mycars.html', data=data)


@app.route('/inputcontract')  # opens the input contract window
def input_contract():
    cursor.execute(
        """SELECT * FROM `car_details` """)
    data = cursor.fetchall()

    return render_template('tempcontract.html', data=data)


@app.route('/savecontract', methods=['POST'])  # registers the contract
def save_contract():
    carno = request.form.get('carno')
    basecharge = request.form.get('basecharge')
    chargekm = request.form.get('chargeperkm')
    maxspeed = request.form.get('maxspeed')
    penpspeed = request.form.get('penperms')
    pickupplace = request.form.get('pickup')
    special = request.form.get('special')

    cursor.execute(
        """SELECT * FROM `car_details` WHERE `carno` LIKE '{}'""".format(carno))
    data = cursor.fetchall()

    if len(data) > 0:
        cursor.execute(
            """INSERT INTO `contract_details` (`car_no`,`basecharge`,`chargekm`,`maxspeed`,`weipersv`,`pickupplace`,
            `special`) VALUES ('{}','{}','{}', '{}','{}','{}','{}')""".format(carno, basecharge, chargekm,
                                                                              maxspeed, penpspeed, pickupplace,
                                                                              special))
        conn.commit()
        return redirect('/home')
    else:
        return redirect('/input_cr_fail')


@app.route('/input_cr_fail')  # if the user fails to confirm his car's details
def fail_contract():
    msg = "car number is not valid"
    return render_template('tempcontract.html', msg=msg)


@app.route('/rentcar')  # renders the rentcar page
def rent_car():
    cursor.execute(
        """SELECT * FROM `car_details` """)
    data = cursor.fetchall()
    return render_template('rentcar.html', data=data)


@app.route('/view_contract')  # renders the contract viewer
def viewcontract():
    cursor.execute(
        """SELECT * FROM `contract_details` """)
    data = cursor.fetchall()
    nparray = np.array(data)
    finaldata = nparray.flatten()
    newdata = str(finaldata)
    encoded = newdata.encode()
    result = hashlib.sha256(encoded)
    blockhashhh = result.hexdigest()
    return render_template('viewcontract.html', data=data, blockhashhh=blockhashhh)


@app.route('/trxsave', methods=['POST'])  # saves details of transaction on database
def save_trx():
    dateandtime = request.form.get('pickupdatentime')
    noofhours = request.form.get('hourss')
    metaradd = request.form.get('address')
    cursor.execute(
        """INSERT INTO `trx_data` (`dateandtime`,`noofhours`,`metaddress`) VALUES ('{}','{}','{}')""".format(
            dateandtime,
            noofhours, metaradd))
    conn.commit()
    return redirect('/home')


@app.route('/account')  # shows all the transactions
def my_account():
    cursor.execute(
        """SELECT * FROM `trx_data` """)
    data = cursor.fetchall()
    cursor_2.execute(
        """SELECT `carname` FROM `car_details` """)
    carname = cursor_2.fetchall()
    cursor_3.execute(
        """SELECT * FROM `contract_details` """)
    info = cursor_3.fetchall()
    nparray = np.array(info)
    finaldata = nparray.flatten()
    newdata = str(finaldata)
    encoded = newdata.encode()
    result = hashlib.sha256(encoded)
    blockhashhh = result.hexdigest()

    return render_template('bookings.html', data=data, carname=carname, blockhashhh=blockhashhh)


@app.route('/finalpage')  # this deals with the final payment page
def final_page():
    cursor.execute(
        """SELECT `speed` FROM `obd_values` """)
    data = cursor.fetchall()
    nparray = np.array(data)
    finaldata = nparray.flatten()
    cursor_2.execute(
        """SELECT * FROM `contract_details` """)
    cardata = cursor_2.fetchall()
    npcarray = np.array(cardata)
    finalcdata = npcarray.flatten()  # get individual values of this array
    print(finalcdata)
    basecharge = int(float(finalcdata[1]))
    chargeperkm = int(float(finalcdata[2]))
    maxspeed = int(float(finalcdata[3]))
    penpspeed = int(float(finalcdata[4]))

    pen = 0
    for i in finaldata:
        if i > maxspeed:
            pen = pen + 1
    penalty = penpspeed * pen
    meanspeed = np.mean(finaldata)
    totaltime = (len(finaldata) * 4) / 3600
    totalmeandistance = meanspeed * totaltime
    pricekm = chargeperkm * totalmeandistance
    totalprice = basecharge + pricekm
    totalpriceafterpen = basecharge + pricekm + penalty
    finaltotal = totalpriceafterpen / 100000
    return render_template("finalpage.html", totalprice=totalprice, totalpriceafterpen=totalpriceafterpen,
                           penalty=penalty, finaltotal=finaltotal)


@app.route('/getdata', methods=['GET'])  # this gets the rpm and speed data from the car using esp32
def get_cardata():
    speed = request.args.get('speedd')
    rpm = request.args.get('rpm')
    print(rpm)
    print(speed)
    cursor.execute(
        """INSERT INTO `obd_values` (`speed`) VALUES ('{}')""".format(speed))
    conn.commit()
    return speed


# main driver function
if __name__ == '__main__':
    app.run(debug=True, host='192.168.29.244')
# if __name__ == '__main__':
#
#     app.run(debug=True, host='192.168.137.71')
