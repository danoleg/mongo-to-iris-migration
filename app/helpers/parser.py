import datetime


def parse_dict(data: dict, path_list=None, res=None) -> list:
    """
    Recursive function which makes iris globals compatible data structure from dict

    :param data: dict, required field
    :param path_list:
    :param res:
    :return: list
    """
    if res is None:
        res = []
    if path_list is None:
        path_list = []
    if isinstance(data, dict):
        for key, value in data.items():

            if isinstance(value, list):
                i = 0
                for el in value:
                    path_part = [key, i]
                    if isinstance(el, dict):
                        parse_dict(el, path_list + path_part, res)
                    else:
                        if isinstance(el, (datetime.date, datetime.datetime)):
                            el = el.isoformat()
                        res.append({
                            "path_list": path_list + path_part,
                            "value": el
                        })
                    i += 1

            elif isinstance(value, dict):
                mod_path = path_list + [key]
                parse_dict(value, mod_path, res)

            else:
                mod_path = path_list + [key]
                if isinstance(value, (datetime.date, datetime.datetime)):
                    value = value.isoformat()
                res.append({
                    "path_list": mod_path,
                    "value": value
                })
    return res
