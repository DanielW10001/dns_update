"""Periodically Update DDNS to Local Public IP"""

__author__ = 'Daniel (danielw10001@gmail.com)'
__version__ = '0.1.0'

import requests
import argparse
import re
import time


args = argparse.Namespace()
parser = argparse.ArgumentParser(description="Periodically Update DDNS to Local Public IP")
parser.add_argument('host')
parser.add_argument('domain')
parser.add_argument('password', help='Dynamic DNS API Password')
parser.add_argument('proxy')
parser.parse_args(namespace=args)


class APIError(RuntimeError):
    pass


last_ip = ''
while True:
    # Get local pulic IP
    while True:
        err_count = 0
        try:
            response_json = requests.get('http://ip-api.com/json/?fields=status,query', proxies={'http': args.proxy}, timeout=10).json()
            if response_json['status'] != 'success':
                raise APIError(f'status: {response_json["status"]}')
            ip = response_json['query']
        except (ValueError, KeyError, requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.Timeout, APIError):
            if err_count > 5:
                del ip
                raise
            else:
                err_count += 1
        else:
            break

    # Update IP
    if ip != last_ip:
        while True:
            err_count = 0
            try:
                response = requests.get(f'https://dynamicdns.park-your-domain.com/update?host={args.host}&domain={args.domain}&password={args.password}&ip={ip}', proxies={'https': args.proxy}, timeout=10)
                response.raise_for_status()
                if not re.search(r'\<ErrCount\>0\<\/ErrCount\>.*\<Done\>true\<\/Done\>', response.text):
                    raise APIError(f'DDNS Response: {response.text}')
            except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.Timeout, APIError):
                if err_count > 5:
                    raise
                else:
                    err_count += 1
            else:
                last_ip = ip
                break
        time.sleep(30)
    else:
        time.sleep(15*60)
