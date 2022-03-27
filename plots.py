from collections import defaultdict
from plotly import graph_objs as go
import psutil
import socket

from collections import deque
from typing import MutableSequence

from plotly import express as px
import streamlit as st
import time
from typing import Dict, Optional

print(f"System Memory used: {psutil.virtual_memory().used // (1024 ** 3)} GB")
print(f"System Memory available: {psutil.virtual_memory().available // (1024 ** 3)} GB")
print(f"System Memory total: {psutil.virtual_memory().total // (1024 ** 3)} GB")

hostname = socket.gethostname()
print(f"Hostname: {hostname}")

partitions = psutil.disk_partitions()

# data = defaultdict(defaultdict(defaultdict(defaultdict(list))))

used_memory: Dict[float, MutableSequence[Optional[float]]] = defaultdict(deque)
free_memory: Dict[float, MutableSequence[Optional[float]]] = defaultdict(deque)
total_memory: Dict[float, MutableSequence[Optional[float]]] = defaultdict(deque)
data: Dict[str, MutableSequence[Optional[float]]] = defaultdict(deque)

arr_size = 30


data["time"] = deque([None] * arr_size)
data["used_memory"] = deque([None] * arr_size)
data["free_memory"] = deque([None] * arr_size)
data["total_memory"] = deque([None] * arr_size)
data["cpu_usage"] = deque([None] * arr_size)


def refresh_data():
    global data
    # for part in partitions:
    #     mnt = part.mountpoint
    #     if "snap" in mnt or "boot" in mnt:
    #         continue
    memory = psutil.virtual_memory()

    data["time"].appendleft(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    data["used_memory"].appendleft(memory.used // (1024**3))
    data["free_memory"].appendleft(memory.free // (1024**3))
    data["total_memory"].appendleft(memory.total // (1024**3))
    data["cpu_usage"].appendleft(psutil.cpu_percent())

    data["time"].pop()
    data["used_memory"].pop()
    data["free_memory"].pop()
    data["total_memory"].pop()
    data["cpu_usage"].pop()


if __name__ == "__main__":

    stats = st.empty()
    cpu = st.empty()
    while True:
        refresh_data()
        time.sleep(0.5)
        stats.plotly_chart(
            px.line(data, x="time", y=["used_memory", "free_memory", "total_memory"]),
            title=f"Memory usage on {hostname}",
        )
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=data["cpu_usage"][-1],
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": "CPU %"},
                delta={"reference": data["cpu_usage"][-2]},
                gauge={
                    "axis": {"range": [0, 100]},
                    "steps": [
                        {"range": [0, 50], "color": "lightgray"},
                        {"range": [50, 90], "color": "gray"},
                        {"range": [90, 100], "color": "red"},
                    ],
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": 95,
                    },
                },
            )
        )
        cpu.plotly_chart(fig)
