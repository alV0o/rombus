import psycopg2
from psycopg2 import Error

db_config = {
    "dbname": "openmmes",
    "user": "Zit_User",
    "password": "Zit2026",
    "host": "192.168.0.134",
    "port": "5432"
}

connection = None
cursor = None
def GetProducts_():
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # SQL-запрос для получения всех записей из таблицы product_types
        select_query = "SELECT id, name FROM product_types;"
        
        cursor.execute(select_query)
        
        # Получаем все строки из результата запроса
        products = cursor.fetchall()
       

        return products

    except (Exception, Error) as error:
        print("Ошибка при чтении из PostgreSQL:", error)



if __name__ == "__main__":
    print(GetProducts_name())
    if cursor:
        cursor.close()
    if connection:
        connection.close()