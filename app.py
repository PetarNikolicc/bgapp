from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os
from werkzeug.utils import secure_filename
from utils.background_removal import remove_background
from PIL import UnidentifiedImageError

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Uppdaterad lista över tillåtna filtyper, inklusive .webp
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Konfigurationer
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['RESULT_FOLDER'] = 'processed/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max filstorlek 16 MB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Försök att bearbeta bilden, fånga eventuella fel
        output_filepath = os.path.join(app.config['RESULT_FOLDER'], filename)
        try:
            remove_background(filepath, output_filepath)
        except UnidentifiedImageError:
            flash('The uploaded file is not a valid image.')
            return redirect(url_for('index'))

        return redirect(url_for('show_result', filename=filename))
    else:
        flash('File type not allowed. Please upload a valid image.')
        return redirect(url_for('index'))

@app.route('/result/<filename>')
def show_result(filename):
    return render_template('result.html', filename=filename)

@app.route('/processed/<filename>')
def result_file(filename):
    return send_from_directory(app.config['RESULT_FOLDER'], filename)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['RESULT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)