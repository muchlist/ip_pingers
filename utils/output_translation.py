def output_error(err: str):
    if err == "b''":
        return False
    return True

def output_success(msg: str):
    if "100%" in msg:
        return "DOWN"
    elif "50%" in msg:
        return "DOWN/UP"
    elif "0%" in msg:
        return "UP"
    return "DOWN" 