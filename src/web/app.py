from flask import Flask, jsonify
from src.database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db:5432/scanner_db'  # Update for production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/api/tokens')
def get_tokens():
    # Mocked tokens response (replace with actual DB query in production)
    tokens_data = [
        {
            "name": "Token A",
            "symbol": "TKA",
            "market_cap": 100000,
            "transactions": 12000
        },
        {
            "name": "Token B",
            "symbol": "TKB",
            "market_cap": 200000,
            "transactions": 15000
        }
    ]
    return jsonify(tokens_data)

if __name__ == "__main__":
    app.run(debug=True)