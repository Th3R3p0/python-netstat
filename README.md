## Python module for returning netstat like results

```python
import netstat

netstat.netstat()
netstat.only_listening()
```

Currently the formatting for IPv6 addresses is not displaying correctly

The original source code is from http://voorloopnul.com/blog/a-python-netstat-in-less-than-100-lines-of-code/

Modifications have been made to add support for TCP6 and filtering. More to be added in the future
