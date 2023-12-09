from flask import Flask, render_template, request, flash, send_from_directory,redirect,url_for, send_file, current_app
from werkzeug.utils import secure_filename
from xml_parser import parseXML, parseJSON, parseFile
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'
app.secret_key = b'Th1$ 1$ @ very-very secret key!'
ALLOWED_EXTENSIONS = {'xml','json','txt'}

def allowed_file(filename):
    print(filename.rsplit('.',1)[1].lower())
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        if 'xmlcode' in request.form.keys():
            xmlcode = request.form.get('xmlcode')
            data = parseXML(xmlcode)
            return render_template('index.html',code=data)
        elif 'jsoncode' in request.form.keys():
            jsoncode = request.form.get('jsoncode')
            data = parseJSON(jsoncode)
            return render_template('index.html',code=data)
        elif 'file' in request.files:
            file = request.files.get('file')
            if file.filename == '':
                flash('No selected file')
                return render_template('index.html')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(f"upload/{filename}")
                download_file = parseFile(f"upload/{filename}")
                return redirect(url_for('download',filename=download_file))
            else:
                flash('File type is not supported')
                return render_template('index.html')
            
@app.route('/download/<path:filename>')
def download(filename):
    download_folder = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_file(path_or_file=os.path.join(download_folder,filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)