def seconds_to_str(seconds: int) -> str:
    """The function should return a text representation of the time."""
    time_ = {
        "d": 3600 * 24,
        "h": 60 * 60,
        "m": 60,
        "s": 1,
    }
    if not seconds:
        return "00:00"
    result = {}
    for name, value in time_.items():
        if res := seconds // value:
            result[name] = f"{res:0>2}"
            seconds -= res * value
        elif result:
            result[name] = "00"
    return result.get("h", "00") + ":" + result.get("m", "00")
