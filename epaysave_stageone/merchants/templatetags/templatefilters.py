from django import template

register=template.Library()

@register.filter
def get_by_index(mylist, index):
    return mylist[index]

@register.filter
def get_by_key(mylist, key):
    return mylist[key]

@register.simple_tag(name='get_dict')
def get_dict(id_data, value, key):
    return id_data[value][key]

@register.simple_tag(takes_context=True)
def get_items(context):
    return context.items()

@register.filter
def multiply(value, arg):
    value=float(value)
    arg=float(arg)
    return value*arg