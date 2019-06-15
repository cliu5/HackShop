from flask import Flask, request, render_template, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
app = Flask(__name__, template_folder='templates', static_url_path='')

UPLOAD_FOLDER = '/users/claireliu/apple-pie-illuminate/static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app=Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

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

    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route("/test")      
def test():
    import io
    import os
    from google.cloud import vision
    from google.cloud.vision import types
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="StuyHacks-6a466864a1d5.json"
    
    client=vision.ImageAnnotatorClient()
    file_name=os.path.join(
        os.path.dirname(__file__),        
        'test.jpg')
    with io.open(file_name,'rb') as image_file:
        content=image_file.read()

    image=types.Image(content=content)
    response=client.label_detection(image=image)
    print(response)
    labels=response.label_annotations

    print('Labels:')
    for label in labels:
        print(label.description)

    return render_template('index.html')

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()
