from django.http import HttpResponse
import libdyn

def update(request):
    # "If the IP address passed to the system is not properly formed, it will be
    # ignored and the system's best guess will be used."
    default_address = request.META['REMOTE_ADDR']
    ip_address = request.GET.get('myip', default_address)
    if not libdyn.is_ip_address(ip_address):
        ip_address = default_address
        
    hostnames = request.GET.get('hostname', '').split(',')
    hostnames.reverse()

    codes = libdyn.process(hostnames, ip_address)

    return HttpResponse(libdyn.format(codes), content_type='text')
