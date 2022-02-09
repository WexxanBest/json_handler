# JSON Handler

It's easy-to-use library which helps you to work with data in JSON files and Python dictionaries like if they were Python objects.

## Installation

```commandline
pip install json_handler
```
No dependencies!
## Getting Started

### Example 1. 

You can easily read existing JSON file and modify it. Here is JSON file (example.json): 

```json
{
    "field_1": "Hi",
    "field_2": "Hello world!",
    "field_3": {
        "sub_field": 123
    }
}
```

We can modify the content of that by using following code:

```python
from json_handler import JsonHandler

handler = JsonHandler('example.json')

handler.field_1 = 123
handler['field_2'] = "What's up?"
handler.field_3 = {}
handler.field_3.sub_field = [1, 2, 3]

handler.save()
```

The result of modifications will be (example.json):
```json
{
    "field_1": 123,
    "field_2": "What's up?",
    "field_3": {
        "sub_field": [1, 2, 3]
    }
}
```

### Example 2.
If file does not exist, it will be automatically 
created if parameter _'auto_create'_ 
set to _True_.


```python
from json_handler import JsonHandler

handler = JsonHandler('example2.json', auto_create=True)

handler.a = 5
handler.b = 'Hi there'
handler.save()
```
In the same directory file _(example2.json)_ will be created with following content:

```json
{
  "a": 5,
  "b": "Hi there"
}
```

### Example 3.
There is way to automatically save all changes happening with data.
To do that you should just set parameter _'auto_save'_ to _True_.


```python
from json_handler import JsonHandler

handler = JsonHandler('example3.json', auto_create=True, auto_save=True)

handler.hi = 'Hello'
handler.five = 5
```

In the same directory file _(example3.json)_ will be created with following content :

```json
{
  "hi": "Hello",
  "five": 5
}
```

### Example 4.
You can use _Python built-in dict_ methods with JsonHandler object. For example:


```python
from json_handler import JsonHandler

handler = JsonHandler('example4.json', auto_create=True, auto_save=True)

handler.hi = 'Hello'
handler.five = 5
handler.sub_dict = {}
handler.sub_dict.fine = 'ok'

print(handler.keys())
print(handler.values())
print(handler.items())
```


The output will be:
```commandline
dict_keys(['hi', 'five', 'sub_dict'])
dict_values(['Hello', 5, {'fine': 'ok'}])
dict_items([('hi', 'Hello'), ('five', 5), ('sub_dict', {'fine': 'ok'})])
```

---
Also you can clear data by using _dict.clear()_ method:

```python
handler.clear()
print(handler)
```

The output will be:
```commandline
{}
```
Yeah, you can actually print _JsonHandler_ object and it will be printed
like usual _Python dict_

### Example 5.
You can pretty print your _JsonHandler_ object like any _dict_ object by using
built-in python module _pprint_.

```python
from pprint import pprint
from json_handler import JsonHandler


handler = JsonHandler('test.json')
handler.well = [{'hi': 'hello'} for _ in range(5)]

pprint(handler)
```

The output will be:
```json
{"well": [{"hi": "hello"},
          {"hi": "hello"},
          {"hi": "hello"},
          {"hi": "hello"},
          {"hi": "hello"}]}
```
P@wf#bnpkNbD9Qh