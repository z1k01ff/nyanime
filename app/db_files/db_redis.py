import os
import platform
from redis.asyncio import Redis

REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "test")

# Визначення ОС
if platform.system() == "Windows":
    REDIS_HOST = "10.3.100.19"  # Змініть на бажаний хост для Windows
    REDIS_PORT = 6340  # Змініть на бажаний порт для Windows
else:
    REDIS_HOST = os.getenv("REDIS_HOST", "10.3.100.19")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6340"))

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
