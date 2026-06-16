import requests
import time

id_order = input('Введите ID заказа: ')
get_url = f"http://192.168.0.134:8000/api/v1/work-orders/{id_order}/batches"
get_headers = {
    "Authorization": "Bearer 1|H6bkMBDTCSKRfuD445VVXQO55tY2Pp6PDnLIkBRe48f72971",
    "Accept": "application/json"  # Хорошая практика для работы с API
}

def parsing_order(data):
    
    for batch in data['data']:
        if batch['status'] == 'IN_PROGRESS': #в идеале сделать четвертое состояние (Должен начаться)
            for step in batch['steps']:
                if step['status'] == 'IN_PROGRESS':
                    break
                if step['status'] == 'PENDING':
                    post_url = f"http://192.168.0.134:8000/api/v1/batch-steps/{step['id']}/start"
                    post_headers ={
                        "Authorization": "Bearer 1|H6bkMBDTCSKRfuD445VVXQO55tY2Pp6PDnLIkBRe48f72971"
                    }
                    print(f'Шаг [{step['id']}] запущен')
                    response = requests.post(post_url, headers=post_headers)
                    print(f'Код статуса: [{response.status_code}]')
                    break


def main():
    while(True):
        try:
            response = requests.get(get_url, headers=get_headers ,timeout=(1.5, 3.0))

            if response.status_code == 200:
                
                data = response.json()
                parsing_order(data=data)
        except Exception as e:
            print(f'[ОШИБКА] {e}')
        finally:
            time.sleep(5)
        

if __name__ == '__main__':
    main()