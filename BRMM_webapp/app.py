from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)

from flask import flash
from flask import session
import os
app.secret_key = os.urandom(16)

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn



@app.route("/")
def home(): 
    return render_template("welcome.html")

@app.route("/listcourses")
def listcourses():
    connection = getCursor()
    connection.execute("SELECT * FROM course;")
    courseList = connection.fetchall()
    return render_template("courselist.html", course_list = courseList)

@app.route("/driverrundetails")
def driverrundetails():
    connection = getCursor()
    connection.execute("SELECT * FROM driver;")
    driverList = connection.fetchall()
    return render_template("driverrundetails.html", driver_list=driverList)

@app.route("/viewdetails", methods=["GET", "POST"])
def viewdetails ():
    driver_id = request.form.get('driver_id')
    connection = getCursor()
    connection.execute("""
            SELECT d.first_name, d.surname, d.driver_id, c.model, c.drive_class 
            FROM driver d JOIN car c ON d.car = c.car_num 
            WHERE d.driver_id = %s
           """, (driver_id,))
    driver = connection.fetchone()

    connection.execute("""
             SELECT c.name, r.run_num, r.seconds, r.cones, r.wd,
               ROUND(r.seconds + IFNULL(r.cones * 5, 0) + IFNULL(r.wd * 10, 0), 2) AS total_time
             FROM run r  
             JOIN course c ON r.crs_id = c.course_id 
             WHERE r.dr_id = %s        
            """, (driver_id,))   
    viewdetails = connection.fetchall()              
    return render_template("viewdetails.html", driver=driver, viewdetails = viewdetails)



@app.route("/driverlistdetails")
def driverlistdetails():
    driver_id = request.args.get('driver_id', type=int)
    connection = getCursor()
    connection.execute("""
            SELECT d.first_name, d.surname, d.driver_id, c.model, c.drive_class 
            FROM driver d JOIN car c ON d.car = c.car_num 
            WHERE d.driver_id = %s
           """, (driver_id,))
    driver = connection.fetchone()
    connection.execute("""
             SELECT c.name, r.run_num, r.seconds, r.cones, r.wd,
               ROUND(r.seconds + IFNULL(r.cones * 5, 0) + IFNULL(r.wd * 10, 0), 2) AS total_time
             FROM run r  
             JOIN course c ON r.crs_id = c.course_id 
             WHERE r.dr_id = %s        
            """, (driver_id,))   
    driverlistdetails = connection.fetchall()              
    return render_template("driverlistdetails.html", driver=driver, driverlistdetails = driverlistdetails )

@app.route("/listdrivers", methods=["GET", "POST"])
def listdrivers():
     connection = getCursor()
     connection.execute("""
        SELECT  
            d.driver_id AS 'Driver ID',
            CONCAT(d.surname, ' ', d.first_name) AS 'Name',
            d.date_of_birth AS 'Date of Birth',
            d.age AS 'Age',
            ca.model AS 'Car Model',
            ca.drive_class AS 'Drive Class',
            CONCAT(c.surname, ' ', c.first_name) AS 'Caregiver Name'
        FROM 
            driver d
        LEFT JOIN 
            driver c ON d.caregiver = c.driver_id
        JOIN 
            car ca ON d.car = ca.car_num;
    """)
     drivers = connection.fetchall()
     return render_template("driverlist.html", drivers=drivers)

@app.route("/overall")
def overall():
    cursor = getCursor()
    query = """
    SELECT
        d.driver_id,
        CASE
            WHEN age BETWEEN 12 AND 25 THEN CONCAT(d.surname, ' ', d.first_name, ' (J)') 
            ELSE CONCAT(d.surname, ' ', d.first_name)
        END AS driver_name,
        c.model AS car_model,
        c.drive_class AS drive_class,
        COALESCE(MAX(CASE WHEN bt.crs_id = 'A' THEN ROUND(bt.best_seconds, 2) END), 'DNF') AS "Going Loopy (A)",
        COALESCE(MAX(CASE WHEN bt.crs_id = 'B' THEN ROUND(bt.best_seconds, 2) END), 'DNF') AS "Mum's Favourite (B)",
        COALESCE(MAX(CASE WHEN bt.crs_id = 'C' THEN ROUND(bt.best_seconds, 2) END), 'DNF') AS "Walnut (C)",
        COALESCE(MAX(CASE WHEN bt.crs_id = 'D' THEN ROUND(bt.best_seconds, 2) END), 'DNF') AS "Hamburger (D)",
        COALESCE(MAX(CASE WHEN bt.crs_id = 'E' THEN ROUND(bt.best_seconds, 2) END), 'DNF') AS "Shoulders Back (E)",
        COALESCE(MAX(CASE WHEN bt.crs_id = 'F' THEN ROUND(bt.best_seconds, 2) END), 'DNF') AS "Cracked Fluorescent (F)",
        CASE 
            WHEN 'DNF' IN (
                COALESCE(MAX(CASE WHEN bt.crs_id = 'A' THEN ROUND(bt.best_seconds, 2) END), 'DNF'),
                COALESCE(MAX(CASE WHEN bt.crs_id = 'B' THEN ROUND(bt.best_seconds, 2) END), 'DNF'),
                COALESCE(MAX(CASE WHEN bt.crs_id = 'C' THEN ROUND(bt.best_seconds, 2) END), 'DNF'),
                COALESCE(MAX(CASE WHEN bt.crs_id = 'D' THEN ROUND(bt.best_seconds, 2) END), 'DNF'),
                COALESCE(MAX(CASE WHEN bt.crs_id = 'E' THEN ROUND(bt.best_seconds, 2) END), 'DNF'),
                COALESCE(MAX(CASE WHEN bt.crs_id = 'F' THEN ROUND(bt.best_seconds, 2) END), 'DNF')
            ) THEN 'NQ'
            ELSE COALESCE(ROUND(SUM(bt.best_seconds), 2), 'DNF')
        END AS "Overall"
    FROM
        driver d
    JOIN
        car c ON d.car = c.car_num
    LEFT JOIN (
        SELECT
            r.dr_id,
            r.crs_id,
            MIN(r.seconds) AS best_seconds
        FROM
            run r
        GROUP BY
            r.dr_id, r.crs_id
    ) bt ON d.driver_id = bt.dr_id
    GROUP BY
        d.driver_id,
        d.surname,
        d.first_name,
        c.model,
        c.drive_class
   ORDER BY
    CASE 
        WHEN `OverAll` = 'NQ' THEN 1
        ELSE 0
    END,
    `Overall`,
    CONCAT(d.surname, ' ', d.first_name);
    """
    cursor.execute(query)
    data = cursor.fetchall()
    # Add "cup" and "prize" annotations
    formatted_data = []
    for i, row in enumerate(data):
        if i == 0:
            formatted_data.append(row + ("🏆",))
        elif 1 <= i <= 4:
            formatted_data.append(row + ("🎁",))
        else:
            formatted_data.append(row + ("",))

    cursor.close()
    connection.close()

    return render_template('overall.html', data=formatted_data)


@app.route("/graph")
def graph():
    cursor = getCursor()
    sql = """
    SELECT
    d.driver_id,
    CONCAT(d.surname, ' ', d.first_name) AS driver_name,
    CASE 
        WHEN 'DNF' IN (
            COALESCE(MAX(CASE WHEN bt.crs_id = 'A' THEN ROUND(bt.best_seconds, 2) END), 'DNF'),
            COALESCE(MAX(CASE WHEN bt.crs_id = 'B' THEN ROUND(bt.best_seconds, 2) END), 'DNF'),
            COALESCE(MAX(CASE WHEN bt.crs_id = 'C' THEN ROUND(bt.best_seconds, 2) END), 'DNF'),
            COALESCE(MAX(CASE WHEN bt.crs_id = 'D' THEN ROUND(bt.best_seconds, 2) END), 'DNF'),
            COALESCE(MAX(CASE WHEN bt.crs_id = 'E' THEN ROUND(bt.best_seconds, 2) END), 'DNF'),
            COALESCE(MAX(CASE WHEN bt.crs_id = 'F' THEN ROUND(bt.best_seconds, 2) END), 'DNF')
        ) THEN 'NQ'
        ELSE COALESCE(ROUND(SUM(bt.best_seconds), 2), 'NQ')
    END AS Overall
FROM
    driver d
JOIN
    car c ON d.car = c.car_num
LEFT JOIN (
    SELECT
        r.dr_id,
        r.crs_id,
        MIN(r.seconds) AS best_seconds
    FROM
        run r
    GROUP BY
        r.dr_id, r.crs_id
) bt ON d.driver_id = bt.dr_id
GROUP BY
    d.driver_id,
    d.surname,
    d.first_name
HAVING 
    Overall != 'NQ' AND Overall != 'DNF'
ORDER BY
    Overall
LIMIT 5;

    """
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()

    bestDriverList = [str(result[0]) + " " + result[1] for result in results]
    resultsList = [result[2] for result in results]

    return render_template("top5graph.html", name_list=bestDriverList, value_list=resultsList)

@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/base', methods=['GET'])
def base():
    return render_template('base.html')

@app.route("/junior_drivers")
def junior_drivers():

    connection = getCursor()
    connection.execute("""
    SELECT 
        d.driver_id,
        CONCAT(d.first_name, ' ', d.surname) as driver_name, 
        d.age, 
        CONCAT(cg.first_name, ' ', cg.surname) as caregiver_name
    FROM 
        driver d
    LEFT JOIN 
        driver cg ON d.caregiver = cg.driver_id
    WHERE 
        d.age BETWEEN 12 AND 25
    ORDER BY 
        d.age DESC, d.surname ASC;
    """)

    results = connection.fetchall()
    return render_template("junior_drivers.html", drivers=results)




@app.route('/search_drivers', methods=['GET', 'POST'])
def search_drivers():
    if request.method == 'POST':
        search_text = request.form.get('search_text')
        cursor = getCursor()
        cursor.execute(f"SELECT * FROM driver WHERE first_name LIKE %s OR surname LIKE %s", (f"%{search_text}%", f"%{search_text}%"))
        results = cursor.fetchall()
        return render_template("search_drivers.html", drivers=results)
    return render_template('search_drivers.html')

@app.route("/searchdriverdetails")
def searchdriverdetails():
    driver_id = request.args.get('driver_id', type=int)
    cursor = getCursor()
    cursor.execute("""
            SELECT d.first_name, d.surname, d.driver_id, c.model, c.drive_class 
            FROM driver d JOIN car c ON d.car = c.car_num 
            WHERE d.driver_id = %s
           """, (driver_id,))
    driver = cursor.fetchone()
    cursor.execute("""
             SELECT c.name, r.run_num, r.seconds, r.cones, r.wd,
               ROUND(r.seconds + IFNULL(r.cones * 5, 0) + IFNULL(r.wd * 10, 0), 2) AS total_time
             FROM run r  
             JOIN course c ON r.crs_id = c.course_id 
             WHERE r.dr_id = %s        
            """, (driver_id,))   
    searchdriverdetails = cursor.fetchall()      
         
    return render_template("searchdriverdetails.html", driver=driver, searchdriverdetails = searchdriverdetails)



def fetch_drivers(cursor):
    query = "SELECT driver_id, CONCAT(first_name, ' ', surname) AS full_name FROM driver"
    cursor.execute(query)
    return cursor.fetchall()
def fetch_courses(cursor):
    query = "SELECT course_id, CONCAT(course_id, ' - ', name) AS course_name FROM course"
    cursor.execute(query)
    return cursor.fetchall()

def fetch_runs(cursor, driver_id=None, course_id=None):
    conditions = []
    params = []
    if driver_id:
        conditions.append("d.driver_id = %s")
        params.append(driver_id)
    if course_id:
        conditions.append("c.course_id = %s")
        params.append(course_id)

    query = """
        SELECT CONCAT(d.first_name, ' ', d.surname) AS driver_name, 
               d.driver_id,
               c.course_id, 
               c.name AS course_name, 
               r.run_num, 
               r.seconds, 
               r.cones, 
               r.wd,
               ROUND(r.seconds + IFNULL(r.cones * 5, 0) + IFNULL(r.wd * 10, 0), 2) AS total_time
        FROM run r
        JOIN driver d ON r.dr_id = d.driver_id
        JOIN course c ON r.crs_id = c.course_id
    """
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, params)
    return cursor.fetchall()




@app.route('/search_runs', methods=['POST'])
def search_runs():
    cursor = getCursor()
    if not cursor:
        return "Database connection failed", 500
    
    driver_id = request.form.get('driver_id')
    course_id = request.form.get('course_id')
    
    drivers = fetch_drivers(cursor)
    courses = fetch_courses(cursor)
    runs = fetch_runs(cursor, driver_id, course_id)

    return render_template('editrun.html', drivers=drivers, courses=courses, runs=runs, driver_id=driver_id, course_id=course_id)




@app.route('/update_run', methods=['POST'])
def update_run():
    cursor = getCursor()
    if not cursor:
        return "Database connection failed", 500

    driver_id = request.form.get('driver_id')
    course_id = request.form.get('course_id')
    


    try:
        runs = fetch_runs(cursor, driver_id, course_id)
        for run in runs:
            driver_id = run[1]  # 从返回的记录中获取driver_id 
            course_id = run[2]  # 从返回的记录中获取course_id
            run_num = run[4]
            seconds = request.form.get(f'seconds_{driver_id}_{course_id}_{run_num}')
            cones = request.form.get(f'cones_{driver_id}_{course_id}_{run_num}')
            wd = request.form.get(f'wd_{driver_id}_{course_id}_{run_num}') == 'on'

            sql = """
                UPDATE run
                SET seconds = %s, cones = %s, wd = %s
                WHERE dr_id = %s AND crs_id = %s AND run_num = %s
            """
            params = (seconds, cones, wd, driver_id, course_id, run_num)
            cursor.execute(sql, params)

    except mysql.connector.Error as err:
        print("Error: {}".format(err))

    return redirect(url_for('editrun', message='Changes saved successfully!'))


@app.route('/editrun', methods=['GET', 'POST'])
def editrun():
    cursor = getCursor()
    if not cursor:
        return "Database connection failed", 500
    
    drivers = fetch_drivers(cursor)
    courses = fetch_courses(cursor)
    runs = None  # 不在初次加载时传递运行数据
    
    message = request.args.get('message')
     
    return render_template('editrun.html', drivers=drivers, courses=courses,runs=runs, message=message)




@app.route('/add_driver', methods=['GET', 'POST'])
def add_driver():
    global connection
    global dbconn

    # 获取所有可能的监护人
    getCursor()
    cursor = dbconn
    cursor.execute('SELECT driver_id, CONCAT(first_name, " ", surname) as name FROM driver WHERE age IS NULL')
    caregivers = cursor.fetchall()
    cursor.close()
    connection.close()

    age_message = None
    error_message = None
    is_junior = False
    show_caregiver_field = False
    age = None
    caregiver_id = None
    date_of_birth = None
    first_name = None
    surname = None
    car_num = None

    form_data = session.get('form_data', {})

    if request.method == 'POST':
        session['form_data'] = request.form.to_dict()
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        car_num = request.form.get('car')
        is_junior = request.form.get('is_junior') == 'on'
        date_of_birth = request.form.get('date_of_birth') if is_junior else None
        caregiver_id = request.form.get('caregiver') if is_junior else None

        if request.form.get('action') == 'check_age':
            if is_junior and date_of_birth:
                birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d')
                today = datetime.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                if age < 12 or age > 25:
                    error_message = "Invalid age for a junior driver: Participants need to be at least 12 years old to participate in the competition."
                elif age <= 16:
                    show_caregiver_field = True
                    age_message = f"The driver is {age} years old and requires a caregiver."
                else:
                    age_message = f"The driver is {age} years old and does not require a caregiver."
            elif not date_of_birth:
                error_message = "Date of birth is required to check age"
        else:
            if not first_name or not surname or not car_num:
                error_message = "All fields are required"
            else:
                if is_junior:
                    if not date_of_birth:
                        error_message = "Date of birth is required for junior drivers"
                    else:
                        if age is None:
                            birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d')
                            today = datetime.today()
                            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                        if age < 12 or age > 25:
                            error_message = "Invalid age for a junior driver"
                        elif age <= 16:
                            show_caregiver_field = True
                            if not caregiver_id:
                                error_message = "A caregiver is required for drivers 16 or younger"

                if not error_message:
                    getCursor()
                    cursor = dbconn
                    try:
                        cursor.execute('INSERT INTO driver (first_name, surname, date_of_birth, age, caregiver, car) VALUES (%s, %s, %s, %s, %s, %s)',
                                    (first_name, surname, date_of_birth, age, caregiver_id, car_num))
                        new_driver_id = cursor.lastrowid
                        cursor.execute('SELECT course_id FROM course')
                        courses = cursor.fetchall()
                        for course in courses:
                            course_id = course[0]
                            for run_num in range(1, 3):
                                cursor.execute('INSERT INTO run (dr_id, crs_id, run_num, wd) VALUES (%s, %s, %s, 0)',
                                            (new_driver_id, course_id, run_num))
                    finally:
                        cursor.close()
                        connection.close()

                    session.pop('form_data', None)
                    return redirect(url_for('add_driver_success'))

    getCursor()
    cursor = dbconn
    try:
        cursor.execute('SELECT car_num, model FROM car')
        cars = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    if 'form_data' in session:
        form_data = session.pop('form_data')
    else:
        form_data = {}

    return render_template('add_driver.html', cars=cars, form_data=form_data, is_junior=is_junior, show_caregiver_field=show_caregiver_field, caregivers=caregivers, error_message=error_message, age_message=age_message)



@app.route('/add_driver_success')
def add_driver_success():
    return render_template('add_driver_success.html')
