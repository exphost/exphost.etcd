#!/usr/bin/env python
import subprocess
import socket
import os
import time
import sys

sock = None
if os.getenv("NOTIFY_SOCKET"):
    print("jest notify")
    print(os.getenv("NOTIFY_SOCKET"))
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    sock.connect(os.getenv("NOTIFY_SOCKET"))
else:
    print("brak notify")
sys.stdout.flush()
proc = subprocess.Popen(["etcd", "--config-file", "/app/{{app.value.etcd.user.user}}/etcd/conf/etcd.config"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
while True:
    line = proc.stderr.readline()
    print(line)
    sys.stdout.flush()
    if "ready to serve client requests" in line:
        print("Jest server")
        break
print("ETCD started")
print("Sleep start")
sys.stdout.flush()
time.sleep(10)
if sock:
    sock.send("READY=1")
print("Sleep end")
sys.stdout.flush()

while True:
    line = proc.stderr.readline()
    print(line)
    sys.stdout.flush()
#embed: ready to serve client requests
