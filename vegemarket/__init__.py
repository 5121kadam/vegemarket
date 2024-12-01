from flask import Flask, render_template
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
    
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.debug = True
    
    app.secret_key = 'vegemarketkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vegimarket.sqlite'

    db.init_app(app)    
    Bootstrap4(app)

    from . import view
    app.register_blueprint(view.bp)
    
    @app.errorhandler(404) 
    def not_found(e): 
      return render_template("error.html", error=e)

    @app.errorhandler(500)
    def internal_error(e):
      return render_template("error.html", error=e)
       
    return app

