from fastapi import FastAPI
import time
import threading

app = FastAPI()

# Глобальные переменные для стресс-теста
memory_data = []
cpu_stress_active = False

def cpu_intensive_task():
    """Постоянная нагрузка на CPU"""
    while cpu_stress_active:
        _ = sum(range(1000000))

@app.on_event("startup")
async def startup_event():
    global cpu_stress_active, memory_data
    
    # Выделяем 200MB памяти при старте
    print("Allocating 200MB of memory...")
    memory_data = [bytearray(200 * 1024 * 1024)]
    
    # Запускаем 4 потока для нагрузки CPU
    print("Starting CPU stress threads...")
    cpu_stress_active = True
    for i in range(4):
        thread = threading.Thread(target=cpu_intensive_task, daemon=True)
        thread.start()

@app.get("/")
def read_root():
    return {
        "message": "Heavy Resource Consumer",
        "memory_allocated_mb": sum(len(x) for x in memory_data) / 1024 / 1024,
        "cpu_threads": 4
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
