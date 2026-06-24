import psycopg2
from psycopg2 import Error

db_config = {
    "dbname": "openmmes",
    "user": "Zit_User",
    "password": "Zit2026",
    "host": "192.168.0.134",
    "port": "5432"
}

def GetLastStep(template_id: int):  # <-- Теперь принимаем template_id
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # ИСПРАВЛЕНО: ищем последний шаг именно для ТЕКУЩЕГО шаблона
        select_query = """
            SELECT step_number 
            FROM template_steps 
            WHERE process_template_id = %s 
            ORDER BY step_number DESC 
            LIMIT 1;
        """
        cursor.execute(select_query, (template_id,))
        products = cursor.fetchall()

        if not products:
            return 0
        return products[0][0]  # Поскольку LIMIT 1, здесь всегда будет один элемент

    except (Exception, Error) as error:
        print("Ошибка при чтении из PostgreSQL (GetLastStep):", error)
        return 0
    finally:
        if 'connection' in locals() and connection:
            cursor.close()
            connection.close()


def AddStep(PrductID, instruction, name):
    connection = None
    try:
        # 1. Сначала получаем ID шаблона процесса
        template_id = GetProcessTem(PrductID)

        if template_id is None:
            print(f"Ошибка: Не найден шаблон процесса для Product ID {PrductID}")
            return

        # 2. Передаем найденный template_id, чтобы узнать ЕГО последний шаг
        last_step = GetLastStep(template_id)

        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        insert_query = """
            INSERT INTO template_steps (
                process_template_id, step_number, name, instruction,
                estimated_duration_minutes, workstation_id, created_at, 
                min_duration_minutes, requires_confirmation, process_segment_id, 
                is_optional, variant_group, is_default_variant, deleted_at, deleted_by_id
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s) 
            RETURNING id;
        """
        
        new_step_data = (
            template_id,         
            last_step + 1,       # Теперь это гарантированно будет уникальный номер для этого шаблона
            name,                
            instruction,         
            None,                
            None,                
            None,                
            False,               
            None,                
            False,               
            None,                
            False,               
            None,                
            None                 
        )

        cursor.execute(insert_query, new_step_data)
        generated_id = cursor.fetchone()[0]
        connection.commit()
        print(f"Успешно добавлена строка с ID: {generated_id}")

    except (Exception, Error) as error:
        print("Ошибка при записи в PostgreSQL (AddStep):", error)
        if connection:
            connection.rollback()
    finally:
        if connection:
            cursor.close()
            connection.close()


def GetProcessTem(ProductID: int):
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        select_query = """
            SELECT id  
            FROM process_templates 
            WHERE product_type_id = %s 
            ORDER BY version DESC 
            LIMIT 1;
        """
        cursor.execute(select_query, (ProductID,))
        products = cursor.fetchall()

        if not products:
            return None
        return products[-1][0]  # ВАЖНО: Добавили return вместо print!

    except (Exception, Error) as error:
        print("Ошибка при чтении из PostgreSQL (GetProcessTem):", error)
        return None
    finally:
        if 'connection' in locals() and connection:
            cursor.close()
            connection.close()


#def AddStep(PrductID, instruction, name):
    connection = None
    try:
        # Получаем данные ДО открытия основного соединения, чтобы не плодить транзакции
        template_id = GetProcessTem(PrductID)
        last_step = GetLastStep()

        if template_id is None:
            print(f"Ошибка: Не найден шаблон процесса для Product ID {PrductID}")
            return

        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        insert_query = """
            INSERT INTO template_steps (
                process_template_id, step_number, name, instruction,
                estimated_duration_minutes, workstation_id, created_at, 
                min_duration_minutes, requires_confirmation, process_segment_id, 
                is_optional, variant_group, is_default_variant, deleted_at, deleted_by_id
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s) 
            RETURNING id;
        """
        
        # Теперь здесь передаются чистые типы данных (int, str, bool)
        new_step_data = (
            template_id,         # process_template_id (уже число)
            last_step + 1,       # step_number (число + 1 работает отлично!)
            name,                # name
            instruction,         # instruction (наша JSON строка)
            None,                # estimated_duration_minutes
            None,                # workstation_id
            None,                # min_duration_minutes
            False,               # requires_confirmation
            None,                # process_segment_id
            False,               # is_optional
            None,                # variant_group
            False,               # is_default_variant
            None,                # deleted_at
            None                 # deleted_by_id
        )

        cursor.execute(insert_query, new_step_data)
        generated_id = cursor.fetchone()[0]
        connection.commit()
        print(f"Успешно добавлена строка с ID: {generated_id}")

    except (Exception, Error) as error:
        print("Ошибка при записи в PostgreSQL (AddStep):", error)
        if connection:
            connection.rollback()
    finally:
        if connection:
            cursor.close()
            connection.close()