from database import create_database_connection
from decouple import config
from mysql.connector import Error
from datetime import datetime
import os

connection = create_database_connection(config('DATABASE_HOSTNAME'), config('DATABASE_USERNAME'), config('DATABASE_PASSWORD'), 'barber')
def menu_principal():
  print("Seleccione una opcion: \n")
  print("1) Agregar nuevo corte")
  print("2) Ver todos los cortes (con toda la info)")
  print("3) Ver corte según día")
  print("4) Ver total ganado")
  print("0) Salir")
  print()
  opcion = int(input("Ingrese la opción: "))

  while(opcion != 0):
    if opcion == 1:
      add_corte()
    elif opcion == 2:
      get_all_cortes()
    elif opcion == 3:
      fecha = input("Ingrese una fecha (formato YYYY-MM-dd): ")
      search_by_date(fecha)
    elif opcion == 4:
      total = get_total_ganado()
      print(f"El sistema lleva facturando {total} ARS.\n")
    elif opcion == 0:
      print("Gracias por utilizar el sistema de barbería")
      os.system("clear")
      break
    else:
      print("Opción incorrecta.")
    
    opcion = int(input("Ingrese una opción: "))



def main():
  os.system('clear')
  print("Bienvenido al sistema de control de barbería")
  print()
  menu_principal()


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
  
  increment_id = read_query(connection, "select id from cortes")
  increment_id = increment_id[-1][0] + 1

  print(increment_id)
  add_query = f"""
  INSERT INTO cortes
  VALUES ({increment_id},{valor},'2023-09-12')
  """
  
  execute_query(connection, add_query)

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
  cantidad_cortes = read_query(connection, f"select id from cortes where fecha ='{fecha}'")
  print(f'El dia {fecha} se realizaron {cantidad_cortes[-1][0]} cortes')

def get_total_ganado():
  cantidad_cortes = read_query(connection, f"select valor from cortes")
  total = 0

  for corte in cantidad_cortes:
    total = total + corte[0]

  return total


main()


