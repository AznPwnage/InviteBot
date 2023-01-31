def append_str_to_value_if_key_exists(d: dict, separator: str, k: str, value_to_append: str):
    if k in d.keys():
        v = d.get(k)
        v = v + separator + value_to_append
        d[k] = v
    else:
        d[k] = value_to_append


def append_obj_to_value_if_key_exists(d: dict, k: str, value_to_append):
    if k in d.keys():
        v = d.get(k)
        v.append(value_to_append)
        d[k] = v
    else:
        d[k] = [value_to_append]
