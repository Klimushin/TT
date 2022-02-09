from database import app
from expenses import exp

app.register_blueprint(exp, url_prefix='/')

if __name__ == "__main__":
    app.run(debug=True)
