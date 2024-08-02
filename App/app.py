# app.py
import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Load the trained model
model = load_model('/Users/danielboudagian/Celeb_Lookalike_Website/actor_classification_model6.h5')

# Define the mapping from class indices to actor names
names = [
    "Amy_Adams", "Anna_Kendrick", "Anne_Hathaway", "Blake_Lively", "Brie_Larson",
    "Felicity_Jones", "Gal_Gadot", "Julia_Roberts", "Kate_Winslet", "Michael_B._Jordan",
    "Nicole_Kidman", "Penelope_Cruz", "Priyanka_Chopra", "Reese_Witherspoon", "Salma_Hayek",
    "Saoirse_Ronan", "Scarlett_Johansson", "Sofia_Vergara", "Taraji_P._Henson", "Zendaya",
    "ben_affleck", "bill_murray", "bradley_cooper", "chris_evans", "chris_pratt",
    "clint_eastwood", "colin_firth", "daniel_day-lewis", "edward_norton", "elisabeth_moss",
    "emily_mortimer", "ethan_hawke", "forest_whitaker", "gary_oldman", "harrison_ford",
    "helen_mirren", "hugh_grant", "hugh_jackman", "hugh_laurie", "ian_mckellen",
    "isla_fisher", "j.k.simmons", "jack_nicholson", "jared_leto", "javier_bardem",
    "jeff_bridges", "jeff_goldblum"
]

# Define preprocessing function
def preprocess_image(image_path):
    img_height, img_width = 224, 224  # Use the same dimensions used during training
    img = load_img(image_path, target_size=(img_height, img_width))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 255.0  # Rescale image
    return img_array

# Function to predict actor name
def predict_actor(file_path):
    img_array = preprocess_image(file_path)
    prediction = model.predict(img_array)
    predicted_class_index = np.argmax(prediction)
    actor_name = names[predicted_class_index]
    return actor_name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Make prediction
        actor_name = predict_actor(file_path)
        
        # Return the result page
        return render_template('result.html', actor_name=actor_name, uploaded_image_url=url_for('static', filename='uploads/' + filename))

if __name__ == '__main__':
    app.run(debug=True)
