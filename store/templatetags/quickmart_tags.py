from django import template

register = template.Library()

@register.filter(name='currency')
def currency(value):
    """Formats float/decimal into Indian/standard comma separated with 2 decimals"""
    try:
        val = float(value)
        return f"{val:,.2f}"
    except (ValueError, TypeError):
        return "0.00"

@register.filter(name='format_date')
def format_date(value):
    """Formats datetime as %d-%b-%Y %I:%M %p"""
    if hasattr(value, 'strftime'):
        return value.strftime('%d-%b-%Y %I:%M %p')
    return value or ''
