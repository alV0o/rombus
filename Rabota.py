import time
import requests

# Константы конфигурации
TOKEN = "1|H6bkMBDTCSKRfuD445VVXQO55tY2Pp6PDnLIkBRe48f72971"
GET_URL = "http://localhost:8000/api/v1/work-orders/16/batches"
POST_URL_TEMPLATE = "http://192.168.0.134:8000/api/v1/batch-steps/{batchStepId}/complete"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def process_active_batch():
    while True:
        try:
            # 1. Получаем список всех батчей
            print(f"Отправка GET-запроса на {GET_URL}...")
            response = requests.get(GET_URL, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении GET-запроса: {e}")
            return

        batches = response_data.get("data", [])
        target_batch = None

        # 2. Ищем батч со статусом IN_PROGRESS
        for batch in batches:
            if batch.get("status") == "IN_PROGRESS":
                target_batch = batch
                break

        # Если батч со статусом IN_PROGRESS не найден
        if not target_batch:
            return

        # Автоматически определяем ID активного батча
        active_batch_id = target_batch.get("id")

        # 3. Обрабатываем шаги только этого выбранного батча
        steps = target_batch.get("steps", [])
        for step in steps:
            step_id = step.get("id")
            instruction = step.get("instruction")
            duration_minutes = step.get("duration_minutes")
            
            # Проверяем условие: инструкция начинается со слова "Работа"
            if isinstance(instruction, str) and instruction.strip().startswith("Работа"):
                
                # Считаем время ожидания
                minutes_to_wait = duration_minutes if duration_minutes is not None else 0
                if minutes_to_wait > 0:
                    seconds_to_wait = minutes_to_wait
                    print(f"-> Ожидание {minutes_to_wait} мин. ({seconds_to_wait} сек.)...")
                    time.sleep(seconds_to_wait)
                
                # 4. Отправляем POST запрос для завершения конкретного шага
                post_url = POST_URL_TEMPLATE.format(batchStepId=step_id)
                
                try:
                    post_response = requests.post(post_url, headers=headers, json={})
                    if post_response.status_code in [200, 201]:
                        print(f"-> Успешно! Шаг {step_id} завершен. Код: {post_response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"-> Не удалось отправить POST-запрос для шага {step_id}: {e}")
        time.sleep(5)

if __name__ == "__main__":
    process_active_batch()