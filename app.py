from flask import Flask, request, json
from tensorflow.keras.preprocessing import image
from tensorflow.keras import backend as K
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
from flask_cors import CORS
import numpy as np
import os 

app = Flask(__name__)
CORS(app)
basepath = os.path.dirname(__name__)

model = load_model('Malaria_predictor.h5')


@app.route('/api/sema', methods=['POST'])
def index():
    if request.method == 'POST':

        f = request.files['file']
        uploads_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(uploads_path)

        img = image.load_img(uploads_path, target_size=(150, 150))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        pred_image = np.vstack([x])

        result = { }

        try:
            pred = model.predict(pred_image)

            for i in pred:
                if (i[0] > i[1]):
                    result['infected'] = 1
                    os.remove(uploads_path)
                else:
                    result['uninfected'] = 1
                    os.remove(uploads_path)
        except Exception as e:
            result = "Sorry, an error occurred"
            
        return json.dumps(result)
    return None


if __name__ == "__main__":
    app.run()     