def exact_equal_string(first, second):
    if first.lower() == second.lower():
        return "success"
    else:
        return "failed"


def approx_equal_string(first, second):
    if first.lower() in second.lower():
        return "success"
    else:
        return "failed"


def head_equal_string(first, second):
    my_str1 = str(second)
    my_str2 = str(first)
    if my_str1.startswith(my_str2):
        return "success"
    else:
        return "failed"