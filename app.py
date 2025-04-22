from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file, Response
from login import *
import time, datetime, base64, pytz
from database import *
from markit import *
from qr import *
import asyncio
from autc import *
import os

BASE_DIR = os.path.abspath("../../")

app = Flask(__name__)

flag=True

app.secret_key = os.urandom(24)

try:
    @app.route('/start', methods=['POST'])
    def start():
        asyncio.run(autc())

    @app.route('/')
    def home():
        return render_template("index.html")

    @app.route('/about')
    def about():
        return render_template("about.html")

    @app.route('/connect')
    def connect():
        return render_template("connect.html")

    @app.route('/donate')
    def donate():
        return render_template("donate.html")

    @app.route('/signout')
    def signout():
        try:
            del session['user']
        except Exception as e:
            print("No Session found")
        return redirect("/")

    @app.route('/files',methods=['GET', 'POST'])
    def files():
        try:
            if session['user']=='admin':
                return render_template('files.html',files=get_file_list(BASE_DIR))
        except Exception as e:
            print('false login')
            return redirect('/')
        
    @app.route('/download/<path:filename>')
    def download_file(filename):
        try:
            if session['user']=='admin':
                pass
            else:
                return 'FUCK YOU!!'
        except Exception as e:
            return 'FUCK YOU!!'
        file_path = os.path.join(BASE_DIR, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return "File not found", 404

    # Function to list files and directories
    def get_file_list(directory):
        file_list = []
        for root, dirs, files in os.walk(directory):
            relative_path = os.path.relpath(root, BASE_DIR)
            if relative_path == ".":
                relative_path = "Root Directory"
            file_list.append({'type': 'folder', 'name': relative_path})
            for file in files:
                file_list.append({'type': 'file', 'name': os.path.join(relative_path, file)})
        return file_list
    
    @app.route('/admin',methods=['POST','GET'])
    def admin():
        try:
            if session['user']=='admin':
                return render_template('admin.html')
        except Exception as e:
            print('false login')
            return redirect('/')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['username']
            password = request.form['password']
            aemail = email
            try:
                email_prefix = email.split("@")[0].upper() # Extract the part before @ from the email
                email_end = email.split("@")[1]
                email = email_prefix + "@" + email_end
            except Exception as e:
                print(e)

            if aemail=='admin' and password=='admin123':
                session['user']="admin"
                return redirect('admin')

            # Validate credentials
            elif db_login(email,password):
                session['user']=email
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials. Try again.', 'danger')

        return render_template('login.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template("dashboard.html")

    @app.route('/signup',methods=['POST','GET'])
    def signup():
        if request.method == 'POST':
            email = request.form['username']
            password = request.form['password']

            # Validate credentials
            if login_and_save_data(email,password):
                session['user']=email
                flash('Registration successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials. Try again.', 'danger')
        return render_template("signup.html")


    @app.route('/scan')
    def scan():
        if flag:
            return render_template('scan.html', title="Scan QR Code")
        else:
            return 'Contact Admin Service Forbidden!!'

    @app.route('/')
    def index():
        return render_template('index.html')
    
    UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__))  # Root directory
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    @app.route("/upload", methods=["POST"])
    def upload_image():
        try:
            if session['user']:
                pass
            else:
                return
        except Exception as e:
            return
        if "image" not in request.files:
            return "No image file found", 400
        ist = pytz.timezone('Asia/Kolkata')
        t=datetime.datetime.now(ist).strftime("%Y%m%d%H%M%S")
        image = request.files["image"]
        t=f"qr_{t}.jpg"
        image_path = os.path.join(app.config["UPLOAD_FOLDER"],t)
        image.save(image_path)

        qr_id=scan_it(t)
        # sid=get_sid(session['user'],get_pass(session['user']))
        # testing=mark_attendance(sid,qr_id,get_stu(session['user']))
        # print(testing)
        # if(testing):
        l=asyncio.run(start_mark(qr_id))
        # session['qr']=qr_id
        # session['responsi']=l
        flash("Attendance marked!!")
        # else:
        #     session['qr']=qr_id
        #     session['responsi']=testing

        return "Image saved successfully", 200
    

        
except Exception as e:
    print(e)


if __name__=="__main__":
    app.run(debug=False, port=6969, host='0.0.0.0')
