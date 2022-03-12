def hasLetterInString(value):
    for i in value:
        if str.isalpha(i):
            return True
    return False

def hasNumberInString(value):
    for i in value:
        if str.isdigit(i):
            return True
    return False