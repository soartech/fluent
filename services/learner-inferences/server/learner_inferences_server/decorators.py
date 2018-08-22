from learner_inferences_server.log_utils import print_with_time

# This decorator allows any store method to retry multiple times before raising exception.
# For details see https://dzone.com/articles/pymongo-pointers-how-to-make-robust-and-highly-ava-1
def retry_decorator(num_tries, exceptions):
    def decorator(func):
        def f_retry(*args, **kwargs):
            for i in range(num_tries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if i < (num_tries - 1):
                        print_with_time('WARN: Retrying call to store client after connection error: {0}.'.format(str(e)))
                        continue
                    else:
                        print_with_time('ERROR: Maxed out retries after connection error: {0}.'.format(str(e)))
                        raise
        return f_retry
    return decorator

