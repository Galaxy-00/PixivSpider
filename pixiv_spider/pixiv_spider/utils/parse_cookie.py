def parse_cookie(cookie_str):
    cookie = {}
    for line in cookie_str.split(';'):
        key, value = line.split('=', 1)
        cookie[key] = value
    return cookie