# LockAccrossMachine

A lock accross machine for a distributed system using aerospike.

#Installation
Override the config according to your system
By default it is
```json
{
    "hosts": [("127.0.0.1", 3000)]
}
```
We have to register the udf to use this module
```python
from aerospike import client
client.udf_put("atomicity.lua")
```