from hashlib import md5

from ipware.ip import get_ip, get_real_ip


def get_user_hash(request):
    return md5(get_real_ip(request) or get_ip(request)).hexdigest()
