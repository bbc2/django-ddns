import sys
import dyndns.settings as settings

ARG_NOCHG = 'NOCHG'
ARG_YES = 'YES'

CODE_BADAUTH = 'badauth'
CODE_NOT_DONATOR = '!donator'
CODE_GOOD = 'good'
CODE_NOCHG = 'nochg'
CODE_NOTFQDN = 'notfqdn'
CODE_NOHOST = 'nohost'
CODE_NUMHOST = 'numhost'
CODE_ABUSE = 'abuse'
CODE_BADAGENT = 'badagent'
CODE_DNSERR = 'dnserr'
CODE_911 = '911'

def is_ip_address(ip_address):
    """Validate IPv4 or IPv6 address"""
    from IPy import IP
    try:
        IP(ip_address)
    except ValueError:
        return False
    return True

def process(hostnames, ip_address):
    """
    Process hostnames, update their associated IP address and return codes.

    "Each hostname specified will be updated with the same information, and the
    return codes will be given one per line, in the same order as given."

    "hostname: Comma separated list of hostnames that you wish to update
    (up to 20 hostnames per request)"

    "myip: IP address to set for the update."
    """
    if hostnames == []:
        # "If no hostnames were specified, notfqdn will be returned once."
        return [{ 'code': CODE_NOTFQDN, 'ip': '' }]
    if len(hostnames) > 20:
        # "numhost: Too many hosts (more than 20) specified in an update. Also
        # returned if trying to update a round robin (which is not allowed)."
        return [{ 'code': CODE_NUMHOST, 'ip': '' }]
        
    processed = []
    sys.path.append(settings.UPDATERS_DIR)

    try:
        for host in hostnames:
            processed.append(_process_host(host, ip_address, settings.HOST_UPDATERS))
    finally:
        # Make sure sys.path does not grow even if an exception was raised
        sys.path.pop()

    return processed

def _process_host(host, ip_address, updaters):
    if host == '':
        # "notfqdn: The hostname specified is not a fully-qualified domain name
        # (not in the form hostname.dyndns.org or domain.com)."
        return { 'code': CODE_NOTFQDN, 'ip': '' }
    if host not in settings.HOSTNAMES:
        # "nohost: The hostname specified does not exist in this user account
        # (or is not in the service specified in the system parameter)."
        return { 'code': CODE_NOHOST, 'ip': '' }

    from importlib import import_module
    for name in updaters:
        updater = import_module(name)
        if updater.update(host, ip_address):
            return { 'code': CODE_GOOD, 'ip': ip_address }
        else:
            return { 'code': CODE_911, 'ip': ip_address }

def format(lines):
    """Format host lines"""
    return '\n'.join(["%s %s" % (line['code'], line['ip']) for line in lines])
