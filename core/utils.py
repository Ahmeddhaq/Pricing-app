ADMIN_USERNAME = "Arshad al Haq"

def is_admin(user):
    return user.is_authenticated and user.username.lower() == ADMIN_USERNAME.lower()

def is_sales(user):
    return user.is_authenticated and (is_admin(user) or user.groups.filter(name='Sales').exists())

def is_production(user):
    return user.is_authenticated and (is_admin(user) or user.groups.filter(name='Production').exists())
