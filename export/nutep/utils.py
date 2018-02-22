from urlparse import urlparse

from django.http import QueryDict
from django.utils.encoding import iri_to_uri
from django.utils.timezone import now


def next_url(full_path, keys_to_delete=None):
    q = QueryDict('', mutable=True)
    nexturl = urlparse(full_path).path
    next_query = iri_to_uri(urlparse(full_path).query)
    next_query_dict = None
    if next_query:
        deleted_keys = []
        next_query_dict = QueryDict(next_query).copy()
        if keys_to_delete:
            deleted_keys.extend(keys_to_delete)
        for k, v in next_query_dict.iteritems():            
            if not v:
                deleted_keys.append(k)
        for key in deleted_keys:
            if key in next_query_dict:
                del[next_query_dict[key]]
    params = '?%s' % next_query_dict.urlencode() if next_query_dict else ''
    q['next'] = '%s%s' % (nexturl, params)
    return q.urlencode()


def is_user_valid(user):
    if user.is_superuser:
        return False
    if not user.profile:
        return False
    if user.profile.valid_till < now():
        return False
    return True