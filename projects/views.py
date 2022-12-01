from django.shortcuts import render,get_object_or_404, HttpResponseRedirect, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from register.models import Project
from projects.models import Task
from projects.forms import NewCommentForm
from projects.forms import TaskRegistrationForm
from projects.forms import ProjectRegistrationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def findtemp(request):
    if request.user.groups.filter(name='Intern').exists():
        return 'intern/tempintern.html'
    elif request.user.groups.filter(name='Sr Intern').exists():
        return 'srintern/tempsrintern.html'
    elif request.user.groups.filter(name='Professor').exists():
        return 'srintern/tempsrintern.html'
    elif request.user.groups.filter(name='Lead Consultant').exists():
        return 'consultant/tempprof.html'
    elif request.user.groups.filter(name='Head Consultant').exists():
        return 'consultant/tempprof.html'
# Create your views here.
def projects(request):
    projects = Project.objects.all()
    avg_projects = Project.objects.all().aggregate(Avg('complete_per'))['complete_per__avg']
    tasks = Task.objects.all()
    overdue_tasks = tasks.filter(due='2')
    var = findtemp(request)
    context = {
        'avg_projects' : avg_projects,
        'projects' : projects,
        'tasks' : tasks,
        'overdue_tasks' : overdue_tasks,
        'temp':var,
    }
    return render(request, 'projects/projects.html', context)

def taskprofile(request,id):
    tasks = Task.objects.filter(assign = id)
    var = findtemp(request)
    context = {
        'tasks': tasks,
        'temp':var,
    }
    return render(request,'projects/tasks.html',context)

def newTask(request):
    if request.method == 'POST':
        form = TaskRegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            var = findtemp(request)
            context = {
                'created': created,
                'form': form,
                'temp':var,
            }
            return render(request, 'projects/new_task.html', context)
        else:
            return render(request, 'projects/new_task.html', context)
    else:
        form = TaskRegistrationForm()
        var = findtemp(request)
        context = {
            'form': form,
            'temp': var,
        }
        return render(request,'projects/new_task.html', context)

def newProject(request):
    if request.method == 'POST':
        form = ProjectRegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            form = ProjectRegistrationForm()
            var = findtemp(request)
            context = {
                'created': created,
                'form': form,
                'temp':var,
            }
            return render(request, 'projects/new_project.html', context)
        else:
            return render(request, 'projects/new_project.html', context)
    else:
        form = ProjectRegistrationForm()
        var = findtemp(request)
        context = {
            'form': form,
            'temp':var,
        }
        return render(request,'projects/new_project.html', context)

class edittask(generic.UpdateView):
    model = Task
    fields = ["status"]
    template_name = "projects/etask.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        var = findtemp(self.request)
        context["temp"] = var
        
        return context
        
def taskprofile1(request):
    tasks = Task.objects.filter()
    context = {
        'tasks': tasks,
    }
    return render(request,'projects/alltasks.html',context)

def comment(request):
    return render(request,'projects/vtask.html')
    


def viewtask(request, task):

    task = get_object_or_404(Task, id=task)

    allcomments = task.comments.filter(status=True)
    
    page = request.GET.get('page', 1)

    paginator = Paginator(allcomments, 10)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    user_comment = None

    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.username=request.user.username
            user_comment.task = task
            user_comment.save()
            # return HttpResponseRedirect('/' +'projects/etask'+'/'+task.slug)
            return redirect('projects:viewtask',task= task.id)
        
    else:
        comment_form = NewCommentForm()
        
    return render(request, 'projects/etask.html', {'task': task, 'comments':  user_comment, 'comments': comments, 'comment_form': comment_form, 'allcomments': allcomments, })




@login_required(login_url='login')
def ProjectProfile(request,id):
    
    projdet = Project.objects.all()
    var = findtemp(request)
    context = {'projdet': projdet,'pid':id,
    'temp':var,
    }
    
    return render(request,"projectprofile.html",context)
