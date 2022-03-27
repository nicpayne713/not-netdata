from collections import defaultdict
import psutil
import socket

from plotly import express as px
import streamlit as st
import time
from typing import Dict, List

print(f"System Memory used: {psutil.virtual_memory().used // (1024 ** 3)} GB")
print(f"System Memory available: {psutil.virtual_memory().available // (1024 ** 3)} GB")
print(f"System Memory total: {psutil.virtual_memory().total // (1024 ** 3)} GB")


print(f"Hostname: {socket.gethostname()}")

partitions = psutil.disk_partitions()

# data = defaultdict(defaultdict(defaultdict(defaultdict(list))))

used_disk: Dict[float, List[float]] = defaultdict(list)
free_disk: Dict[float, List[float]] = defaultdict(list)
total_disk: Dict[float, List[float]] = defaultdict(list)


def refresh_data():
    global used_disk
    global free_disk
    global total_disk
    # for part in partitions:
    #     mnt = part.mountpoint
    #     if "snap" in mnt or "boot" in mnt:
    #         continue
    disk = psutil.disk_usage("/")

    used_disk["time"].append(time.time())
    used_disk["disk"].append(disk.used // (1024**3))
    free_disk["time"].append(time.time())
    free_disk["disk"].append(disk.free // (1024**3))
    total_disk["time"].append(time.time())
    total_disk["disk"].append(disk.total // (1024**3))


if __name__ == "__main__":

    stats = st.empty()
    while True:
        refresh_data()
        time.sleep(2)
        stats.plotly_chart(px.line(used_disk, x="time", y="disk"))
        breakpoint()
