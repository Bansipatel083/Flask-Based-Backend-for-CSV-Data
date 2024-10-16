# Flask-Based-Backend-for-CSV-Data

**Signup:**

    Creates a new user account.

**Login:**

    Authenticates the user and provides a token.

**Logout:**

    Invalidates the user's token.

**Fetch_purchase_data_from_csv:**

    Takes a CSV file as input.
    Reads, cleans, and processes the data.
    Calculates item_total and bill_total.
    Inserts the data into the purchase and purchase_details tables.

**Get_purchase_data:**

    Takes a bill_no as input.
    Retrieves data from both purchase and purchase_details tables using a join.
    Returns the data or an appropriate message if not found.

**Update_purchase_detail_data:**

    Takes an id and mrp as input.
    Updates the mrp for the specified record.
    Returns a success or failure message.

**delete_purchase_detail_data:**

    Takes an id as input.
    Deletes the record with the specified id.
    Returns a success or failure message.

**create_purchase_csv:**

    Retrieves data from purchase and purchase_details tables using a join.
    Creates a CSV file from the retrieved data.
    Stores the CSV file locally.

**postman document**

https://documenter.getpostman.com/view/21639736/2sAXxV5VLs