from tinymce.widgets import TinyMCE

class SEOMixin(object):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('ft', ):
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 120, 'rows': 30},
            ))
        return super(SEOMixin, self).formfield_for_dbfield(db_field, **kwargs)

class HTMLDetailMixin(object):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name.startswith('detail'):
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 120, 'rows': 30},
            ))
        return super(HTMLDetailMixin, self).formfield_for_dbfield(db_field, **kwargs)
