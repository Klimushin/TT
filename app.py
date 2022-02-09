from flask import Flask

from database import db
from expenses import exp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testtask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(exp, url_prefix='/')

if __name__ == "__main__":
    app.run(debug=True)
