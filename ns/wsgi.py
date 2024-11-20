from app import app
import os

if __name__ == "__main__":
    # Get the port from the environment variable
    port = int(os.environ.get("PORT", 4000))  # Default to 4000 for local testing
    print(f"Starting app on port {port}")  # Log the port to confirm
    app.run(host="0.0.0.0", port=port)
