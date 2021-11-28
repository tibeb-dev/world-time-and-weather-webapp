from datetime import timedelta
import requests
import hashlib
import re

from flask import Flask, render_template, request, session, redirect

import psycopg2
import psycopg2.extras
import psycopg2.errors


app = Flask(__name__,static_url_path="/static")
app.permanent_session_lifetime = timedelta(minutes=50)

app.config["SECRET_KEY"] = "super secret key"

db_config = {

    "user": "kid",
    "password": "kid",
    "host": "localhost",
    "port": "5432",
    "database": "kidus"
}

# create necessary tables by default
try:
    connection = psycopg2.connect(**db_config)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS airlines(

            id SERIAL PRIMARY KEY ,
            
            name VARCHAR NOT NULL UNIQUE,
            
            password VARCHAR NOT NULL,
            
            day DATE NOT NULL);
        """)
    connection.commit()
except (Exception, psycopg2.Error) as error:
    print("Error connecting to PostgreSQL database", error)
    connection = None
finally:
    if connection != None:
        cursor.close()
        connection.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/registorpage")
def registor_page():
    return render_template("registor.html")


@app.route("/loginpage")
def login_page():
    return render_template("login.html")


@app.route("/registor", methods=['POST'])
def registor():

    name = request.form["name"]
    password = request.form["password"]
    day = request.form["day"]

    if password == "":
        return render_template("registered.html",password = password)

    # string must be encoded in utf-8 before hashing
    encoded_password = str(password).encode('utf-8')
    hashed_password = hashlib.sha256(encoded_password).hexdigest()

    conn = psycopg2.connect(**db_config)

    cursor = conn.cursor()

    select_query = "SELECT * FROM airlines WHERE name = %s and password = %s"

    cursor.execute(select_query, (name, hashed_password))

    record = cursor.fetchone()
    if record is not None:
        record_none = None
        return render_template("registered.html", record=record, record_none=record_none)

    if name == "" or day == "":
        return render_template("registered.html", name=name, day=day)

    nameRegex = re.match("^[a-zA-Z][a-zA-Z0-9]{1,50}$", name)
    if nameRegex == None:
        return render_template("registered.html", nameRegex=nameRegex)

    dateRegex = re.match("^2021-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[0])$", day)
    if dateRegex == None:
        return render_template("registered.html", dateRegex=dateRegex)

    insert_query = "INSERT INTO airlines(name,password,day) VALUES(%s,%s,%s)"
    cursor.execute(insert_query, (name, hashed_password, day))

    conn.commit()

    return render_template("registered.html",name=name)

    
       

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        
        
        conn = psycopg2.connect(**db_config)

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        form_name = request.form["name"]
        form_password = request.form["password"]

        if form_name == None or form_name =="" or form_password == None or form_password == "" :
            message_error = "fill the form properly"
            return render_template("reminder.html",message_error = message_error)
        
        

       

        # insert_query="INSERT INTO session(name,token) VALUE(session,session_token)
        # # string must be encoded in utf-8 before hashing
        encodedPassword = str(form_password).encode('utf-8')
        hashedPassword = hashlib.sha256(encodedPassword).hexdigest()

        select_query = "SELECT * FROM airlines WHERE name = %s and password = %s"
        cursor.execute(select_query, (form_name, hashedPassword))

        record = cursor.fetchone()

        if record is not None:
            
            session['name'] = request.form['name']
            return render_template("reminder.html", name=record["name"])

    if request.method == 'GET':
        if "name" in session:
            return redirect("/reminder")
        return render_template("login.html")


@app.route("/reminder")
def reminder():
    if "name" in session:
        name = session["name"]
        return render_template("reminder.html", name=name)

    return redirect("/login")


@app.route("/registered")
def registered():
    return render_template("registered.html")


@app.route("/time")
def time():
    if "name" in session:
        return render_template("time.html", name=session["name"])
    else:
        return redirect("/login")


@app.route("/weather")
def weather():
    if "name" in session:
        return render_template("weather.html")
    else:
        return redirect("/login")


@app.route("/timeapi")
def timeapi():
    if "name" in session:
        
        try:

            form_continent_request = request.args.get("continent")
            
            form_cities_request = request.args.get("city")

            print(form_continent_request,"continent")
            print(form_cities_request,"city")
            print("" == form_cities_request or form_cities_request == None)

            if "" == form_cities_request or form_cities_request == None:
                URL = f"http://worldtimeapi.org/api/timezone/{form_continent_request}"
            else:
                URL = f"http://worldtimeapi.org/api/timezone/{form_continent_request}/{form_cities_request}"

            response = requests.get(url=URL)
            response = response.json()
            print(response)

            
            if form_continent_request != "" and form_continent_request != None:
                for r in response:
                    form_continent_request = form_continent_request.capitalize()
                    if f"{form_continent_request}" in r:
                        form_none = None
                        return render_template("res_api.html", response=response, form_continent_request=form_continent_request,
                                            form_none=form_none)
            if form_continent_request =="" or form_continent_request == None:
                error_message = "fill the continent"
                form_none = None
                return render_template("res_api.html",error_message = error_message,form_none = form_none )
            if "error" in response:
                form_error = None
                error = response["error"]
                return render_template("res_api.html", error=error, form_error=form_error)
            timezone = response['timezone']
            datetime = response['datetime']
            utc_offset = response['utc_datetime']
            day_of_the_week = response['day_of_week']

            return render_template("res_api.html",
                                   continent=form_continent_request, cities=form_cities_request,
                                   timezone=timezone, datetime=datetime, GMT=utc_offset, day_of_week=day_of_the_week
                                   )
        except requests.exceptions.ConnectionError:
            error_none = None
            error_message = "connection error check your wifi"
            return render_template("res_api.html", error_message=error_message, error_none=error_none)

    else:
        return redirect("/login")


@app.route("/weatherapi")
def weatherapi():
    if "name" in session:
        try:
            form_city_name = request.args.get("city")
            
            URL = f"http://api.openweathermap.org/data/2.5/weather?q={form_city_name}&appid=03bafb90e71dae738fce744e860900b3"
            response = requests.get(url=URL)
            response = response.json()
            

            if "message" in response:
                form_error = None
                error = response["message"]
                return render_template("res_weather_api.html", error=error, form_error=form_error)

            country_code = response["sys"]["country"]
            longtitude = response["coord"]["lon"]
            latitude = response["coord"]["lat"]
            cloud = response["weather"][0]["description"]

            temp_max = response["main"]["temp_max"]
            temp_max = tempreture_converture(temp_max)
            temp_min = response["main"]["temp_min"]
            temp_min = tempreture_converture(temp_min)
            temprature_average = response["main"]["temp"]
            temprature_average = tempreture_converture(temprature_average)

            pressure = response["main"]["pressure"]
            pressure = str(pressure)+" kpa"

            humidity = response["main"]["humidity"]
            wind_speed = response["wind"]["speed"]

            return render_template("res_weather_api.html",
                                   city_name=form_city_name, country_code=country_code, longtitude=longtitude, latitude=latitude,
                                   temp_max=temp_max, temp_min=temp_min, temprature_average=temprature_average, pressure=pressure,
                                   humidity=humidity, wind_speed=wind_speed, cloud=cloud
                                   )
        except requests.exceptions.ConnectionError:
            error_none = None
            error_message = "connection error check your wifi"
            return render_template("res_weather_api.html", error_message=error_message, error_none=error_none)

    else:
        return redirect("/login")




@app.route("/logout")
def logout():
    session.pop("name")
    return redirect("/")


@app.errorhandler(404)
def invalid_route(e):
    return "invalid route"


def tempreture_converture(kelvin):
    celsius = kelvin - 273.15
    celsius = round(celsius, 2)
    celsius = f"{celsius} degress celsius"
    return celsius


if __name__ == "__main__":
    app.run(debug=True)
