from flask import Flask


def create_app():
    app = Flask(__name__)


    with app.app_context():
        from .index.home_page import index_bp

        app.register_blueprint(index_bp)
        
    return app
