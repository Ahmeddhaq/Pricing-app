from .utils import is_admin, is_sales, is_production

def role_check(request):
    if not request.user.is_authenticated:
        return {
            'is_admin': False,
            'is_sales': False,
            'is_production': False,
        }
    return {
        'is_admin': is_admin(request.user),
        'is_sales': is_sales(request.user),
        'is_production': is_production(request.user),
    }
