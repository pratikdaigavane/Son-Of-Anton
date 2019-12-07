
class LogRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'logger':
            return 'logger'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'logger':
            return 'logger'
        return None

    def allow_syncdb(self, db, model):
        if db == 'logger':
            return model._meta.app_label == 'logger'
        elif model._meta.app_label == 'logger':
            return False
        return None
