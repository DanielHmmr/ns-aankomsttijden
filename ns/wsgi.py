from app import app
import os

if __name__ == "__main__":
    # Fetch the port from the environment variable set by Render
    port = int(os.environ.get("PORT", 4000))  # Use 4000 as fallback if PORT is not set
    app.run(host="0.0.0.0", port=port)
