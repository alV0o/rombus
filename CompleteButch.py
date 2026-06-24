import subprocess
import json

num = 2
qualty = 50

# Передаем аргументы в виде списка — это безопаснее и не зависит от оболочки bash
cmd = [
    "curl", "-X", "POST",
    "-H", "Authorization: Bearer 1|EljXTrGO0HeAq7sQNb2a3SOhxKfyMlWl94QHyOI3f506e386",
    "-H", "Content-Type: application/json",
    "-d", json.dumps({"produced_qty": qualty}),
    f"http://localhost:8000/api/v1/batch-steps/{num}/complete"
]

# Выполняем команду напрямую
result = subprocess.run(cmd, capture_output=True, text=True)

print("Вывод (STDOUT):", result.stdout)
print("Ошибки (STDERR):", result.stderr)