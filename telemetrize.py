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

META = {
    'runid': str(uuid.uuid4()),
    'pwd': os.getcwd(),
    'path': os.getenv('PATH'),
    'executable': sys.executable,
    'ver': sys.version,
    'host': socket.gethostname(),
    'user': getpass.getuser()
}

class TimeProfiler:

    def __init__(self, identifier: str = 'anonymous-time-profiler'):
        self.identifier = identifier

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, ec_val, exc_tb):
        end = time.time()
        total_time = end - self.start
        send_telemetry({
            'telemetryid': self.identifier,
            'runtime': total_time,
            'time': self.start,
            'args': str([]),
            'kwargs': str({})
        })


def telemetrize(identifier: str = 'anonymous-telemetrize-decorator'):
    def _telemetrize(function): 
        def _t(*args, **kwargs): 
            begin = time.time()
            try:
                result = function(*args, **kwargs)
            except Exception as e:
                raise e
            end = time.time()
            send_telemetry({
                'telemetryid': identifier,
                'runtime': end - begin,
                'time': begin,
                'args': [str(_) for _ in args],
                'kwargs': {k: str(v) for k, v in kwargs.items()},
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
        return a + b

    @telemetrize('sub')
    def sub(a, b):
        time.sleep(0.01)
        return a + b

    OPERATION = lambda message: ping_server(message, 'http://127.0.0.1:8000/endpoint/')

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
