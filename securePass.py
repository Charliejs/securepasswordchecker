import requests
import hashlib
import sys

try:
    with open('passdoc.txt', mode='r') as my_file:
        pass_code = my_file.readline()

except FileNotFoundError:
    print('File not Found!!!!')


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    chec_pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    five_char, tail = chec_pass[:5], chec_pass[5:]
    response = request_api_data(five_char)
    return get_password_leaks_count(response, tail)


def main():
    count = pwned_api_check(pass_code)

    if count:
        print(f'The password was found {count} times ...should be changed')
    else:
        print(f'The password not found. carry on')


if __name__ == '__main__':
    main()
