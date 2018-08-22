from activity_index_client import SingleActivityApi, MultipleActivitiesApi
from activity_index_client.models import LearningActivity
from time import time

class memoize(object):
    '''
    Modified from django.utils.functional.memoize to add cache expiry.

    Wrap a function so that results for any argument tuple are stored in
    'cache'. Note that the args to the function must be usable as dictionary
    keys. Only cache results younger than expiry_time (seconds) will be returned.

    Only the first num_args are considered when creating the key.
    '''

    def __init__(self, expires=0):
        self.expires_sec = expires

    def __call__(self, func):
        def wrapped(*args, **kwargs):
            obj = args[0]
            key = (func, args[1:], frozenset(kwargs.items()))

            # Check the cache
            try:
                cache = obj.__cache
            except AttributeError:
                cache = obj.__cache = dict()

            if not ('force_update' in kwargs and kwargs['force_update'] == True):
                if key in cache:
                    result, timestamp = cache[key]
                    # Check the age.
                    age = time() - timestamp
                    if self.expires_sec <= 0 or age < self.expires_sec:
                        return result
            # Get a new result
            result = func(*args)
            # Cache it
            cache[key] = (result, time())
            # and return it.
            return result

        return wrapped

class CachedMultipleActivitiesApi(object):
    def __init__(self, base_url):
        self.activities_api = MultipleActivitiesApi()
        self.activities_api.api_client.configuration.host = base_url

    @memoize(expires=5*60)
    def get_activities(self, *args, **kwargs):
        return self.activities_api.get_activities(*args, **kwargs)

    @memoize(expires=5*60)
    def get_activities_with_http_info(self, *args, **kwargs):
        return self.activities_api.get_activities_with_http_info(*args, **kwargs)

class CachedSingleActivityApi(object):
    def __init__(self, base_url):
        self.activities_api = SingleActivityApi()
        self.activities_api.api_client.configuration.host = base_url

    def delete_activity(self, *args, **kwargs):  # noqa: E501
        return self.activities_api.delete_activity(*args, **kwargs)

    def delete_activity_with_http_info(self, *args, **kwargs):  # noqa: E501
        return self.activities_api.delete_activity_with_http_info(*args, **kwargs)

    @memoize(expires=5*60)
    def get_activity(self, *args, **kwargs) -> LearningActivity: # noqa: E501
        return self.activities_api.get_activity(*args, **kwargs)

    @memoize(expires=5*60)
    def get_activity_with_http_info(self, *args, **kwargs):  # noqa: E501
        return self.activities_api.get_activity_with_http_info(*args, **kwargs)

    def post_activity(self, *args, **kwargs):  # noqa: E501
        return self.activities_api.post_activity(*args, **kwargs)

    def post_activity_with_http_info(self, *args, **kwargs):  # noqa: E501
        return self.activities_api.post_activity_with_http_info(*args, **kwargs)

    def update_activity(self, *args, **kwargs):  # noqa: E501
        return self.activities_api.update_activity(*args, **kwargs)

    def update_activity_with_http_info(self, *args, **kwargs):  # noqa: E501
        return self.activities_api.update_activity_with_http_info(*args, **kwargs)
