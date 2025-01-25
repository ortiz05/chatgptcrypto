from flask import Flask, jsonify
from src.database.models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scanner.db'  # Update to Postgres for production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/api/stats')
def get_stats():
    return jsonify({
        "message": "Improved endpoints with error handling",
    })

if __name__ == "__main__":
    app.run(debug=True)