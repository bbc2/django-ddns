import bind_settings
import subprocess

def update(host, ip_address):
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
    
    return (err == '')
