# redis_decorator


```python
improt RS

rs = RS(host='localhost', port=6379, db=0, password='pass')
rs.connect()
>> (True, 'okay')

@rs.get_cache
def request(path, key=None):
    print(path)
    return  path + path
```

```python
# first run 
request('testcheck', key='rew')

# request-testcheck: [('key', 'rew')] 
# testcheck
>> testchecktestcheck
```

```python
# second run 
request('testcheck', key='rew')

>> '"testchecktestcheck"'
```
