import bind_settings
import subprocess
import pickledb

OK = 'ok'
SAME = 'same'
ERROR = 'error'

def update(host, ip_address):
    db = pickledb.load('address.db', True)
    if not db.get(host):
        db.set(host, ip_address)
    elif db.get(host) == ip_address:
        return SAME
    db.set(host, ip_address)

    update_str = """
        zone %(domain)s
        update delete %(host)s A
        update add %(host)s 300 A %(ip)s
        send
        quit
    """ % { 'domain': 'dyn.bbc.re', 'host': host, 'ip': ip_address }
    p = subprocess.Popen(['/usr/bin/nsupdate', '-k', bind_settings.KEY_FILE],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    (out, err) = p.communicate(input=update_str)
    
    return (err == '') and OK or ERROR
