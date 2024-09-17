import cv2
from rembg import remove

def remove_background(input_path, output_path):
    with open(input_path, 'rb') as input_file:
        input_data = input_file.read()
    
    result = remove(input_data)
    
    with open(output_path, 'wb') as output_file:
        output_file.write(result)