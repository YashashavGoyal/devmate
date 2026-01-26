def vprint(verbose: bool, fn, message: str):
    if verbose:
        fn(message)
