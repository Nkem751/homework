# Import the Flask application instance from the 'app' module
from app import app

# Check if this script is executed directly (not imported as a module)
if __name__ == '__main__':
    # Run the Flask application
    app.run()
