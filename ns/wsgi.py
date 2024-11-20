from app import app
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    print(f"Starting app on port {port}")  # Log the port to verify
    app.run(host="0.0.0.0", port=port)
