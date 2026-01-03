import sys
import os
from dotenv import load_dotenv

# Add the current directory to sys.path so 'app' can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import create_app  # type: ignore

load_dotenv()

# Initialize the application using the factory pattern
app = create_app()

if __name__ == "__main__":
    # Debug mode enabled for Development Phase
    # Host 0.0.0.0 allows external access if needed during testing
    app.run(debug=True, host='0.0.0.0', port=5000)