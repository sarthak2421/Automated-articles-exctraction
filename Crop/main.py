from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import process
from Crop.models import Userdb
from forms import LoginForm


app = Flask(__name__)

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

# Set the upload folder for Flask app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    if '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1]

    extension = extension.lower()

    if extension in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


@app.route('/', methods=['GET','POST'])
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Userdb.query.filter_by(uname=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            print(attempted_user)
            login_user(attempted_user)
            flash(f"Login Successfully as {attempted_user.uname}", category='success')

    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    return render_template('registration.html')




@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    files = request.files.getlist('file')

    results = []

    for file in files:
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Call the processing function from another Python file
            result = process_file(filepath)
            results.append(result)

    return jsonify({'results': results})


def process_file(filepath):
    process.main(filepath.split("\n"))
    # process.main(['.\\images\\Mumbai-Samachar'])
    # process.extraction()


if __name__ == '__main__':
    app.run(debug=True, port=9000)
