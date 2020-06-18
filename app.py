import sys
import os
import platform
import subprocess
import queue
import threading
import time

from setting import MODE, NUM_PING, NUM_WORKER
from resource.device_list import device_list
from utils.output_translation import *
from utils.json_reader import get_cctv_dict_from_json


def worker_func(pingArgs, pending, done):
    try:
        while True:
            # Mendapatkan alamat selanjutnya untuk di ping
            address = pending.get_nowait()

            start_time = time.time()

            ping = subprocess.Popen(pingArgs + [address[1]],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE
                                    )
            out, error = ping.communicate()

            ping_time = (time.time() - start_time) / float(NUM_PING)
            ping_time = "%.3f" % ping_time

            out = output_success(str(out))
            error = output_error(str(error))

            # hasilnya dimasukkan ke done
            done.put([out, ping_time, address[1], address[0], error, ])

    except queue.Empty:
        # Tidak ada lagi alamat
        pass
    finally:
        # Beritahu main thread pekerjaannya diakhiri
        done.put(None)


plat = platform.system()
scriptDir = sys.path[0]
hosts = os.path.join(scriptDir, 'hosts.txt')

# argumen untuk ping mengecualikan alamat ip
if plat == "Windows":
    pingArgs = ["ping", "-n", f"{NUM_PING}", "-l", "1", "-w", "100"]
elif plat == "Linux":
    pingArgs = ["ping", "-c", f"{NUM_PING}", "-l", "1", "-s", "1", "-W", "1"]
else:
    raise ValueError("Platform tidak didukung")

# antrian alamat untuk di ping
pending = queue.Queue()

# antrian untuk hasil
done = queue.Queue()

# memuat worker sebanyak NUM-WORKER
workers = []
for _ in range(NUM_WORKER):
    workers.append(threading.Thread(
        target=worker_func, args=(pingArgs, pending, done)))

# Masukkan alamat ke antrian pending
# cctv_dict = device_list
cctv_dict = get_cctv_dict_from_json()
print(f"Memulai ping ke {len(cctv_dict.keys())} host...")
for device in cctv_dict.keys():
    pending.put([device, cctv_dict[f"{device}"]])  # memasukkan [key, value]

# memulai semua worker
for w in workers:
    w.daemon = True
    w.start()

# Cetak hasilnya begitu tiba
numTerminated = 0
list_to_print = []
while numTerminated < NUM_WORKER:
    result = done.get()
    if result is None:
        # Worker di akhiri
        numTerminated += 1
    else:
        if MODE == 1:
            if result[0] == "DOWN" or result[0] == "DOWN/UP":
                list_to_print.append(result)
                # print(result)
        if MODE == 0:
            # print(result)
            list_to_print.append(result)


# Menunggu semua worker diakhiri
for w in workers:
    w.join()

# Mencetak List
for i in range(len(list_to_print)):
    print(f"{i+1} > {list_to_print[i]}")
