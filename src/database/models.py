from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(20), nullable=False)
    price_usd = db.Column(db.Float, nullable=False)
    volume_24h = db.Column(db.Float, nullable=False)
    chain = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Pool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chain = db.Column(db.String(50), nullable=False)
    pair_address = db.Column(db.String(100), nullable=False)
    dex_id = db.Column(db.String(50))
    token_address = db.Column(db.String(100))
    liquidity_usd = db.Column(db.Float)
    volume_24h = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TokenBoost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_address = db.Column(db.String(100), nullable=False)
    boost_score = db.Column(db.Float)
    boost_rank = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)