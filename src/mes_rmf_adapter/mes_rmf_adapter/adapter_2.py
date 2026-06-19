import rclpy
import json
import requests
import time
import uuid
import queue
from pydantic import BaseModel
from rclpy.node import Node
from rmf_task_msgs.msg import ApiRequest
from std_msgs.msg import String
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

class Location(BaseModel):
    place_name:str
    handler:str

# потенциально сделать разные для pickup и dropoff. 
class Payload(BaseModel): 
    sku:str
    quantity:int

class Task(BaseModel):
    task_id:str
    pickup:Location
    dropoff:Location
    payload:Payload

id_order = input('Введите ID заказа: ')
get_url = f"http://192.168.0.134:8000/api/v1/work-orders/{id_order}/batches"
get_headers = {
    "Authorization": "Bearer 1|9vVg1vhzPZPBGvhcTkiifUUaOChfjoYK0cmbvAP5806a0b6e",
    "Accept": "application/json"  # Хорошая практика для работы с API
}

rmf_qos = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL
)

task_queue = queue.Queue()
step_id_dict = {}

def parsing_order(data):
    global task_queue
    global step_id_dict

    
    for batch in data['data']:
        if batch['status'] == 'IN_PROGRESS': #в идеале сделать четвертое состояние (Должен начаться)
            for step in batch['steps']:
                if step['status'] == 'READY' and step['id']:
                    try:
                        json_string = json.loads(step['instruction'])
                        task = Task(**json_string)
                        task.task_id = str(uuid.uuid4())
                        print(f'Добавлен таск с id {task.task_id}')
                        
                        post_url = f"http://192.168.0.134:8000/api/v1/batch-steps/{step['id']}/start"
                        post_headers ={
                            "Authorization": "Bearer 1|9vVg1vhzPZPBGvhcTkiifUUaOChfjoYK0cmbvAP5806a0b6e"
                        }
                        print(f'Шаг [{step['id']}] запущен')
                        response = requests.post(post_url, headers=post_headers)
                        print(f'Код статуса: [{response.status_code}]')
                        
                        task_queue.put(task)
                        step_id_dict[task.task_id] = step['id']
                    except:
                        continue



class TaskPublisher(Node):
    def __init__(self):
        super().__init__('task_publisher')
        self.publisher = self.create_publisher(ApiRequest, 'task_api_requests', rmf_qos)
        timer_period = 5.0
        self.timer = self.create_timer(timer_period, self.publish_task)
        self.subscriber = self.create_subscription(String, 'task_state_update', self.status_check, 10)
        self.is_processing = False
        self.tasks_working = []


    def publish_task(self):
        global task_queue

        if self.is_processing:
            return

        try:
            response = requests.get(get_url, headers=get_headers ,timeout=(1.5, 3.0))

            if response.status_code == 200:
                
                data = response.json()
                parsing_order(data=data)
                
                if (not task_queue.empty()):
                    task = task_queue.get()

                    msg = ApiRequest()
                    msg.request_id = task.task_id
                    msg.json_msg = self.create_json_msg(task)

                    self.publisher.publish(msg)
                    self.get_logger().info(f'Задача [{task.task_id}] отправлена')
                    self.tasks_working.append(task.task_id)
            else:
                self.get_logger().error(f'Статус: [{response.status_code}]')
        except Exception as e:            
            self.get_logger().error(f'Ошибка: {str(e)}')
        finally:
            self.is_processing = False
    
    def fill_description(self, task:Task):
        return {
            'pickup': {
                'place': task.pickup.place_name,
                'handler': task.pickup.handler,
                'payload': {
                    'sku': task.payload.sku,
                    'quantity': task.payload.quantity
                }
            },
            'dropoff': {
                'place': task.dropoff.place_name,
                'handler': task.dropoff.handler,
                'payload': {
                    'sku': task.payload.sku,
                    'quantity': task.payload.quantity
                }
            }
        }

    
    def create_json_msg(self, task:Task):
        current_time_ms = int(time.time() * 1000)
        json_msg = {
            'type': 'dispatch_task_request',
            'request': {
                'unix_millis_earliest_start_time': current_time_ms, # ставим текущее время вместо 0
                'unix_millis_request_time': current_time_ms,
                'priority': {
                    'type': 'binary',
                    'value': 0
                },
                'category': 'delivery',
                'description': self.fill_description(task),
                'labels': [
                    'task_definition_id=delivery',
                    f'pickup={task.pickup.place_name}',
                    f'destination={task.dropoff.place_name}',
                    f'payload={task.payload.sku}',
                    f'track_id={task.task_id}'
                ],
                'requester': 'admin'
            }
        }
        return json.dumps(json_msg)
    
    def status_check(self, msg):
        
        global step_id_dict

        try:
            data = json.loads(msg.data)
            booking = data['data']['booking']
            labels = booking.get('labels',[])
            task_id = '-1'
            for label in labels:
                if str(label).startswith('track_id='):
                    task_id = label.split('=')[1]
            
            if task_id in self.tasks_working:
                if data['data']['status'] == 'completed':
                    id_step = step_id_dict[task_id]
                    post_url = f"http://192.168.0.134:8000/api/v1/batch-steps/{id_step}/complete"
                    post_headers ={
                        "Authorization": "Bearer 1|9vVg1vhzPZPBGvhcTkiifUUaOChfjoYK0cmbvAP5806a0b6e"
                    }
                    self.get_logger().info(f'Задача [{task_id}] выполнена')
                    response = requests.post(post_url, headers=post_headers)
                    print(f'Код статуса: {response.status_code}')


        except Exception as e:
            self.get_logger().error(f'Ошибка: {e}')
    
def main(args = None):
    rclpy.init(args=args)
    node = TaskPublisher()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()