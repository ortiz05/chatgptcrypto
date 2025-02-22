from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db:5432/scanner_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    symbol = db.Column(db.String, nullable=False)
    market_cap = db.Column(db.Float, nullable=True)
    transactions = db.Column(db.Integer, nullable=True)

@app.route('/api/tokens')
def get_tokens():
    tokens = Token.query.all()
    return jsonify([
        {
            "name": token.name,
            "symbol": token.symbol,
            "market_cap": token.market_cap,
            "transactions": token.transactions,
        }
        for token in tokens
    ])

if __name__ == "__main__":
    app.run(debug=True)