from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from expenses import exp

app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testtask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(exp, url_prefix='/')

if __name__ == "__main__":
    app.run(debug=True)
