import random, string
def generate_tracking_code():
    prefix = "BX"
    code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{prefix}-{code}"
