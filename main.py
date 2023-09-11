from database import create_database_connection
from decouple import config
from mysql.connector import Error
from datetime import datetime

connection = create_database_connection(config('DATABASE_HOSTNAME'), config('DATABASE_USERNAME'), config('DATABASE_PASSWORD'), 'barber')

def execute_query(connection, query):
  cursor = connection.cursor()
  try:
    cursor.execute(query)
    connection.commit()
    print("Query successful")
  except Error as err:
    print(f"Error: {err}")


def read_query(connection, query):
  cursor = connection.cursor()
  result = None
  try:
    cursor.execute(query)
    result = cursor.fetchall()
    return result
  except Error as err:
    print(f'Error : {err}')


def add_corte():
  valor = int(input('Ingrese el valor del corte:'))

  fecha = datetime.now().strftime("%Y-%m-%d")
  fecha = str(fecha)
  
  increment_id = read_query(connection, "select * from cortes")
  increment_id = increment_id[-1][0] + 1


  add_query = f"""
  INSERT INTO cortes
  VALUES ({increment_id},{valor},'2023-09-12')
  """
  
  execute_query(connection, add_query)
  print('add succesfull')

def get_total_cortes():
  results = read_query(connection, "select * from cortes")
  total = 0
  for result in results:
    total += result[1]
  return total
  

def get_all_cortes():
  results = read_query(connection, "select * from cortes")
  for result in results:
    print(result)

def search_by_date(fecha):
  results = read_query(connection, f"select * from cortes where fecha = '{fecha}'")
  if len(results) == 0:
    print('No hay cortes en esa fecha')

  for result in results:
    print(result)

def get_cantidad_cortes(fecha):
  results = read_query(connection, f"select * from cortes where fecha ='{fecha}'")
  print(f'El dia {fecha} se realizaron {results[-1][0]} cortes')


search_by_date('2023-09-11')
get_cantidad_cortes('2023-09-11')


