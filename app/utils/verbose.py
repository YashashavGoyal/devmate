def vprint(message: str, verbose: bool = False, fn=None, **kwargs): 
    if verbose:
        if fn:
            fn(message, **kwargs)
        else:
            print(message)
