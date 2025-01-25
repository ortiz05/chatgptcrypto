from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db:5432/scanner_db'  # Ensure this matches the PostgreSQL setup
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/api/tokens')
def get_tokens():
    # Mocked response; replace with actual database queries
    tokens_data = [
        {"name": "Token A", "symbol": "TKA", "market_cap": 100000, "transactions": 12000},
        {"name": "Token B", "symbol": "TKB", "market_cap": 200000, "transactions": 15000}
    ]
    return jsonify(tokens_data)

if __name__ == "__main__":
    app.run(debug=True)