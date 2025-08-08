from flask import Flask, jsonify
from db import AIResponse, Session
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:8088"])

@app.route("/api/results", methods=["GET"])
def get_results():
    session = Session()
    results = session.query(AIResponse).order_by(AIResponse.id.desc()).all()
    session.close()

    return jsonify([
        {
            "name": r.name,
            "age": r.age,
            "number": r.number,
            "response": r.response
        }
        for r in results
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
