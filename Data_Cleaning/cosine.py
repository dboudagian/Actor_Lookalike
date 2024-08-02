import os
import shutil
import numpy as np
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
from sklearn.metrics.pairwise import cosine_similarity
import cv2
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model
import tensorflow as tf

import cv2
import os
from mtcnn import MTCNN

def zoom_in_on_face(image_path, output_path, min_width=224, min_height=224):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image at {image_path}")
        return False

    # Initialize the MTCNN face detector
    detector = MTCNN()

    # Convert the image to RGB as MTCNN expects RGB images
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect faces in the image
    faces = detector.detect_faces(image_rgb)

    if len(faces) == 0:
        print(f"No faces found in {image_path}")
        return False

    # Get the bounding box of the first detected face
    (x, y, w, h) = faces[0]['box']
    face_image = image[y:y+h, x:x+w]

    # Get dimensions of the face image
    face_height, face_width = face_image.shape[:2]

    # Resize the face image if it is smaller than the minimum size
    if face_width < min_width or face_height < min_height:
        aspect_ratio = face_width / face_height
        if aspect_ratio > 1:
            new_width = max(min_width, int(min_height * aspect_ratio))
            new_height = min_height
        else:
            new_width = min_width
            new_height = max(min_height, int(min_width / aspect_ratio))
        face_image = cv2.resize(face_image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Create the output directory if it does not exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save the cropped face image
    success = cv2.imwrite(output_path, face_image)
    if not success:
        print(f"Error: Unable to save cropped image at {output_path}")
        return False

    return True

def get_images_in_folder(folder_path):
    supported_formats = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(supported_formats)]
    image_files.sort()
    return image_files

def extract_features(img, model):
    img = cv2.resize(img, (224, 224))  # Resize to model's expected input size
    img = img.astype('float32')
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)  # Preprocess for ResNet50
    features = model.predict(img)
    return features.flatten()

def process_folders(input_base_folder, output_base_folder, above_threshold_folder, min_width=224, min_height=224):
    try:
        os.makedirs(output_base_folder, exist_ok=True)
        os.makedirs(above_threshold_folder, exist_ok=True)
    except OSError as e:
        print(f"Error creating directories: {e}")
        return
    
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

    # Add global average pooling
    x = base_model.output
    x = tf.keras.layers.GlobalAveragePooling2D()(x)

    # You can add more layers here if necessary
    # x = Dense(1024, activation='relu')(x)  # Example of adding a fully connected layer

    # Create the final model
    model = Model(inputs=base_model.input, outputs=x)
    
    print("hello")

    for folder_name in os.listdir(input_base_folder):
        folder_path = os.path.join(input_base_folder, folder_name)
        if os.path.isdir(folder_path):
            images = []
            image_files = get_images_in_folder(folder_path)
            
            print("hello")
            
            # Create a subfolder in the output_base_folder for this group
            group_output_folder = os.path.join(output_base_folder, folder_name)
            os.makedirs(group_output_folder, exist_ok=True)
            
            for image_file in image_files:
                image_path = os.path.join(folder_path, image_file)
                output_path = os.path.join(group_output_folder, image_file)
                if zoom_in_on_face(image_path, output_path, min_width, min_height):
                    img = cv2.imread(output_path)
                    images.append((image_file, img, output_path))

            features_dict = {}
            for image_file, img, _ in images:
                features_dict[image_file] = extract_features(img, model)

            above_55_images = []

            # First round of cosine similarity calculation with threshold 0.55
            for image_file, img, output_path in images:
                image_features = features_dict[image_file]
                similarities = []
                for other_image_file, other_features in features_dict.items():
                    if image_file != other_image_file:
                        similarity = cosine_similarity([image_features], [other_features])[0][0]
                        similarities.append(similarity)
                
                if similarities:
                    avg_similarity = np.mean(similarities)
                    print(f"Average similarity for {image_file} in {folder_name} (threshold 0.55): {avg_similarity:.4f}")
                    
                    if avg_similarity > 0.55:
                        above_55_images.append((image_file, img, output_path))

            # Second round of cosine similarity calculation with threshold 0.70
            filtered_features_dict = {image_file: features_dict[image_file] for image_file, img, _ in above_55_images}
            for image_file, img, output_path in above_55_images:
                image_features = filtered_features_dict[image_file]
                similarities = []
                for other_image_file, other_features in filtered_features_dict.items():
                    if image_file != other_image_file:
                        similarity = cosine_similarity([image_features], [other_features])[0][0]
                        similarities.append(similarity)
                
                if similarities:
                    avg_similarity = np.mean(similarities)
                    print(f"Average similarity for {image_file} in {folder_name} (threshold 0.70): {avg_similarity:.4f}")
                    
                    if avg_similarity > 0.7:
                        # Create a subfolder in the above_threshold_folder for this group
                        group_above_threshold_folder = os.path.join(above_threshold_folder, folder_name)
                        os.makedirs(group_above_threshold_folder, exist_ok=True)
                        
                        destination_path = os.path.join(group_above_threshold_folder, image_file)
                        if not os.path.exists(destination_path):
                            shutil.copy(output_path, destination_path)
                            print(f"Moved image {image_file} to {group_above_threshold_folder}")





# Example usage
input_base_folder = '/Users/danielboudagian/Downloads/Pictures'  # Specify the path to your base directory with subfolders
output_base_folder = '/Users/danielboudagian/james'  # Specify the path to the output directory for processed images
above_threshold_folder = '/Users/danielboudagian/james_pics'  # Specify the path to the output directory for images above the threshold


process_folders(input_base_folder, output_base_folder, above_threshold_folder)



# Example usage
# input_base_folder = '/Users/danielboudagian/Downloads/Imager'  # Specify the path to your base directory with subfolders
# output_base_folder = '/Users/danielboudagian/Process_Images'  # Specify the path to the output directory for processed images
# above_threshold_folder = '/Users/danielboudagian/Above'  # Specify the path to the output directory for images above the threshold

