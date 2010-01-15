# tags.py
from django import template

register = template.Library()

@register.simple_tag
def active(request, pattern):
    """
    checks to see if current url matches given pattern and, if so, outputs 'active'.
    
    This is useful for giving a class of 'active' to a nav link so it can be styled accordingly.
    """
    import re
    if re.search("^/$", pattern):
        pattern = "%s%s%s" % ('^', pattern, '$') 
    if re.search(pattern, request.path):
	    return 'active'
    return ''

@register.simple_tag
def hashtag(tag):
    """
    prepends a # to a tag if it doesn't already have one.
    
    for some reason when using django-tagging you need to give
     tag.__unicode__ to this tag or else it throws an error.
    """
    import re
    if re.search("^#.*$", tag):
        return '%s' % tag
    return '#%s' % tag
    
    
# @register.simple_tag
# def is_negative(num):
#     """
#     prepends a # to a tag if it doesn't already have one.
# 
#     for some reason when using django-tagging you need to give
#      tag.__unicode__ to this tag or else it throws an error.
#     """
#     import re
#     if re.search("^-.*$", num):
#         return ' negative'

# @register.simple_tag
# def regex(pattern, value, output):
#     """
#     prepends a # to a tag if it doesn't already have one.
# 
#     for some reason when using django-tagging you need to give
#      tag.__unicode__ to this tag or else it throws an error.
#     """
#     import re
#     if re.search(patter, value):
#         return output

MOMENT = 120    # duration in seconds within which the time difference 
                # will be rendered as 'a moment ago'
@register.filter
def naturalTimeDifference(value):
    """
    Finds the difference between the datetime value given and now()
    and returns appropriate humanize form
    """

    from datetime import datetime, timedelta
    from pytz import timezone    
    import pytz 
    
    utc = pytz.utc
    hst = timezone('Pacific/Honolulu')

    if isinstance(value, datetime):
        value = value.replace(tzinfo=utc) + timedelta(minutes=30)
        now = datetime.now().replace(tzinfo=hst)
        delta = now - value
        # return "%s %s" % (datetime.now(), value)
        if delta.days > 6:
            return value.strftime("%b %d")                    # May 15
        if delta.days > 1:
            return value.strftime("%A")                       # Wednesday
        elif delta.days == 1:
            return 'yesterday'                                # yesterday
        elif delta.seconds >= 7200:
            return str(delta.seconds / 3600 ) + ' hours ago' # 3 hours ago
        elif delta.seconds >= 3600:
            return '1 hour ago' # 1 hour ago
        elif delta.seconds >  MOMENT:
            return str(delta.seconds/60) + ' minutes ago'     # 29 minutes ago
        else:
            return 'a moment ago'                             # a moment ago
        return defaultfilters.date(value)
    else:
        return str(value)