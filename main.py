from fastapi import FastAPI
from datetime import datetime
import psutil
import os

app = FastAPI()

# Глобальная переменная для хранения данных
memory_hog = []

@app.get("/")
def read_root():
    return {
        "message": "Hello World from FastAPI!",
        "timestamp": datetime.now().isoformat(),
        "memory_usage_mb": psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024,
        "cpu_percent": psutil.cpu_percent(interval=1)
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/ready")
def readiness_check():
    return {"status": "ready"}

@app.get("/startup")
def startup_check():
    return {"status": "started"}

@app.get("/stress-memory/{mb}")
def stress_memory(mb: int):
    """Занять N мегабайт памяти"""
    global memory_hog
    try:
        # Выделяем память (1 MB = 1024 * 1024 байт)
        memory_hog.append(bytearray(mb * 1024 * 1024))
        current_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        return {
            "allocated_mb": mb,
            "total_allocated_mb": sum(len(x) for x in memory_hog) / 1024 / 1024,
            "current_memory_mb": current_memory,
            "message": f"Allocated {mb}MB"
        }
    except MemoryError:
        return {"error": "Memory allocation failed"}

@app.get("/stress-cpu/{seconds}")
def stress_cpu(seconds: int):
    """Нагрузить CPU на N секунд"""
    import time
    start = time.time()
    result = 0
    while time.time() - start < seconds:
        result += sum(range(10000))
    return {
        "duration_seconds": seconds,
        "cpu_percent": psutil.cpu_percent(interval=1),
        "message": f"CPU stressed for {seconds} seconds"
    }

@app.get("/clear-memory")
def clear_memory():
    """Очистить выделенную память"""
    global memory_hog
    size = sum(len(x) for x in memory_hog) / 1024 / 1024
    memory_hog.clear()
    return {"message": f"Cleared {size}MB"}

@app.get("/metrics")
def get_metrics():
    """Получить текущие метрики"""
    process = psutil.Process(os.getpid())
    return {
        "memory_mb": process.memory_info().rss / 1024 / 1024,
        "cpu_percent": psutil.cpu_percent(interval=1),
        "allocated_mb": sum(len(x) for x in memory_hog) / 1024 / 1024
    }
