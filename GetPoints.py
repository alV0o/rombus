import requests

# Настройки API
 
API_URL_MAPS = "http://192.168.0.144:8080/maps"  


def get_api_maps():
    
    try:
        response = requests.get(API_URL_MAPS)
        response.raise_for_status()
        api_response = response.json()

        # Собираем массив объектов с явным указанием роли
        return api_response
    except requests.exceptions.RequestException as e:
        print(f"Ошибка API: {e}")
        return []

def get_api_points(name):
    # Защита 1: Проверяем, что name — это строка, а не объект виджета
    if not isinstance(name, str):
        # Если пришел объект комбобокса, пробуем вытащить из него выбранное значение
        if hasattr(name, "get"):
            name = name.get()
        else:
            print(f"Ошибка: В get_api_points передан некорректный тип данных: {type(name)}")
            return []

    API_URL = f"http://192.168.0.144:8080/coords/{name}" 
    
    # Защита 2: Игнорируем системный прокси локально для этого запроса
    session = requests.Session()
    session.trust_env = False  # Это заставит requests игнорировать переменные окружения прокси

    try:
        response = session.get(API_URL, timeout=5) # Добавили таймаут, чтобы скрипт не зависал навсегда
        response.raise_for_status()
        api_response = response.json()

        # Проверяем, что нам пришел словарь, как ожидает вложенный цикл
        if not isinstance(api_response, dict):
            print("Ошибка: API вернул данные не в формате словаря (dict)")
            return []

        # Собираем массив объектов с явным указанием роли
        points_list = [
            {
                "place_name": place_name,
                "role": "pickup" if "pickup" in str(role).lower() else "dropoff", # Приводим к lower для надежности
                "handler": handler_name,
            }
            for place_name, handlers in api_response.items()
            if isinstance(handlers, dict) # Защита от некорректной структуры внутри ответа
            for role, handler_name in handlers.items()
        ]
        return points_list

    except requests.exceptions.RequestException as e:
        print(f"Ошибка API при запросе к {API_URL}: {e}")
        return []

# Запуск функции
if __name__ == "__main__":
    result_points = get_api_points()
    print("Полученный массив точек:")
    print(result_points)