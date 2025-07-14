from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Run your Flask app
import app.main
app.main.app.run(debug=False)
