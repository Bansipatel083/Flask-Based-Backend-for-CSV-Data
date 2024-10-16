from app.extensions import db


class PurchaseDetails(db.Model):
    __tablename__ = 'purchase_details'
    
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'), nullable=False)
    medicine_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    mrp = db.Column(db.Float, nullable=False)
    item_total = db.Column(db.Float, 
                           db.Computed('quantity * mrp'),  # or you could define as GENERATED ALWAYS AS (quantity * mrp) in SQL
                           nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<PurchaseDetail {self.medicine_name}>'