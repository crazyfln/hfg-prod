import re
import datetime
import time
import string
import random
from django.core.urlresolvers import reverse



def file_url(category):
    def inner(instance, filename):
        r = re.compile(r'[^\S]')
        filename = r.sub('', filename)
        now = datetime.datetime.now()
        timestamp = int(time.time())
        return 'uploads/{0}/{1.year:04}/{1.month:02}/{1.day:02}/{2}/{3}'.format( \
                category, now, timestamp, filename)
    return inner

def random_string(length):
    alphanumeric = string.letters + string.digits
    return "".join(random.choice(alphanumeric) for i in range(length))

def list_button(self, obj, page, button_display, get_arguments=None): 
    info = self.admin_site.name, obj._meta.app_label, obj._meta.module_name, page 
    url = reverse('{0}:{1}_{2}_{3}'.format(*info), args=(obj.id,)) 
    return "<a href='{0}'>{1}</a>".format(url, button_display) 

