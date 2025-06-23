from flask import Flask
from app.routes import main

app = Flask(__name__, template_folder='templates')  # 👈 explicitly specify the template folder
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
