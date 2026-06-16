import rclpy
import uvicorn
import json
import time
import threading
from rclpy.node import Node
from fastapi import FastAPI
from pydantic import BaseModel
from rmf_task_msgs.msg import ApiRequest
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

class PickupPoint(BaseModel):
    place_name:str
    handler:str

class DropoffPoint(BaseModel):
    place_name:str
    handler:str

# потенциально сделать разные для pickup и dropoff. 
class Payload(BaseModel): 
    sku:str
    quantity:int

class Task(BaseModel):
    task_id:str
    pickup:PickupPoint
    dropoff:DropoffPoint
    payload:Payload

app = FastAPI()

getted_task: Task = None

task_lock = threading.Lock()

@app.post("/submit_task")
def handle_mes_task(task: Task):

    global getted_task

    print(f"Получена задача с ID: {task.task_id}")
    print(f"Нужно забрать из точки: {task.pickup.place_name}")
    print(f"Тип детали: {task.payload.sku}, Количество: {task.payload.quantity}")

    with task_lock:
        getted_task = task

    return {"status": "success", "message": f"Task {task.task_id} received"}


rmf_qos = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL
)


class TaskPublisher(Node):
    def __init__(self):
        super().__init__('task_publisher')
        self.publisher = self.create_publisher(ApiRequest, 'task_api_requests', rmf_qos)
        timer_period = 1.0
        self.timer = self.create_timer(timer_period, self.publish_task)


    def publish_task(self):
        global getted_task
        
        with task_lock:
            if getted_task != None:
                self.msg = ApiRequest()
                self.msg.request_id = getted_task.task_id
                self.msg.json_msg = self.create_json_msg(getted_task)
            
                self.publisher.publish(self.msg)
                self.get_logger().info('Задача отправлена')

                getted_task = None
    
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
                    f'payload={task.payload.sku}'
                ],
                'requester': 'admin'
            }
        }
        return json.dumps(json_msg)
    
def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8080)

def main(args = None):
    api_thread = threading.Thread(target=run_fastapi, daemon=True)
    api_thread.start()

    rclpy.init(args=args)
    node = TaskPublisher()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()    