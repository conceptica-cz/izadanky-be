def get_func_from_path(dotted_path):
    module_name, func_name = dotted_path.rsplit(".", 1)
    module = __import__(module_name, fromlist=[func_name])
    return getattr(module, func_name)
