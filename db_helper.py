from mysql.connector import connect, Error

# Create a function to handle the connection
def get_db_connection():
    try:
        cnx = connect(
            host="localhost",
            user="root",
            password="cheshta9",
            database="pandeyji_eatery"
        )
        return cnx
    except Error as err:
        print(f"Error: {err}")
        return None

# Function to call the MySQL stored procedure and insert an order item
def insert_order_item(food_item, quantity, order_id):
    try:
        with get_db_connection() as cnx:
            if cnx is None:
                return -1  # Return error code if connection fails

            cursor = cnx.cursor()
            cursor.callproc('insert_order_item', (food_item, quantity, order_id))
            cnx.commit()
            cursor.close()

            print("Order item inserted successfully!")
            return 1

    except Error as err:
        print(f"Error inserting order item: {err}")
        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        return -1

# Function to insert a record into the order_tracking table
def insert_order_tracking(order_id, status):
    try:
        with get_db_connection() as cnx:
            if cnx is None:
                return

            cursor = cnx.cursor()
            insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
            cursor.execute(insert_query, (order_id, status))
            cnx.commit()
            cursor.close()
            print("Order tracking inserted successfully!")

    except Error as err:
        print(f"Error inserting order tracking: {err}")

# Function to get the total price of an order
def get_total_order_price(order_id):
    try:
        with get_db_connection() as cnx:
            if cnx is None:
                return 0

            cursor = cnx.cursor()
            query = f"SELECT get_total_order_price({order_id})"
            cursor.execute(query)
            result = cursor.fetchone()[0]
            cursor.close()
            return result

    except Error as err:
        print(f"Error fetching total order price: {err}")
        return 0

# Function to get the next available order_id
def get_next_order_id():
    try:
        with get_db_connection() as cnx:
            if cnx is None:
                return 1

            cursor = cnx.cursor()
            query = "SELECT MAX(order_id) FROM orders"
            cursor.execute(query)
            result = cursor.fetchone()[0]
            cursor.close()

            if result is None:
                return 1
            else:
                return result + 1

    except Error as err:
        print(f"Error fetching next order id: {err}")
        return 1

# Function to fetch the order status from the order_tracking table
def get_order_status(order_id):
    try:
        with get_db_connection() as cnx:
            if cnx is None:
                return None

            cursor = cnx.cursor()
            query = f"SELECT status FROM order_tracking WHERE order_id = %s"
            cursor.execute(query, (order_id,))  # Use parameterized query
            result = cursor.fetchone()
            cursor.close()

            if result:
                return result[0]
            else:
                return None

    except Error as err:
        print(f"Error fetching order status: {err}")
        return None


if __name__ == "__main__":
    # Test functions here
    print(get_next_order_id())
    # insert_order_item('Samosa', 3, 99)
    # insert_order_tracking(99, "in progress")
    # print(get_total_order_price(56))

