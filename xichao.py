from flask import render_template
import flask
from cStringIO import StringIO
import os
import MySQLdb
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from flask import send_from_directory
from time import time
from sqlalchemy import *
import sqlalchemy.util as util
import string, sys
from sqlalchemy.databases import mysql



app = Flask(__name__)
UPLOAD_FOLDER = 'static/upload_images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




conn = MySQLdb.connect(host='localhost', user='root',passwd='root') 
conn.select_db('xichao_theme');
cursor = conn.cursor()
cursor.execute("select * from xichao_theme")
data = cursor.fetchone() 
#print cursor.description



def save_image_path_to_db(content): 
   # c = dict(content=content) 
    
    # image_path.save(c) 
    # return c['_id'] 
    # return c
    pass

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
   

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/db")
def testmysql():
    return "hello db"
    #return cursor.description


@app.route("/test/")
def test():
    #x=image_path.find()
    x=[]
    all_path=[]
    for item in x:
            all_path.append("../"+item['content'].encode('utf8'))
    all_path=str(all_path).replace("\'","").strip("\'")[1:-1]
    print all_path
    return render_template('nav.html',all_path=all_path)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.filename=str(int(time()))+'.'+file.filename.rsplit('.', 1)[1]
            
            #save image url to db
            content=UPLOAD_FOLDER+file.filename
            print save_image_path_to_db(content)

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
@app.route('/upload_images/<filename>')
def uploaded_file(filename):
    #return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
    return '<script type="text/javascript" >alert("uploaded!");</script>'






if __name__ == "__main__":
    app.run(debug=True)

