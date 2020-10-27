from flask import Flask, request, json
from tensorflow.keras.preprocessing import image
from tensorflow.keras import backend as K
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
from classfier import classify
import os 


app = Flask(__name__)


basepath = os.path.dirname(__name__)



@app.route('/api/classify', methods=['POST'])
def index():
    if request.method == 'POST':

        f = request.files['file']
        image = Image.open(f)
        
        result = classify(image)
            
        return json.dumps(result)
    return None


if __name__ == "__main__":
    app.run()     