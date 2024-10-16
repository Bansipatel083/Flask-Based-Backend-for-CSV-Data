import csv
import pandas as pd
from datetime import datetime
from app.extensions import db
from app.models.purchase import Purchase
from app.models.purchase_details import PurchaseDetails


def fetch_purchase_data_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Error reading the CSV file: {e}")

    # Clean the data
    df.dropna(inplace=True)
    
    # Convert data types to datetime
    df['bill_date'] = pd.to_datetime(df['bill_date'])
    df['expiry_date'] = pd.to_datetime(df['expiry_date'])

    # Calculate item_total
    df['item_total'] = df['quantity'] * df['mrp']
    try:
        for bill_no, group in df.groupby('bill_no'):
            existing_purchase = Purchase.query.filter_by(bill_no=bill_no).first()
            if existing_purchase:
                print(f"Bill number {bill_no} already exists. Skipping insertion.")
                purchase = existing_purchase
            else:
                purchase = Purchase(
                    bill_no=bill_no,
                    bill_date=group['bill_date'].iloc[0],
                    bill_total=float(group['bill_total'].iloc[0])
                )
                db.session.add(purchase)
                db.session.flush()  

            # Insert into PurchaseDetails table
            for _, row in group.iterrows():
                existing_detail = PurchaseDetails.query.filter_by(purchase_id=purchase.id,medicine_name=row['medicine_name'],expiry_date=row['expiry_date']).first()
                if existing_detail:
                    existing_detail.quantity += row['quantity']
                    existing_detail.mrp = row['mrp']
                else:
                    purchase_detail = PurchaseDetails(
                        purchase_id=purchase.id,
                        medicine_name=row['medicine_name'],
                        quantity=row['quantity'],
                        mrp=row['mrp'],
                        expiry_date=row['expiry_date']
                    )
                    db.session.add(purchase_detail)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error inserting data into the database: {e}")
    finally:
        db.session.close()


def get_purchase_data(bill_no):
    try:
        # Retrieve the purchase data for the given bill_no
        purchase = Purchase.query.filter_by(bill_no=bill_no).first()

        if not purchase:
            return ({"meassage":f"That {bill_no} is not include in tha data"})

        purchase_details = PurchaseDetails.query.filter_by(purchase_id=purchase.id).all()
        # Construct the response data
        result = {
            "bill_no": purchase.bill_no,
            "bill_date": str(purchase.bill_date),
            "bill_total": purchase.bill_total,
            "items": [
                {
                    "medicine_name": detail.medicine_name,
                    "quantity": detail.quantity,
                    "mrp": detail.mrp,
                    "expiry_date": str(detail.expiry_date),
                    "item_total": detail.quantity * detail.mrp 
                }
                for detail in purchase_details
            ]
        }
        return result

    except Exception as e:
        db.session.rollback()
        raise e
    
def update_purchase_detail_data(data):
    try:
        # get data
        detail_id=data.get('id')
        new_mrp = data.get('mrp')

        if not detail_id or not new_mrp:
            return {"status":"error","message":"Missing id or MRP"}
        
        #get data from the purchase_detail
        purchase_detail = PurchaseDetails.query.get(detail_id)
        if not purchase_detail:
            return {"status": "error", "message": "Purchase detail not found"}
        
        #update mrp
        purchase_detail.mrp = new_mrp 

        db.session.commit()
        return {"status": "success", "message": "MRP updated successfully"}
    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": str(e)}
    
def delete_purchase_detail_data(data):
    try:
        detail_id= data.get('id')
        purchase_detail = PurchaseDetails.query.get(detail_id)
        if detail_id is None:
                return {"status":"error","message":"Missing id"}
        
        #only one input taking and that is "id" only
        if len(data) > 1 or 'id' not in data:
                return {"status": "error", "message": "Only 'id' is allowed as input"}
        if not purchase_detail:
                return {"status": "error", "message": "Purchase detail not found"}
        db.session.delete(purchase_detail)
        db.session.commit()

        return {"status": "success", "message": "Purchase detail deleted successfully"}
    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": str(e)}
         
def create_purchase_csv():
    try:
        # Retrieve purchases and their details using a join
        purchases = db.session.query(Purchase, PurchaseDetails).join(PurchaseDetails, Purchase.id == PurchaseDetails.purchase_id).all()
        csv_file_path = 'purchases_data.csv'

        # Create and write to the CSV file
        with open(csv_file_path, mode='w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write the header row
            csv_writer.writerow(['Bill Date', 'Bill No','Bill_total', 'Medicine Name', 'Quantity', 'MRP', 'Item Total', 'Expiry Date', 'Bill Total'])

            # Iterate through each purchase and its details
            for purchase, detail in purchases:
                csv_writer.writerow([
                    purchase.id,
                    purchase.bill_date,
                    purchase.bill_no,
                    purchase.bill_total,
                    detail.medicine_name,
                    detail.quantity,
                    detail.mrp,
                    detail.item_total,
                    detail.expiry_date
                ])

        return {"status": "success", "message": "CSV file created successfully", "file": csv_file_path}

    except Exception as e:
        return {"status": "error", "message": str(e)}


