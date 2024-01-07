from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.views.generic import View, ListView, DeleteView, DetailView
from django.contrib import messages
from django.urls import reverse_lazy

# local import
from .models import Image, Task
from .forms import TaskCreationForm, TaskUpdateForm

# Create your views here.


class HomeView(ListView):
    '''Home Page and Show All Task'''
    model = Task
    template_name = 'home.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            print(self.request.user)
            return Task.objects.filter(user=self.request.user).order_by('-priority')
        return None
    
class FilterView(LoginRequiredMixin, ListView):
    '''Filter by category like completed, incompleted etc'''
    model = Task
    template_name = 'home.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        category = self.kwargs['category']
        if category == 'completed':
            return Task.objects.filter(user = self.request.user, is_completed = True)
        elif category == 'incompleted':
            return Task.objects.filter(user = self.request.user, is_completed = False)
        elif category == 'created':
            return Task.objects.filter(user = self.request.user).order_by('-created_at')
        elif category == 'due_date':
            return Task.objects.filter(user = self.request.user).order_by('due_date')
        elif category == 'priority':
            return Task.objects.filter(user = self.request.user).order_by('-priority')
        else:
            return None


class TaskCreateView(LoginRequiredMixin, FormView):
    '''Create Task and must be a Authenticate user'''

    template_name = 'tasks/task_create_form.html'
    form_class = TaskCreationForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user # set user for this task
        instance.save()

        # create instance for images
        images = self.request.FILES.getlist('images')
        print(self.request.FILES)
        for image in images:
            Image.objects.create(task=instance, image=image)

        messages.success(self.request, 'Task created successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Someting missing, please try again :(')
        return self.render_to_response(self.get_context_data(form=form))

    def handle_no_permission(self):
        messages.warning(self.request, 'You need to be logged in.')
        return redirect('login')
    

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    '''Delete a Task'''
    model = Task
    template_name = 'tasks/task_delete_conf.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        try:
            task = Task.objects.get(pk =self.kwargs['id'])
            return task
        except:
            messages.warning(self.request, "Task doesn't exist!")
            return None
        

class TaskDetailView(LoginRequiredMixin, DetailView):
    '''Task Detail view'''
    model = Task
    template_name = 'tasks/task_detail_page.html'
    context_object_name = 'task'




class TaskUpdateView(LoginRequiredMixin, FormView):
    '''Update task and also upload multple image'''
    model = Task
    template_name = 'tasks/update_task.html'
    form_class = TaskUpdateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        task_id = self.kwargs.get('id')
        task = Task.objects.get(pk=task_id, user=self.request.user)
        kwargs['instance'] = task
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = self.kwargs.get('id')
        context['task'] = Task.objects.get(pk=task_id, user=self.request.user)
        return context
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()


        # create instance for images
        images = self.request.FILES.getlist('images')
        for image in images:
            Image.objects.create(task=instance, image=image)

        messages.success(self.request, 'Task updated successfully with images.')
        return redirect('task-details', pk=instance.id)

    def form_invalid(self, form):
        task_id = self.kwargs.get('task_id')
        task = Task.objects.get(pk=task_id, user=self.request.user)
        messages.error(self.request, 'Something Error :(')
        return render(self.request, self.template_name, {'form': form, 'task': task})
    
    def handle_no_permission(self):
        messages.warning(self.request, 'You need to be logged in.')
        return redirect('login')
    

class ImageDeleteView(LoginRequiredMixin, DeleteView):
    model = Image
    template_name = 'tasks/img_delete_conf.html'

    def get_success_url(self):
        messages.success(self.request, "image deleted successfully")
        return reverse_lazy('task-details', kwargs={'pk': self.object.task.pk})
    
    def get(self, request, *args, **kwargs):
        image = self.get_object()
        if request.user == image.task.user:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('home') 
        

class TaskSearchView(LoginRequiredMixin, View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        title = request.GET.get('title', None)
        if title:
            tasks = Task.objects.filter(title__icontains=title, user = request.user)
            context = {'search': True, 'tasks': tasks}
            return render(request, self.template_name, context)
        else:
            redirect('home')