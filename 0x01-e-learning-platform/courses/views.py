from django.shortcuts import get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.apps import apps
from django.forms.models import modelform_factory
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from .forms import ModuleFormSet
from django.views.generic.base import TemplateResponseMixin, View

from .models import Course, Module, Content

# Create your views here.


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(
    OwnerMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin
):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'
    

class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'

class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None
    
    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)
    
    def dispatch(self, request, pk):
        self.course = get_object_or_404(
            Course,
            id=pk,
            owner=request.user
        )
        return super().dispatch(request, pk)
    
    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({
            'course': self.course,
            'formset': formset
        })
    
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        
        return self.render_to_response({
            'course': self.course,
            'formset': formset
        })

class ContentCreateUpdateView(TemplateResponseMixin, View):
    # TemplateResponseMixin - simplify the rendering of templates
    # by providing the ability to specify a template for rendering
    # the response, along with context data
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'
    
    def get_model(self, model_name):
        # Check that the given model name is one of the four content models:
        # Text, Video, Image, or File.
        # Use Django’s apps module to obtain the actual class for
        # the given model name.
        # If the given model name is not one of the valid ones,
        # return None
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(
                app_label='courses',
                model_name=model_name
            )
        
        return None
    
    def get_form(self, model, *args, **kwargs):
        # Build a dynamic form using the modelform_factory()
        # function of the form’s framework.
        Form = modelform_factory(
            model,
            exclude=['owner', 'order', 'created', 'updated']
        )
        
        return Form(*args, **kwargs)
    
    def dispatch(self, request, module_id, model_name, id=None):
        # Receives the following URL parameters and stores the
        # corresponding module, model, and content object as
        # class attributes.
        self.module = get_object_or_404(
            Module,
            id=module_id,
            course__owner=request.user
        )
        self.model = self.get_model(model_name)
        
        if id:
            self.obj = get_object_or_404(
                self.model,
                id=id,
                owner=request.user
            )
        return super().dispatch(request, module_id, model_name, id)
    
    def get(self, request, module_id, module_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({
            'form': form,
            'object': self.obj
        })
    
    def post(self, request, module_id, module_name, id=None):
        form = self.get_form(
            self.model,
            instance=self.obj,
            data=request.POST,
            file= request.FILES
        )
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            
            if not id:
                # new content
                Content.objects.create(module=self.module, item=obj)
        
            return redirect(
                'module_content_list',
                self.module.id
            )
        # render_to_resonse() purpose is to combine a template and
        # context data to produce an HTTP response
        return self.render_to_response({
            'form': form,
            'object': self.obj
        })


class ContentDeleteview(View):
    # Retrieves the content object with the given ID. 
    # It deletes the related Text, Video, Image, or File object.
    # Finally, it deletes the content object
    # and redirects the user to the module_content_list 
    # URL to list the other contents of the module
    def post(self, request, id):
        content = get_object_or_404(
            Content,
            id=id,
            module__course__owner=request.user
        )
        module = content.module
        content.item.delete()
        content.delete()
        return redirect(
            'module_content_list',
            module.id
        )


class ModuleContentListView(TemplateResponseMixin, View):
    # Gets the Module object with the given ID that belongs 
    # to the current user and renders a template with the given module
    template_name = 'courses/manage/module/content_list.hmtl'
    
    def get(self, request, module_id):
        module = get_object_or_404(
            Module,
            id=module_id,
            course__owner=request.user
        )
        return self.render_to_response({
            'module': module
        })