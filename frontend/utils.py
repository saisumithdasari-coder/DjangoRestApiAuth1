import os
import requests


def register_request(username, password):
    url = f'{get_base_url()}/register/'
    res = requests.post(url, data={'username': username, 'password': password})
    return res.json()


def login_request(username, password):
    url = f'{get_base_url()}/login/'
    res = requests.post(url, data={'username': username, 'password': password})
    return res.json()


def refresh_request(token):
    url = f'{get_base_url()}/refresh/'
    res = requests.post(url, data={'refresh_token': token})
    return res.json()


def revoke_request(token):
    url = f'{get_base_url()}/logout/'
    res = requests.post(url, headers={'token': token})
    return res.json()


def hello_world_request(token):
    url = f'{get_base_url()}/api/hello/'
    res = requests.get(url, headers={'Authorization': f'Bearer {token}'})
    return res.content


def get_host_and_port_for_service(service=""):
    services = {
        "backend": {
            "host": "BACKEND-SERVICE-HOST",
            "port": "BACKEND-SERVICE-PORT",
        },
    }
    host = os.getenv('{host}'.format(host=services[service]["host"]), '{service}'.format(service=service))
    port = os.getenv('{port}'.format(port=services[service]["port"]), '8000')
    return host, port


def get_base_url():
    host, port = get_host_and_port_for_service('backend')
    return f'http://{host}:{port}'
