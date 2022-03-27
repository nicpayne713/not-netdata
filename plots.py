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

    data["time"].append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    data["used_memory"].append(memory.used // (1024**3))
    data["free_memory"].append(memory.free // (1024**3))
    data["total_memory"].append(memory.total // (1024**3))
    data["cpu_usage"].append(psutil.cpu_percent())

    data["time"].popleft()
    data["used_memory"].popleft()
    data["free_memory"].popleft()
    data["total_memory"].popleft()
    data["cpu_usage"].popleft()


def cpu_chart():
    global data
    global fig
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
    return fig


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
        cpu.plotly_chart(cpu_chart())
