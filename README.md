# JSON Handler

It's easy-to-use library which helps you to work with data in JSON files and Python dictionaries like if they were Python objects.

## Examples

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
handler.sub_field = [1, 2, 3]

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
