"""
A simple library that wraps functions and methods and sends telemetry data.

Copyright (c) 2018 nortonjp@cs.wa.edu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import time
import os
import csv
import sys
import uuid
import json
import socket
import getpass
import requests

from threading import Thread

OPERATION = lambda payload: print(json.dumps(payload, indent=2))

try:
    CODE_VER = __version__
except NameError:
    CODE_VER = "unknown"

META = {
    'runid': str(uuid.uuid4()),
    'pwd': os.getcwd(),
    'path': os.getenv('PATH'),
    'executable': sys.executable,
    'pyver': ".".join((str(_) for _ in sys.version_info)),
    'codever': CODE_VER,
    'host': socket.gethostname(),
    'user': getpass.getuser()
}

class TimeProfiler:

    def __init__(self, identifier: str = 'anonymous-time-profiler'):
        self.identifier = identifier

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        total_time = end - self.start
        send_telemetry({
            'eventid': str(uuid.uuid4()),
            'telemetryid': self.identifier,
            'runtime': total_time,
            'time': self.start,
            'args': str([]),
            'kwargs': str({}),
            'error': str(exc_val)
        })


def telemetrize(identifier: str = 'anonymous-telemetrize-decorator'):
    def _telemetrize(function): 
        def _t(*args, **kwargs): 
            begin = time.time()
            error = None
            try:
                result = function(*args, **kwargs)
            except Exception as e:
                error = e
                raise e
            finally:
                end = time.time()
                send_telemetry({
                    'eventid': str(uuid.uuid4()),
                    'telemetryid': identifier,
                    'runtime': end - begin,
                    'time': begin,
                    'args': str([_ for _ in args]),
                    'kwargs': str({k: v for k, v in kwargs.items()}),
                    'error': str(error)
                })
            return result
        return _t 
    return _telemetrize


def send_telemetry(message: dict):
    """
    Ping a server/Write to a file or print.
    Uses whatever OPERATION is currently defined to be.
    """
    Thread(target=OPERATION, args=({**message, **META},)).start()


def write_to_csv(message: dict, location: str = 'telemetry.csv'):
    """
    Write the payload to a csv table.
    """
    try:
        if not os.path.isfile(location):
            with open(location, "a", newline='') as handle:
                csvhandle = csv.writer(
                    handle, 
                    delimiter=',', 
                    quotechar='"', 
                    quoting=csv.QUOTE_MINIMAL
                )
                csvhandle.writerow(message.keys())

        with open(location, "a", newline='') as handle:
            csvhandle = csv.writer(
                handle, 
                delimiter=',', 
                quotechar='"', 
                quoting=csv.QUOTE_MINIMAL
            )
            csvhandle.writerow(message.values())

    except IOError:
        pass


def ping_server(message: dict, target: str):
    print(message)
    message['kwargs'] = str(message['kwargs'])
    print(requests.post(target, data=message))

if __name__ == "__main__":
    print("Show casing an example")
    
    @telemetrize('add')
    def add(a, b):
        c = a
        for i in range(200):
            c += a + b

    @telemetrize('sub')
    def sub(a, b):
        time.sleep(0.01)
        return a + b

    @telemetrize('sometimes-broken')
    def whatthe(a, b):
        time.sleep(0.05)
        return a + ', hello' + b

    OPERATION = write_to_csv

    with TimeProfiler('weird-multiplies'):
        235 * 432
        235 * 432
        235 * 432
        time.sleep(0.1)
        235 ** 432

    add(1, 2)
    add('a', 'b')
    sub(1, 2)
    sub(82, 3)
    try:
        whatthe(902, 5)
    except:
        pass

    def payload():
        add(time.time(), time.time())
        add('a', f'{time.time()}')
        sub(1, time.time())
        sub(time.time(), 3)

    loop_until = time.time() + 5
    max_threads = 8
    pool = []
    while time.time() < loop_until:
        for thread in range(max_threads):
            t = Thread(target=payload)
            t.start()
            pool.append(t)
        for thread in pool:
            thread.join()

    with TimeProfiler('just-throw-an-exception'):
        raise ValueError()