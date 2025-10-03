from flask import Flask

app = Flask(__name__)

@app.get("/")
def hello():
    return "CRYPTO XOR!\n"

if __name__ == "__main__":
    # Bind to all interfaces inside the container
    app.run(host="0.0.0.0", port=8000)
