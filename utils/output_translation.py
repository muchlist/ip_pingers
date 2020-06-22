def output_error(err_msg: str):
    if err_msg == "b''":
        return False
    return True


def output_success(msg: str, err_msg: str):

    if output_error(err_msg):
        return "ERROR"

    if "100%" in msg:
        return "DOWN"
    elif "87%" in msg:
        return "DOWN/UP"
    elif "75%" in msg:
        return "DOWN/UP"
    elif "62%" in msg:
        return "DOWN/UP"
    elif "50%" in msg:
        return "DOWN/UP"
    elif "37%" in msg:
        return "UP"
    elif "25%" in msg:
        return "UP"
    elif "12%" in msg:
        return "UP"
    elif "0%" in msg:
        return "UP"
    return "DOWN"
