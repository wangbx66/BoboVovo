from os.path import join

import mandrill
import colorama
colorama.init()

def matchfile(s, mode='a'):
    webpage = s.webpage.replace('/', '$')
    return open(join('matches', webpage), mode)

def matchurl(s):
    return s.replace('$', '/')

def domain(s):
    return s.webpage.split('/')[2]

def lb(s):
    z = min([a for a in range(1, 3) if int(10**a * s) == 10**a * s])
    return s - 10**(-z)/2

def red(s):
    return(colorama.Fore.RED + s.__str__() + colorama.Fore.WHITE)

def mandrill(content='NO CONTENT', subject='NO SUBJECT', email_to = ['wangbx66@gmail.com']):
    client = mandrill.Mandrill('trD65wtdBM16dNDeW7iPVQ')
    message = {
    'from_email': 'message.wangbx66@gmail.com',
    'from_name': 'wangbxbot',
    'text': content,
    'subject': subject,
    'to': [{'email': x, 'type': 'to'} for x in email_to]}
    result = client.messages.send(message=message, async=False, ip_pool='Main Pool')
