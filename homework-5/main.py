import json

import psycopg2

from config import config


def main():
    script_file = 'postgres-homeworks/homework-5/fill_db.sql'
    json_file = 'postgres-homeworks/homework-5/suppliers.json'
    db_name = 'my_new_db'

    params = config()
    conn = None

    create_database(params, db_name)
    print(f"БД {db_name} успешно создана")

    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                execute_sql_script(cur, script_file)
                print(f"БД {db_name} успешно заполнена")

                create_suppliers_table(cur)
                print("Таблица suppliers успешно создана")

                suppliers = get_suppliers_data(json_file)
                insert_suppliers_data(cur, suppliers)
                print("Данные в suppliers успешно добавлены")

                add_foreign_keys(cur, json_file)
                print(f"FOREIGN KEY успешно добавлены")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_database(params, db_name) -> None:
    """Создает новую базу данных."""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute(f"DROP DATABASE {db_name}")

    except Exception as e:
        print(f'Информация: {e}')

    finally:
        cur.execute(f"CREATE DATABASE {db_name}")
    conn.close()


def execute_sql_script(cur, script_file) -> None:
    """Выполняет скрипт из файла для заполнения БД данными."""
    with open (script_file, 'r') as f:
        sql_script = f.read()
        cur.execute(sql_script)


def create_suppliers_table(cur) -> None:
        cur.execute("""
            CREATE TABLE suppliers (
                company_name VARCHAR NOT NULL,
                contact VARCHAR,
                address VARCHAR,
                phone VARCHAR,
                fax VARCHAR,
                homepage VARCHAR,
                products VARCHAR
            )
        """)


def get_suppliers_data(json_file: str) -> list[dict]:
    data_list = []
    """Извлекает данные о поставщиках из JSON-файла и возвращает список словарей с соответствующей информацией."""
    with open(json_file, 'r' ) as f:
        data_json = json.load(f)
        for supplier in data_json:
            data_list.append({
                'company_name':supplier['company_name'],
                'contact':supplier['contact'],
                'address':supplier['address'],
                'phone':supplier['phone'],
                'fax':supplier['fax'],
                'homepage':supplier['homepage'],
                'products':supplier['products']
            })
    return(data_list)


def insert_suppliers_data(cur, suppliers: list[dict]) -> None:
    """Добавляет данные из suppliers в таблицу suppliers."""
    #print(suppliers)
    for supplier in suppliers:
        cur.execute(
            """
            INSERT INTO suppliers (company_name, contact, address, phone, fax,homepage, products)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (supplier['company_name'], supplier['contact'], supplier['address'], supplier['phone'],supplier['fax'],supplier['homepage'],supplier['products'])
        )
        


def add_foreign_keys(cur, json_file) -> None:
    """Добавляет foreign key со ссылкой на supplier_id в таблицу products."""
    cur.execute("""
                ALTER TABLE products ADD COLUMN supplier_id serial
                """)
    cur.execute("""
            ALTER TABLE suppliers ADD COLUMN supplier_id serial
            """)
    cur.execute("""
            ALTER TABLE suppliers ADD PRIMARY KEY (supplier_id)
            """)
    cur.execute('SELECT product_name, supplier_id  FROM products')
    product_name = cur.fetchall()


    with open(json_file, 'r') as file:
        sup_data = json.load(file)
    supplier_id = 1
    for i in sup_data:
        i['supplier_id'] = supplier_id
        supplier_id += 1

    with open(json_file, 'w') as file:
        json.dump(sup_data, file)

    with open(json_file, 'r') as file:
        sup_data = json.load(file)
    for product in product_name:
        for sup_product in sup_data:
            product = list(product)
            if product[0] in sup_product['products']:
                cur.execute(
                        f"""UPDATE products
                            SET supplier_id = {sup_product['supplier_id']}
                            WHERE product_name = '{product[0].replace("'", "''")}'""")
    cur.execute('''
        ALTER TABLE products ADD CONSTRAINT fk_products_supplier_id FOREIGN KEY(supplier_id) REFERENCES suppliers(supplier_id);
    ''')


if __name__ == '__main__':
    main()
