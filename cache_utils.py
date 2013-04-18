import os
import cPickle as pickle
from cmd_utils import log


mem_caches = dict()


def cache_del(cache_name, cache_key):
    if cache_name not in mem_caches:
        cache_get(cache_name, cache_key)
    if cache_key in mem_caches[cache_name]:
        del mem_caches[cache_name][cache_key]
        _write_cache(cache_name)
        return True
    else:
        return False


def cache_get(cache_name, cache_key):
    if cache_name not in mem_caches:

        file_name = cache_name + '.data'
        file_path = os.path.join('cache', file_name)
        file_mode = "rb" if os.path.isfile(file_path) else "wb"
        f = open(file_path, file_mode)
        try:
            data = pickle.load(f)
        except (IOError, EOFError):
            data = dict()
        mem_caches[cache_name] = data
        f.close()

    try:
        rs = mem_caches[cache_name][cache_key]
        log('Cache Hit: %s[%s]' % (cache_name, cache_key), 5)
        return rs
    except KeyError:
        return None


def cache_set(cache_name, cache_key, cache_value):

    if cache_name not in mem_caches:
        cache_get(cache_name, cache_key)

    mem_caches[cache_name][cache_key] = cache_value
    _write_cache(cache_name)


def _write_cache(cache_name):
    file_name = cache_name + '.data'
    f_write = open(os.path.join('cache', file_name), 'wb')
    pickle.dump(mem_caches[cache_name], f_write)
    f_write.close()


if __name__ == "__main__":
    from cmd_utils import cmd_arg
    cache_key = cmd_arg('--key', None)
    cache_name = cmd_arg('--name', None)
    if cache_key and cache_name:
        cache_del(cache_name, cache_key)
