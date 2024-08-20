def register_blueprints(app):
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from .menu import menu as menu_blueprint
    app.register_blueprint(menu_blueprint)
    
    from .mission import mission as mission_blueprint
    app.register_blueprint(mission_blueprint)

    from .param import param as param_blueprint
    app.register_blueprint(param_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    from .compil import compil as compil_blueprint
    app.register_blueprint(compil_blueprint)

    from .edition import edition as edition_blueprint
    app.register_blueprint(edition_blueprint)

    from .profils import profils as profils_blueprint
    app.register_blueprint(profils_blueprint)
