# Repo: filter_lods

## Summary
This repo consists of code to filter a list of dictionaries and other supporting utility functions.

In various Django projects, I have had the need to display and filter data that did not come from a Model but was either a) derived from a Model or created by some other means.  Mostly this takes the form of a list of dictionaries, as:

```
lod = [ { "a": 1, "b": "abc", "c": "2020-01-01" }, { "a": 2, "b": "abc", "c": "2020-01-02" } ]
```

In working with Django there are 2 main needs:

1. display the data in a table (which I have handled by usinng a dynamic table class with `django_tables2`)
1. filter the data based on a search form with various drop-downs and text input boxes

Here are three functions here that will help with this:

- types_lod() = determine data types of the "columns"
- filter_lod() = filter the lod based on search terms
- form_lod() = create the FORM HTML strings for each "column"

## types_lod()

This function searches through a list of dictionaries and determine the actual data type of the values.

Currently only 'date', 'string' and 'int' are determined with the default default type being 'string'.

### input

- fields = list of field names
- data = list of dictionaries

### output:
dictionary:
- key = field_name

    dictionary:
    - key 'type', values ('string', 'int', 'date')
    - key 'len', length of string or 0 if not a string

### Example:

```
>>> from filters import *
>>> lod = [ { "a": 1, "b": "abc", "c": "2020-01-01" }, { "a": 2, "b": "abc", "c": "2020-01-02" } ]
>>> fields = [k for k in lod[0].keys()]
>>> lod_types = types_lod(fields, lod)
>>> lod
[{'a': 1, 'b': 'abc', 'c': '2020-01-01'}, {'a': 2, 'b': 'abc', 'c': '2020-01-02'}]
>>> fields
['a', 'b', 'c']
>>> lod_types
{'a': {'type': 'int', 'len': 0}, 'b': {'type': 'string', 'len': 3}, 'c': {'type': 'date', 'len': 0}}
>>>
```

## filter_lod()

This function takes a list of dictionaries and filters out non-matching rows basied on an onput dictionary.

### input:

- request_items = request.GET dictionary
- fields = list of field names
- data = list of dictionaries
- types = dictionary of field types

### output:

- filtered list of dictionaries

### Example:

```
>>> from filters import *
>>> lod = [ { "a": 1, "b": "abc", "c": "2020-01-01" }, { "a": 2, "b": "abc", "c": "2020-01-02" } ]
>>> fields = [k for k in lod[0].keys()]
>>> # this would be the result of request_dict = request.GET.dict()
>>> request_dict = {'page': '1', 'a': '1', 'b': '_unselected_', 'c': '_unselected_'}
>>> filtered_lod = filter_lod(request_dict, fields, lod, lod_types)
>>> lod
[{'a': 1, 'b': 'abc', 'c': '2020-01-01'}, {'a': 2, 'b': 'abc', 'c': '2020-01-02'}]
>>> filtered_lod
[{'a': 1, 'b': 'abc', 'c': '2020-01-01'}]
>>>
```

## form_lod()

This function takes a list of dictionaries and produces HTML FORM strings for use in a django template to create the "search" form on a page.

### input:

- request_items = request.GET dictionary
- fields = list of field names
- data = list of dictionaries
- types = dictionary of field types
- exclude_fields = list of field names to exclude from the output

### output:

- list of form elements as strings

### Example:

```
>>> from filters import *
>>> lod = [ { "a": 1, "b": "abc", "c": "2020-01-01" }, { "a": 2, "b": "abc", "c": "2020-01-02" } ]
>>> fields = [k for k in lod[0].keys()]
>>> # this would be the result of request_dict = request.GET.dict()
>>> request_dict = {'page': '1', 'a': '1', 'b': '_unselected_', 'c': '_unselected_'}
>>> form_data = form_lod(request_dict, fields, lod, lod_types, [])
>>> form_data
[{'a': '<label for="id_a">a:</label><select class="form-control" name="a" id="id_a"><option value="_unselected_">--------</option><option value="1">1</option><option value="2">2</option></select>'}, {'b': '<label for="id_b">b:</label><select class="form-control" name="b" id="id_b"><option value="_unselected_ selected">--------</option><option value="abc">abc</option></select>'}]
>>>
```
