from app import app
from init_db import init_db

if __name__ == "__main__":
    init_db()  # Initialize the database before running the app
    app.run(host="0.0.0.0", port=5000, debug=True)
