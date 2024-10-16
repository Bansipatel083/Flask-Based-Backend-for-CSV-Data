from app.extensions import db

class Purchase(db.Model):
    __tablename__ = 'purchase'

    id = db.Column(db.Integer, primary_key=True)
    bill_date = db.Column(db.Date, nullable=False)
    bill_no = db.Column(db.String(50), unique=True, nullable=False)
    bill_total = db.Column(db.Float, nullable=False)
    
    # Relationship with PurchaseDetails
    purchase_details = db.relationship('PurchaseDetails', backref='purchase', lazy=True)

    def __repr__(self):
        return f'<Purchase {self.bill_no}>'