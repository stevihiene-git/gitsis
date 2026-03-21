import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import logging

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    
    # Basic configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_SECRET_KEY'] = os.environ.get('WTF_CSRF_SECRET_KEY', 'csrf-secret-key')
    
    # Disable instance folder creation on Vercel
    # Use /tmp for any temporary files if needed
    if os.environ.get('VERCEL'):
        app.instance_path = '/tmp'
    else:
        # Only try to create instance folder locally
        try:
            os.makedirs(app.instance_path, exist_ok=True)
        except:
            pass
    
    # Database configuration
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        # Use SQLite with /tmp for Vercel, or local for development
        if os.environ.get('VERCEL'):
            database_url = 'sqlite:////tmp/sis.db'
            logger.warning("Using SQLite database in /tmp - data will not persist between deployments!")
        else:
            database_url = 'sqlite:///sis.db'
            logger.info("Using SQLite database for local development")
    
    # Handle Heroku/Vercel PostgreSQL URLs
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    logger.info(f"Database URI configured (hidden for security)")
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Configure login
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    return app


# Create app instance
app = create_app()

# Import models and routes after app creation to avoid circular imports
from .models import User, Student, Course, CourseRegistration, Score, Payment, SecurityAudit
from .auth import auth_bp
from .views import views_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(views_bp)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def init_db():
    """Initialize database tables"""
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")


# Initialize database
init_db()import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import logging

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    
    # Basic configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_SECRET_KEY'] = os.environ.get('WTF_CSRF_SECRET_KEY', 'csrf-secret-key')
    
    # Disable instance folder creation on Vercel
    # Use /tmp for any temporary files if needed
    if os.environ.get('VERCEL'):
        app.instance_path = '/tmp'
    else:
        # Only try to create instance folder locally
        try:
            os.makedirs(app.instance_path, exist_ok=True)
        except:
            pass
    
    # Database configuration
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        # Use SQLite with /tmp for Vercel, or local for development
        if os.environ.get('VERCEL'):
            database_url = 'sqlite:////tmp/sis.db'
            logger.warning("Using SQLite database in /tmp - data will not persist between deployments!")
        else:
            database_url = 'sqlite:///sis.db'
            logger.info("Using SQLite database for local development")
    
    # Handle Heroku/Vercel PostgreSQL URLs
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    logger.info(f"Database URI configured (hidden for security)")
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Configure login
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    return app


# Create app instance
app = create_app()

# Import models and routes after app creation to avoid circular imports
from .models import User, Student, Course, CourseRegistration, Score, Payment, SecurityAudit
from .auth import auth_bp
from .views import views_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(views_bp)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def init_db():
    """Initialize database tables"""
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")


# Initialize database
init_db()