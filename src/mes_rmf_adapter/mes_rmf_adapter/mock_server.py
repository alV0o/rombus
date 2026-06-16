from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/task")
def get_task():
    return {
        "task_id": "task_12345",
        "pickup": {
            "place_name": "storage_1",
            "handler": "mock_arm_1"
        },
        "dropoff": {
            "place_name": "machine_1",
            "handler": "mock_machine_arm_1"
        },
        "payload": {
            "sku": "box_type_c",
            "quantity": 3
        }
    }

def main():
    uvicorn.run(app, host="127.0.0.1", port=8080)

if __name__ == "__main__":
    main()