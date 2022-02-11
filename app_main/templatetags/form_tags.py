from django import template

register = template.Library()


def get_label(a_dict, key):
    return getattr(a_dict.get(key), 'label', 'No label')


register.filter("get_label", get_label)
