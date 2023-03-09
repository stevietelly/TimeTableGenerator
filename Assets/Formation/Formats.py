valid_outputs = ["json", "html", "excel", "csv"]

def is_valid_formart(form:str):
    if form in valid_outputs:
        return True
    return False