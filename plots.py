from collections import defaultdict
import psutil
import socket


from collections import deque
from typing import MutableSequence

from plotly import express as px
import streamlit as st
import time
from typing import Dict

print(f"System Memory used: {psutil.virtual_memory().used // (1024 ** 3)} GB")
print(f"System Memory available: {psutil.virtual_memory().available // (1024 ** 3)} GB")
print(f"System Memory total: {psutil.virtual_memory().total // (1024 ** 3)} GB")

hostname = socket.gethostname()
print(f"Hostname: {hostname}")

partitions = psutil.disk_partitions()

# data = defaultdict(defaultdict(defaultdict(defaultdict(list))))

used_memory: Dict[float, MutableSequence[float]] = defaultdict(deque)
free_memory: Dict[float, MutableSequence[float]] = defaultdict(deque)
total_memory: Dict[float, MutableSequence[float]] = defaultdict(deque)
data: Dict[float, MutableSequence[float]] = defaultdict(list)

arr_size = 30


data["time"] = deque([None] * arr_size)
data["used_memory"] = deque([None] * arr_size)
data["free_memory"] = deque([None] * arr_size)
data["total_memory"] = deque([None] * arr_size)


def refresh_data():
    global data
    # for part in partitions:
    #     mnt = part.mountpoint
    #     if "snap" in mnt or "boot" in mnt:
    #         continue
    memory = psutil.virtual_memory()

    data["time"].appendleft(time.time())
    data["used_memory"].appendleft(memory.used // (1024**3))
    data["free_memory"].appendleft(memory.free // (1024**3))
    data["total_memory"].appendleft(memory.total // (1024**3))

    data["time"].pop()
    data["used_memory"].pop()
    data["free_memory"].pop()
    data["total_memory"].pop()


if __name__ == "__main__":

    stats = st.empty()
    while True:
        refresh_data()
        time.sleep(0.5)
        stats.plotly_chart(
            px.line(data, x="time", y=["used_memory", "free_memory", "total_memory"]),
            title=f"Memory usage on {hostname}",
        )
