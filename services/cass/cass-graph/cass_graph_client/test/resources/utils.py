import pickle

import pkg_resources


def load_or_instantiate(package_name, klass, *args):
    resource_name = str(klass.__name__) + '_' + '_'.join(str(arg) for arg in args) + '.pkl'
    print(resource_name)
    if pkg_resources.resource_exists(package_name, resource_name):
        return pickle.load(pkg_resources.resource_stream(package_name, resource_name))
    return klass(*args)
