import pendulum
import urllib.parse

# return true/false if a value matches a dictionary[key] value
def condition_equal(dict, k, v):
    return dict[k] == v


# return true/false if a value is contained in a dictionary[key] value
def condition_contains(dict, k, v):
    return v in dict[k]


# return true/false if a value is an integer
def check_int(s):
    s = str(s)
    if len(s) > 0:
        if s[0] in ("-", "+"):
            return s[1:].isdigit()
        return s.isdigit()
    return False


# return true/false if a value is an date
def check_date(s):
    try:
        pendulum.parse(s)
        return True
    except pendulum.parsing.exceptions.ParserError:
        return False
    # the following catch-all except is needed at the moment as there
    # are a LOT of different exceptions I was running into ... _sigh_
    except:
        return False


def types_lod(fields, data):
    """
    purpose:
      to search through a list of dictionaries and determine the actual
      data type of the values.
      currently only 'date', 'string' and 'int' are determined, default
      type falls back to 'string'
    input:
      - fields = list of field names
      - data = list of dictionaries
    output:
      - dictionary
        key = field_name
        - dictionary
          key 'type', values ('string', 'int', 'date')
          key 'len', length of string or 0 if not a string
    """
    field_types = dict()
    for key in fields:
        key_values = [sub[key] for sub in data]

        # check if all values the same
        # note: right now they are all 'str' so this section turned out to be not
        #       very useful
        # ivalues = iter(key_values)
        # first_type = type(next(ivalues))
        # all_same = (
        #     first_type
        #     if all((type(x) is first_type) for x in ivalues)
        #     else False
        # )

        # check for int
        ivalues = iter(key_values)
        first_int = check_int(next(ivalues))
        same_int = (
            first_int
            if all((check_int(x) == first_int) for x in ivalues)
            else False
        )

        # check for date
        ivalues = iter(key_values)
        first_date = check_date(next(ivalues))
        same_date = (
            first_date
            if all((check_date(x) == first_date) for x in ivalues)
            else False
        )

        item_dict = dict()
        if first_int and same_int:
            item_dict.setdefault("type", "int")
            item_dict.setdefault("len", 0)
            field_types.setdefault(key, item_dict)
        elif first_date and same_date:
            item_dict.setdefault("type", "date")
            item_dict.setdefault("len", 0)
            field_types.setdefault(key, item_dict)
        else:
            item_dict.setdefault("type", "string")
            item_dict.setdefault("len", max(len(x) for x in key_values))
            field_types.setdefault(key, item_dict)

    return field_types


def filter_lod(request_items, fields, data, types):
    """
    purpose:
      to filter a list of dictionaries based on the request.GET items
    input:
      - request_items = request.GET dictionary
      - fields = list of field names
      - data = list of dictionaries
      - types = dictionary of field types
    output:
      - filtered list of dictionaries
    """
    filtered = data
    request_items = request_items
    for key in request_items.keys():
        if "_unselected_" not in request_items[key]:
            if key in fields:
                if types[key]["type"] == "string" and types[key]["len"] > 50:
                    filtered = [
                        d
                        for d in filtered
                        if condition_contains(d, key, request_items[key])
                    ]
                elif types[key]["type"] == "int":
                    filtered = [
                        d
                        for d in filtered
                        if condition_equal(d, key, int(request_items[key]))
                    ]
                else:
                    filtered = [
                        d
                        for d in filtered
                        if condition_equal(d, key, request_items[key])
                    ]

    return filtered


def form_lod(request_items, fields, data, types):
    """
    purpose:
      to generate HTML for an HTML FORM based on the fields and request.GET terms
    input:
      - request_items = request.GET dictionary
      - fields = list of field names
      - data = list of dictionaries
      - types = dictionary of field types
    output:
      - list of form elements as strings
    """
    form_data = list()
    ri = request_items.dict()
    for field in fields:
        if field not in ["result_id_id", "rowid"]:
            # print(ri.get(field))
            if types[field]["type"] == "string" and types[field]["len"] > 50:
                if len(ri.get(field, "")) > 0:
                    form_html = f'<label for="id_{field}">{field}:</label><input type="text" class="form-control" name="{field}" id="id_{field}" value="{ri.get(field)}">'
                else:
                    form_html = f'<label for="id_{field}">{field}:</label><input type="text" class="form-control" name="{field}" id="id_{field}">'
            elif types[field]["type"] == "date":
                form_html = ""
            else:
                form_html = f'<label for="id_{field}">{field}:</label><select class="form-control" name="{field}" id="id_{field}">'
                if field in ri.keys() and "_unselected_" in ri.get(field, ""):
                    form_html += f'<option value="_unselected_ selected">--------</option>'
                else:
                    form_html += (
                        f'<option value="_unselected_">--------</option>'
                    )
                values_dict = dict()
                for datum in data:
                    values_dict.setdefault(datum[field], 1)
                for value in list(values_dict.keys()):
                    if field in ri.keys() and ri.get(field, "") == value:
                        form_html += f'<option value="{value}" selected>{value}</option>'
                    else:
                        form_html += (
                            f'<option value="{value}">{value}</option>'
                        )
                form_html += "</select>"
            if len(form_html) > 0:
                item_dict = dict()
                item_dict.setdefault(field, form_html)
                form_data.append(item_dict)

    return form_data
