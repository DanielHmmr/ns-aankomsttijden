from app import app
import os

if __name__ == "__main__":
    # Get the port from the environment variable (this will be set by Render)
    port = int(os.environ.get("PORT", 4000))  # Default to 4000 if PORT is not set
    app.run(host="0.0.0.0", port=port)
