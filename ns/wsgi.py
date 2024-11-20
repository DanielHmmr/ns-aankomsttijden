from app import app

if __name__ == "__main__":
    # Ensure Flask listens on 0.0.0.0 to be accessible externally
    app.run(host="0.0.0.0", port=4000)
