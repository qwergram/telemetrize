# Telemetrize

Simple python library that telemetrizes your functions. It's as easy as:

```py
from telemetrize import telemetrize, OPERATION
OPERATION = lambda message: ping_server(message, 'http://127.0.0.1:8000/endpoint/')


@telemetrize('add')
def add(a, b):
    return a + b

@telemetrize('sub')
def sub(a, b):
    time.sleep(0.01)
    return a + b


add(1, 2)
```

Will then push payloads to the django server, and are accessible by the django
dashboard. 

![](https://media.discordapp.net/attachments/636989395853115403/750951448061149244/unknown.png)

Other options include writing to a csv file or printing to a log.
Only records timing information.