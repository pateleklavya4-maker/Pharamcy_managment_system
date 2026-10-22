from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# Configure MySQL Connection
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'Ekla@2012',  # Replace with your MySQL password
    'database': 'pharmacy'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    query = request.args.get('search', '')
    category = request.args.get('category', '')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    sql = """
        SELECT m.medicine_id, m.med_name, m.brand_name, m.category, m.unit_price,
               b.batch_number, b.expiry_date, b.stock_qty
        FROM Medicines m
        JOIN Batches b ON m.medicine_id = b.medicine_id
        WHERE 1=1
    """
    params = []
    if query:
        sql += " AND (m.med_name LIKE %s OR m.brand_name LIKE %s)"
        params.extend([f"%{query}%", f"%{query}%"])
    if category and category != 'All':
        sql += " AND m.category = %s"
        params.append(category)
        
    cursor.execute(sql, params)
    inventory = cursor.fetchall()
    
    cursor.execute("SELECT DISTINCT category FROM Medicines")
    categories = [row['category'] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    return render_template('index.html', inventory=inventory, categories=categories, search=query, selected_cat=category)

@app.route('/expiry')
def expiry_tracker():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    sql = """
        SELECT m.med_name, m.brand_name, b.batch_number, b.expiry_date, b.stock_qty,
               CASE 
                   WHEN b.expiry_date < CURDATE() THEN 'EXPIRED'
                   WHEN b.expiry_date <= DATE_ADD(CURDATE(), INTERVAL 30 DAY) THEN 'EXPIRING SOON'
                   ELSE 'SAFE'
               END AS status
        FROM Batches b
        JOIN Medicines m ON b.medicine_id = m.medicine_id
        ORDER BY b.expiry_date ASC
    """
    cursor.execute(sql)
    batches = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('expiry.html', batches=batches)

@app.route('/billing', methods=['GET', 'POST'])
def billing():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        customer_phone = request.form.get('customer_phone')
        batch_id = request.form.get('batch_id')
        qty_sold = int(request.form.get('quantity'))
        
        # Get batch price & current stock
        cursor.execute("SELECT m.unit_price, b.stock_qty FROM Batches b JOIN Medicines m ON b.medicine_id = m.medicine_id WHERE b.batch_id = %s", (batch_id,))
        item_info = cursor.fetchone()
        
        if item_info and item_info['stock_qty'] >= qty_sold:
            subtotal = float(item_info['unit_price']) * qty_sold
            
            # Insert Bill
            cursor.execute("INSERT INTO Bills (customer_name, customer_phone, total_amount) VALUES (%s, %s, %s)", (customer_name, customer_phone, subtotal))
            bill_id = cursor.lastrowid
            
            # Insert Bill Item
            cursor.execute("INSERT INTO Bill_Items (bill_id, batch_id, quantity_sold, subtotal) VALUES (%s, %s, %s, %s)", (bill_id, batch_id, qty_sold, subtotal))
            
            # Update Stock
            cursor.execute("UPDATE Batches SET stock_qty = stock_qty - %s WHERE batch_id = %s", (qty_sold, batch_id))
            conn.commit()
            
        cursor.close()
        conn.close()
        return redirect(url_for('billing'))
        
    cursor.execute("""
        SELECT b.batch_id, m.med_name, m.brand_name, b.batch_number, b.expiry_date, b.stock_qty, m.unit_price 
        FROM Batches b 
        JOIN Medicines m ON b.medicine_id = m.medicine_id 
        WHERE b.expiry_date >= CURDATE() AND b.stock_qty > 0
    """)
    available_batches = cursor.fetchall()
    
    cursor.execute("SELECT * FROM Bills ORDER BY bill_date DESC LIMIT 5")
    recent_bills = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('billing.html', batches=available_batches, bills=recent_bills)

if __name__ == '__main__':
    app.run(debug=True)