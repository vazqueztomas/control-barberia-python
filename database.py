
import mysql.connector
from mysql.connector import Error

def create_database_connection(hostname, user_name, user_password, db ):
  connection = None
  try:
    connection = mysql.connector.connect(
      host = hostname,
      user=user_name,
      passwd = user_password,
      database = db
    )
    print("MySQL Database connection successful")
  except Error as err:
    print(f"Error: {err}")

  return connection
