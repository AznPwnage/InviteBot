def append_to_value_if_key_exists(d: dict, separator: str, k: str, value_to_append: str):
    if k in d.keys():
        v = d.get(k)
        v = v + separator + value_to_append
        d[k] = v
    else:
        d[k] = value_to_append
