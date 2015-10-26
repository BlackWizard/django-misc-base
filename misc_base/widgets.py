# -*- coding:utf-8 -*-

from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.forms.widgets import ClearableFileInput as oldWidget, CheckboxInput, FileInput, Input

from nginx_filter_image.templatetags.pimage import pimage_single, pimage_sizes

class ClearableFileInput(oldWidget, FileInput):
    #template_with_initial = u'%(initial_text)s: %(initial)s %(clear_template)s<br />%(input_text)s: %(input)s'
    template_with_initial = u'%(initial)s %(clear_template)s %(input_text)s:&nbsp;%(input)s<br clear="all"/>'
    
    template_with_clear = u'<label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s %(clear)s </label>'

    def __init__(self, pimage, attrs={}):
        super(ClearableFileInput, self).__init__(attrs=attrs)
        self.pimage = pimage

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label}
        template = u'%(input)s'
        substitutions['input'] = super(FileInput, self).render(name, value, attrs)
        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = (u'<img src="%s" %s>'
                                        % (
                                           pimage_single(escape(value.url), self.pimage),
                                           pimage_sizes(value, self.pimage),
                                           )
                                        )
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)
