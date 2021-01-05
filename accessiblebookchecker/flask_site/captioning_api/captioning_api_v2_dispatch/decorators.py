import functools


def check_error(func):

    @functools.wraps(func)
    def wrapper_check_error(*args, **kwargs):
        if args[0].request_object.error is None:
            return func(*args, **kwargs)
        else:
            args[0].error_response()
            return func(*args, **kwargs)
    return wrapper_check_error





