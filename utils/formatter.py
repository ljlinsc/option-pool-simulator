def get_dollar_str(value: float) -> str:
    if value < 0:
        dollar_str = "-"
    else:
        dollar_str = ""
    dollar_str += "$%.2f" % (value.__abs__())
    return dollar_str
