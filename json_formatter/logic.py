from collections import OrderedDict
import json


def format_json_stream(stream_in, stream_out, **kwargs):
    '''
    @param sort_keys
    @param compact: compact json, no spaces, no indent, no new-lines
    @param indent
    '''
    kwargs_load, kwargs_dump = _prep_params(kwargs)

    try:
        value = json.load(stream_in, **kwargs_load)
    except Exception as e:
        return e

    json.dump(value, stream_out, **kwargs_dump)


def format_json_str(json_str, **kwargs):
    '''
    @param sort_keys
    @param compact: compact json, no spaces, no indent, no new-lines
    @param indent
    '''
    kwargs_load, kwargs_dump = _prep_params(kwargs)

    try:
        value = json.loads(json_str, **kwargs_load)
    except Exception as e:
        return False, str(e)

    json_str = json.dumps(value, **kwargs_dump)
    return True, json_str


def _prep_params(kwargs):
    kwargs_load = {}
    kwargs_dump = {}
    if kwargs.pop('sort_keys', False):
        kwargs_dump['sort_keys'] = True
    else:
        kwargs_load['object_pairs_hook'] = OrderedDict

    if kwargs.pop('compact', False):
        kwargs_dump['separators'] = (',', ':')
    else:
        indent = kwargs.pop('indent', None)
        if indent is not None and indent >= 0:
            kwargs_dump['indent'] = indent
    return kwargs_load, kwargs_dump
