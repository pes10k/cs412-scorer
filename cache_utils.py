import os
import cPickle as pickle


mem_caches = dict()


def cache_get(cache_name, cache_key):
    if cache_name not in mem_caches:

        file_name = cache_name + '.data'
        file_path = os.path.join('cache', file_name)
        file_mode = "rb" if os.path.isfile(file_path) else "wb"
        f = open(file_path, file_mode)
        try:
            data = pickle.load(f)
        except (IOError, EOFError) as e:
            print e
            data = dict()
        mem_caches[cache_name] = data
        f.close()

    try:
        return mem_caches[cache_name][cache_key]
    except KeyError:
        return None


def cache_set(cache_name, cache_key, cache_value):

    file_name = cache_name + '.data'

    if cache_name not in mem_caches:
        cache_get(cache_name, cache_key)

    mem_caches[cache_name][cache_key] = cache_value
    f_write = open(os.path.join('cache', file_name), 'wb')
    pickle.dump(mem_caches[cache_name], f_write)
    f_write.close()
