from flask import Blueprint, render_template, request
from .model import load_model
from .utils import prepare_input

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        rainfall = float(request.form['rainfall'])
        temperature = float(request.form['temperature'])
        pesticide = float(request.form['pesticide'])

        model, feature_names = load_model()
        input_df = prepare_input(rainfall, temperature, pesticide, feature_names)
        prediction = model.predict(input_df)[0]

    return render_template('index.html', prediction=prediction)
