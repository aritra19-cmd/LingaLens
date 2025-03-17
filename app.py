from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pytesseract
from PIL import Image
from googletrans import Translator
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app) # Enable CORS for all routes

#configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#initialize translator
translator = Translator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image',methods=['POST'])
def process_image():
    try:
        target_language = request.form.get('language', 'en')
        original_text = ""

        # Check if the request contains an image or text
        if 'image' in request.files:
            image_file = request.files['image']

            # Save the image temporarily
            img = Image.open(image_file)

            # Use pytesseract to extract text from the image
            original_text = pytesseract.image_to_string(img)

        elif 'text' in request.form:
            original_text = request.form.get('text', '')
        else:
            return jsonify({"error": "No image or text provided"}), 400
        
        # Translate the text
        if original_text.strip():
            # Detect the source language (optional)
            # detected_lang = translator.detect(original_text).lang
            
            # Translate to the target language
            translation = translator.translate(original_text, dest=target_language)
            translated_text = translation.text
            
            return jsonify({
                "original_text": original_text,
                "translated_text": translated_text,
                # "detected_language": detected_lang  # Optional
            })
        else:
            return jsonify({"error": "No text could be extracted or provided"}), 400
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Make sure you have pytesseract installed and configured correctly
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    
    # For production, use a proper WSGI server instead of the built-in Flask server
    app.run(debug=True)