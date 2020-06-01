from django import template
register = template.Library()

@register.filter(name='times') 
def times(number):
    return range(number)

@register.filter
def index(i):
    #for x in range(0,19):
        
    return range(i)