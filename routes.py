# routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from config import get_db_connection

# Define the Blueprint
routes = Blueprint('routes', __name__)

@routes.route('/')
def homepage():
    return render_template('home.html')

@routes.route('/clients')
def view_clients():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get sorting parameters from the query string
    sort_by = request.args.get('sort_by')
    order = request.args.get('order', 'asc')  # Default to ascending if not specified
    order_sql = 'ASC' if order == 'asc' else 'DESC'

    # Determine the SQL query based on sorting parameters
    if sort_by == 'first_name':
        cursor.execute(f"SELECT * FROM clients ORDER BY first_name {order_sql}")
    elif sort_by == 'last_name':
        cursor.execute(f"SELECT * FROM clients ORDER BY last_name {order_sql}")
    else:
        cursor.execute("SELECT * FROM clients")  # Default: no sorting

    clients = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        'clients.html',
        clients=clients,
        selected_sort_by=sort_by,
        selected_order=order
    )

@routes.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clients (first_name, last_name, email, phone_number) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, email, phone_number)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Client added successfully!')
        return redirect(url_for('routes.view_clients'))
    return render_template('add_client.html')

@routes.route('/delete_client/<int:client_id>', methods=['POST'])
def delete_client(client_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clients WHERE client_id = %s", (client_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Client deleted successfully!')
    return redirect(url_for('routes.view_clients'))

@routes.route('/loans')
def view_loans():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get sorting parameters from the query string
    sort_by = request.args.get('sort_by')
    order = request.args.get('order', 'asc')  # Default to ascending if not specified
    order_sql = 'ASC' if order == 'asc' else 'DESC'

    # Determine the SQL query based on sorting parameters
    if sort_by == 'amount':
        cursor.execute(f"SELECT * FROM loans ORDER BY amount {order_sql}")
    elif sort_by == 'interest_rate':
        cursor.execute(f"SELECT * FROM loans ORDER BY interest_rate {order_sql}")
    elif sort_by == 'start_date':
        cursor.execute(f"""
            SELECT loan_id, loan_type, amount, interest_rate, start_date 
            FROM loans
            ORDER BY start_date {order_sql}
        """)
    else:
        cursor.execute("SELECT * FROM loans")  # Default: no sorting

    loans = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        'loans.html',
        loans=loans,
        selected_sort_by=sort_by,
        selected_order=order
    )

@routes.route('/add_loan', methods=['GET', 'POST'])
def add_loan():
    if request.method == 'POST':
        loan_type = request.form['loan_type']
        amount = request.form['amount']
        interest_rate = request.form['interest_rate']
        start_date = request.form['start_date']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO loans (loan_type, amount, interest_rate, start_date) VALUES (%s, %s, %s, %s)",
            (loan_type, amount, interest_rate, start_date)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Loan added successfully!')
        return redirect(url_for('routes.view_loans'))
    return render_template('add_loan.html')

@routes.route('/delete_loan/<int:loan_id>', methods=['POST'])
def delete_loan(loan_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM loans WHERE loan_id = %s", (loan_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Loan deleted successfully!')
    return redirect(url_for('routes.view_loans'))

@routes.route('/contracts')
def view_contracts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch all clients for the dropdown selection
    cursor.execute("SELECT client_id, first_name, last_name FROM clients")
    clients = cursor.fetchall()

    # Check if a client_id parameter is provided for filtering
    client_id = request.args.get('client_id')
    if client_id:
        cursor.execute("""
            SELECT cl.client_id, cl.loan_id, cl.loan_date, 
                   c.first_name AS client_first_name, c.last_name AS client_last_name,
                   l.loan_type, l.amount
            FROM contracts cl
            JOIN clients c ON cl.client_id = c.client_id
            JOIN loans l ON cl.loan_id = l.loan_id
            WHERE cl.client_id = %s
        """, (client_id,))
    else:
        cursor.execute("""
            SELECT cl.client_id, cl.loan_id, cl.loan_date, 
                   c.first_name AS client_first_name, c.last_name AS client_last_name,
                   l.loan_type, l.amount
            FROM contracts cl
            JOIN clients c ON cl.client_id = c.client_id
            JOIN loans l ON cl.loan_id = l.loan_id
        """)
    
    contracts = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('contracts.html', contracts=contracts, clients=clients, selected_client_id=client_id)

@routes.route('/add_client_loan', methods=['GET', 'POST'])
def add_client_loan():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT client_id, first_name, last_name FROM clients")
    clients = cursor.fetchall()
    cursor.execute("SELECT loan_id, loan_type FROM loans")
    loans = cursor.fetchall()

    if request.method == 'POST':
        client_id = request.form['client_id']
        loan_id = request.form['loan_id']
        loan_date = request.form['loan_date']

        cursor.execute(
            "INSERT INTO contracts (client_id, loan_id, loan_date) VALUES (%s, %s, %s)",
            (client_id, loan_id, loan_date)
        )
        conn.commit()
        flash('Client Loan added successfully!')
        return redirect(url_for('routes.view_contracts'))

    cursor.close()
    conn.close()
    return render_template('add_client_loan.html', clients=clients, loans=loans)

@routes.route('/delete_client_loan/<int:client_id>/<int:loan_id>', methods=['POST'])
def delete_client_loan(client_id, loan_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contracts WHERE client_id = %s AND loan_id = %s", (client_id, loan_id))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Client Loan relationship deleted successfully!')
    return redirect(url_for('routes.view_contracts'))