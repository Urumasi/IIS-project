from flask import current_app
from flask_login import current_user
from functools import wraps

def admin_required(func):
    '''
        @app.route('/admin')
        @admin_required
        def admin():
            pass
    :param func: The view function to decorate.
    :type func: function
    '''
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif (not current_user.is_authenticated) or (not current_user.is_active) or (not current_user.is_admin):
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view
