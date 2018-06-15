# subdomains module by CantSayIHave
# created 2018/3/10
#
# houses subdomain handler classes


import http

from subdomains.bot import SubdomainBOT
from subdomains.cdn import SubdomainCDN
from subdomains.rss import SubdomainRSS

from old_subdomains.www import SubdomainWWW
from request import Request


def get_subdomain_handler(request: Request, socket):
    sd = request.subdomain

    if sd == 'www' or sd == '':
        return SubdomainWWW(request, socket)
    elif sd == 'bot':
        return SubdomainBOT(request, socket)
    elif sd == 'rss':
        return SubdomainRSS(request, socket)
    elif sd == 'cdn':
        return SubdomainCDN(request, socket)
    else:
        return SubdomainDNE(request, socket)


class SubdomainDNE:
    def __init__(self, request, socket):
        self.request = request
        self.socket = socket

    def handle(self):
        raise http.SubdomainNotFoundError('Subdomain does not exist')

