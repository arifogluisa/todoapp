from django.forms import fields
from django.http import request
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import View
from .models import Task, Comment
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from .forms import UserRegisterForm, TaskForm, CommentForm
from  django.contrib.auth.decorators import login_required




class CustomLoginView(LoginView):
    template_name = 'todoapp/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task_list')


class RegisterUser(FormView):
    template_name = 'todoapp/register.html'
    form_class = UserRegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task_list')


    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterUser, self).form_valid(form)


    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task_list')
        return super(RegisterUser, self).get(*args, **kwargs)

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'todoapp/task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(user=self.request.user)
        context['count'] = Task.objects.filter(user=self.request.user, complete=False).count()
        return context

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todoapp/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(
            task__id=self.kwargs.get('pk')
        )
        return context


    def post(self, request, *args, **kwargs):
        view = CommentAddView.as_view()
        return view(request, *args, **kwargs)




 

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'todoapp/create_task.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)
        

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    template_name = 'todoapp/create_task.html'
    form_class = TaskForm
    success_url = reverse_lazy('task_list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'todoapp/delete_task.html'
    context_object_name = 'task'
    success_url = reverse_lazy('task_list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user


class CommentAddView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'todoapp/task_detail.html'
    #success_url = reverse_lazy('task_detail')

    def form_valid(self, form):
        form.instance.commenter = self.request.user
        form.instance.task_id = self.kwargs.get('pk')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task_detail', kwargs={'pk': self.kwargs.get('pk')})





@login_required
def comment_update(request, pk):
    comment = Comment.objects.get(id=pk)
    form = CommentForm(instance=comment)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=comment.task.pk)
    context = {'form': form}
    return render(request, 'todoapp/comment_update.html', context)


@login_required
def comment_remove(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('task_detail', pk=comment.task.pk)

    context = {'comment': comment}
    return render(request, 'todoapp/comment_delete.html', context)


        

