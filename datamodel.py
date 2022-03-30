import mysql.connector
from mysql.connector import MySQLConnection, Error
from mysql_dbconfig import read_db_config
import pandas as pd

# ***************************************
# creating mysql connection
# ***************************************
def connect():
     db_config = read_db_config()
     conn = None
     try:
         print('Connecting to MySQL database...')
         conn = MySQLConnection(**db_config)

         if conn.is_connected():
             print('Connection established')

             #get data from database

             data = get_data(conn)
             return data

         else:
             print('Connection failed')

     except Error as error:
         print(error)

     finally:
         disconnect(conn)

         if __name__ == '__main__':
            connect()

# ***************************************
# close database connecting
# ***************************************
def disconnect(conn):
    if conn is not None and conn.is_connected:
        conn.close()

# ***************************************
# getting data from database
# ***************************************
def get_data(conn):
    cursor = conn.cursor()

    # creating product dataframe
    cursor.execute('Select * from products')
    products = list(cursor.fetchall())
    product_df = pd.DataFrame(products, columns=['product_id', 'productname', 'stock', 'reorder', 'type'])

    # creating order dataframe
    cursor.execute('Select * from orders')
    orders = list(cursor.fetchall())
    order_df = pd.DataFrame(orders, columns=['order_id', 'product_id', 'unitprice',
                                             'quantity', 'customer_id', 'employee_id'])

    # creating employee dataframe
    cursor.execute('Select * from employees')
    employees = list(cursor.fetchall())
    employee_df = pd.DataFrame(employees, columns=['employee_id', 'firstname', 'lastname', 'date_of_birth'])
    employee_names = merge_employee_names(employee_df)

    # creating customer dataframe
    cursor.execute('Select * from customers')
    customers = list(cursor.fetchall())
    customer_df = pd.DataFrame(customers, columns=['customer_id', 'first_name', 'last_name'])
    customer_names = merge_customer_names(customer_df)

    customer_df.insert(len(customer_df.columns), 'cust_name', customer_names)
    employee_df.insert(len(employee_df.columns), 'emp_name', employee_names)

    # add new columns to the order dataframe order_df

    total_price=[]

    for i in range(0, len(order_df.get('order_id'))):
        total_price.append(float(order_df.get('unitprice')[i])
                                 * float(order_df.get('quantity')[i].item()))

    order_df.insert(len(order_df.columns), 'total', total_price)

    # merge tables

    merged_table = pd.merge(order_df, product_df, on='product_id')
    merged_table = pd.merge(merged_table, employee_df, on='employee_id')
    merged_table = pd.merge(merged_table, customer_df, on='customer_id')

    merged_table = merged_table[['order_id', 'product_id', 'productname', 'type', 'customer_id', 'cust_name',
                                 'employee_id', 'emp_name', 'total']]

    return merged_table

# ***************************************
# function for merging customer names
# ***************************************
def merge_customer_names(list):
    customer_names = []
    for i in range(0,len(list.get('first_name'))):
        customer_names.append(str(list.get('first_name')[i] + ' ' +
                                  list.get('last_name')[i]))

    return customer_names

# ***************************************
# function for merging employee names
# ***************************************
def merge_employee_names(list):
    employee_names = []
    for i in range(0,len(list.get('firstname'))):
        employee_names.append(str(list.get('firstname')[i] + ' ' +
                                  list.get('lastname')[i]))

    return employee_names

# ***************************************
# creating datamodel to import into app.py
# ***************************************
def  create_datamodel(df_products,df_orders,df_employees,df_customers):
    df_employees['emp_name'] = df_employees['firstname'] + ' ' + df_employees['lastname']
    df_customers['cust_name'] = df_customers('first_name') + ' ' + df_customers['last_name']
    df_orders['total'] = df_orders['unitprice'] * df_orders['quantity']

    #df_order['deliverytime'] = df_order['deliverydate'] - df_order['orderdate']
    #df_order['orderyear'] = df_order['orderdate'].dt.strftime("%Y")
    #df_order['ordermonth'] = pd.to_datetime(df_order['orderdate'])
    #df_order['ordermonth'] = df_order['ordermonth'].dt.month_name()

    order = pd.merge(df_orders, df_products, on='product_id')
    order = pd.merge(order, df_employees, on='employee_id')
    order = pd.merge(order, df_customers, on='customer_id')
    order = order[['order_id',
                'product_id', 'productname', 'type',
                'customer_id', 'cust_name',
                'employee_id', 'emp_name', 'total']]
    return order