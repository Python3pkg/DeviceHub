from flask import request


def save_ip_of_request(prove_usages: list):
    for prove_usage in prove_usages:
        prove_usage['ip'] = request.remote_addr
