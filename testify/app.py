# from flask import Flask
# from flask_login import LoginManager
# from dash import Dash, html
# import dash_bootstrap_components as dbc
# from config import Config
# from extensions import db

# login_manager = LoginManager()

# def create_app():
#     app = Flask(__name__, template_folder='templates', static_folder='static')
#     app.config.from_object(Config)

#     # Initialize extensions
#     db.init_app(app)
#     login_manager.init_app(app)
#     login_manager.login_view = 'auth.login'

#     # Initialize Dash app
#     dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/', external_stylesheets=[dbc.themes.BOOTSTRAP])

#     with app.app_context():
#         # Register blueprints
#         from routes import auth, upload, api_fetch
#         app.register_blueprint(auth.bp)
#         app.register_blueprint(upload.bp)
#         app.register_blueprint(api_fetch.bp)

#         # Import and set up Dash components
#         from dashboard import layout, callbacks
#         dash_app.layout = layout.get_layout()
#         callbacks.register_callbacks(dash_app)

#         # Create database tables
#         db.create_all()

#         # Define user_loader
#         @login_manager.user_loader
#         def load_user(user_id):
#             from models.user import User
#             return User.query.get(int(user_id))

#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)



from flask import Flask
from flask_login import LoginManager
from dash import Dash
import dash_bootstrap_components as dbc
from config import Config
from extensions import db

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # --- FINALIZED SCRIPTS & STYLESHEETS ---
    # Add jspdf and html2canvas for PDF export functionality
    external_scripts = [
        "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"
    ]
    external_stylesheets = [
        dbc.themes.BOOTSTRAP,
        '/static/assets/new_dashboard_styles.css',
        'https://use.fontawesome.com/releases/v5.8.1/css/all.css'
    ]

    # Initialize Dash app with the new scripts
    dash_app = Dash(
        __name__, 
        server=app, 
        url_base_pathname='/dashboard/', 
        external_stylesheets=external_stylesheets,
        external_scripts=external_scripts, # Add scripts here
        suppress_callback_exceptions=True
    )
    
    with app.app_context():
        # Import models
        from models.user import User
        from models.test_report import TestReport
        from models.test_data import TestData
        db.create_all()

        # Register Blueprints
        from routes import auth, upload, api_fetch, dashboard as dashboard_bp
        app.register_blueprint(auth.bp)
        app.register_blueprint(upload.bp)
        app.register_blueprint(api_fetch.bp)
        app.register_blueprint(dashboard_bp.bp)

        # Setup Dash layout and callbacks
        from dashboard import layout, callbacks
        dash_app.layout = layout.get_layout()
        callbacks.register_callbacks(dash_app)

        @login_manager.user_loader
        def load_user(user_id):
            return db.session.get(User, int(user_id))
            
        # --- SECURITY FIX for "BACK BUTTON" PROBLEM ---
        @app.after_request
        def add_header(response):
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)