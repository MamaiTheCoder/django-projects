from django.forms.models import inlineformset_factory

from .models import Course, Module

# Inline formsets are a small abstraction on top of formsets that simplify
# working with related objects
ModuleFormSet = inlineformset_factory(
    Course,
    Module,
    # fields that will be included
    # in each form of the formset
    fields=['title', 'description'],
    # set the number of empty extra forms to display
    # in the formset.
    extra=2,
    # Django will include a Boolean field for each form 
    # that will be rendered as a checkbox input.
    # It allows you to mark the objects that you want to
    # delete.
    can_delete=True
)