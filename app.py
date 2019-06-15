from flask import Flask, request, render_template, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import urllib.request
import json
import ssl
import io
import os
from google.cloud import vision
from google.cloud.vision import types
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="HackShop-bcb242b719d9.json"

app = Flask(__name__, template_folder='templates', static_url_path='')

UPLOAD_FOLDER = '/users/claireliu/apple-pie-illuminate/static'
UPLOAD_FOLDER2= '/users/claireliu/apple-pie-illuminate'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app=Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['UPLOAD_FOLDER2']=UPLOAD_FOLDER2
client=vision.ImageAnnotatorClient()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET','POST'])      
def home():

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER2'],filename))
            print(filename)
            
            file_name=os.path.join(os.path.dirname(__file__),filename)
            
            with io.open(file_name,'rb') as image_file:
                content=image_file.read()

            image=types.Image(content=content)
            response=client.label_detection(image=image)
            print(response)
            labels=response.label_annotations

            print('Labels:')
            for label in labels:
                print(label.description)
                    #test(filename)
                    
            return render_template('index.html',imgURL=filename)
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
#@app.route("/test")      
def test(filename):
    file_name = os.path.join(
        os.path.dirname(__file__),
        'static/test.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations


    print('Labels:')
    for label in labels:
        print(label.description)
        print(label.score)

    return render_template('index.html')


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()
