from flask import Flask, render_template, request, Response
from PIL import Image
import mysql.connector
import json
from ultralytics import YOLO
app = Flask(__name__)

# Konfigurasi MySQL database
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'db_kontak'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/detect", methods=["POST"])
def detect():
    """
        Handler of /detect POST endpoint
        Receives uploaded file with a name "image_file", 
        passes it through YOLOv8 object detection 
        network and returns an array of bounding boxes.
        :return: a JSON array of objects bounding 
        boxes in format 
        [[x1,y1,x2,y2,object_type,probability],..]
    """
    buf = request.files["image_file"]
    boxes = detect_objects_on_image(Image.open(buf.stream))
    return Response(
      json.dumps(boxes),  
      mimetype='application/json'
    )


def detect_objects_on_image(buf):
    """
    Function receives an image,
    passes it through YOLOv8 neural network
    and returns an array of detected objects
    and their bounding boxes
    :param buf: Input image file stream
    :return: Array of bounding boxes in format 
    [[x1,y1,x2,y2,object_type,probability],..]
    """
    model = YOLO("Model/Akurasi98.pt")
    results = model.predict(buf)
    result = results[0]
    output = []
    for box in result.boxes:
        x1, y1, x2, y2 = [
          round(x) for x in box.xyxy[0].tolist()
        ]
        class_id = box.cls[0].item()
        prob = round(box.conf[0].item(), 2)
        output.append([
          x1, y1, x2, y2, result.names[class_id], prob
        ])
    return output

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        

        # Simpan data ke database MySQL
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO contacts (name, email,phone,message) VALUES (%s, %s,%s,%s)', (name, email,phone,message))
        conn.commit()
        conn.close()
        return render_template('index.html')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
