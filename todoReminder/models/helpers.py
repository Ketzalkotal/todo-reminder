def errorOnNone(fun):
    def helper(*args, **kwargs):
        returnVal = fun(*args, **kwargs)
        if returnVal == None:
            raise ValueError("Function {} returns None".format(fun))
        return returnVal
    return helper
