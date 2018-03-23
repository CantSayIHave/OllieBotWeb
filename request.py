# request module by CantSayIHave
# created 2018/3/10
#
# request class breaks apart http request


from globals import *


class Request:
    def __init__(self, raw_text: str):
        self.raw = raw_text
        self.type = raw_text[:raw_text.find(' ')]  # GET, POST, etc
        self.query = http_pull_tag(self.type, raw_text, dl1='/', dl2=' HTTP')

        self.subdomain = http_pull_tag('Host', raw_text).split(DOMAIN_NAME)[0].replace('.', '')
        self.connection = http_pull_tag('Connection', raw_text)
        self.accept = http_pull_tag('Accept', raw_text)
        self.referer = http_pull_tag('Referer', raw_text)


