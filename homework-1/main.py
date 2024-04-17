"""Скрипт для заполнения данными таблиц в БД Postgres."""
import csv
import psycopg2


csv_file_employees = "postgres-homeworks/homework-1/north_data/employees_data.csv"
csv_file_customers_data = "postgres-homeworks/homework-1/north_data/customers_data.csv"
csv_file_orders_data = "postgres-homeworks/homework-1/north_data/orders_data.csv"

conn = psycopg2.connect(host='localhost', database = 'north', user= 'postgres', password= '241655')



class Employees:

  @staticmethod
  def get_csv(csv_file):
    with open (csv_file, "r") as file:
      csv_reader = csv.DictReader(file)
      employee_list = list(csv_reader)
      return employee_list
    
  @staticmethod
  def append_table(employee_list, conn):
    try:
      with conn:
        with conn.cursor() as cur:
          for i in employee_list:
            cur.execute(
                "INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)",
                (i["employee_id"],
                i["first_name"],
                i["last_name"],
                i["title"],
                i["birth_date"],
                i["notes"]))
    finally:
      conn.close()



class Customers:

  @staticmethod
  def get_csv(csv_file):
    with open (csv_file, "r") as file:
      csv_reader = csv.DictReader(file)
      customers_data = list(csv_reader)
      return customers_data

 
  @staticmethod
  def append_table(customers_data, conn):
    try:
      with conn:
        with conn.cursor() as cur:
          for i in customers_data:
            cur.execute(
                "INSERT INTO customers_data VALUES (%s, %s, %s)",
                (i["customer_id"],
                i["company_name"],
                i["contact_name"],))
    finally:
      conn.close()


class Orders:

  @staticmethod
  def get_csv(csv_file):
    with open (csv_file, "r") as file:
      csv_reader = csv.DictReader(file)
      orders_data = list(csv_reader)
      return orders_data

 
  @staticmethod
  def append_table(orders_data, conn):
    try:
      with conn:
        with conn.cursor() as cur:
          for i in orders_data:
            cur.execute(
                "INSERT INTO orders_data VALUES (%s, %s, %s, %s, %s)",
                (i["order_id"],
                 i["customer_id"],
                 i["employee_id"],
                 i["order_date"],
                 i["ship_city"]))
    finally:
      conn.close()




customers_data = Customers()
data_table_customers = customers_data.get_csv(csv_file_customers_data)
customers_data.append_table(data_table_customers, conn)

employees_data = Employees()
data_table_employees = employees_data.get_csv(csv_file_employees)
employees_data.append_table(data_table_employees, conn)

orders_data = Orders()
data_table_orders = orders_data.get_csv(csv_file_orders_data)
orders_data.append_table(data_table_orders, conn)