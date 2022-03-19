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

def getStatusFilePathByUsername(instance,filename):
    # file would be saved to MEDIA_ROOT/username/status_images/filename
    return "{}/status_images/{}".format(instance.status_entry.user.username,filename)
def getUserAppDataDirectory(username):
    pass