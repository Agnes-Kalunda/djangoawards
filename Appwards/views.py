from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, EditProfileForm, NewProjectForm
from .models import Profile, Project, Comments, Rating
from django.contrib.auth import logout
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProlfileSerializer,ProjectSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly
# Create your views here.
@login_required(login_url='/accounts/login/')
def welcome(request):
    return render(request, 'welcome.html')

def index(request):
    all_projects = Project.all_projects()
    return render(request, 'index.html', {'all_projects': all_projects})
@login_required(login_url='/accounts/login/')
def user_profile(request):
    all_profiles= Project.objects.filter(user = request.user)
    return render(request,'profile.html', {'all_profiles':all_profiles})
@login_required(login_url='/accounts/login/')
def search_reslts(request):
    
    if 'project' in request.GET and request.GET['project']:
        search_term = request.GET.get('project')
        searched_project =Project.search_project(search_term)
        message = f'{search_term}'
        return render(request,'search.html', {'message':message,'project':searched_project})
    
    else:
        message = 'You have not entered anything to search '
        return render(request, 'search.html', {'message':message})
@login_required(login_url='/accounts/login/')
def Newproject(request):
    if request.method=='POST':
        form = NewProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('home')
    else:
        form = NewProjectForm()
        return render(request, 'New-project.html', {'form':form})
@login_required(login_url='/accounts/login/')
def singleProject(request, id):
    project = Project.objects.get(id=id)
    comments = Comments.objects.filter(project_id=id)
    rates = Rating.objects.filter(project_id = id)
    designrate = []
    usabilityrate =[]
    contentrate = []
    if rates:
        for rate in rates:
            designrate.append(rate.design)
            usabilityrate.append(rate.usability)
            contentrate.append(rate.content)
        
        total = len(designrate)*10
        design = round(sum(designrate)/total*100, 1)
        usability = round(sum(usabilityrate)/total*100,1)
        content = round(sum(contentrate)/total*100,1)
        return render(request, 'single_project.html',{'project':project, 'comments':comments,'design': design,'usability': usability, 'content':content})
    else:
        design = 0
        usability = 0
        content = 0
        return render(request, 'single_project.html',{'project':project, 'comments':comments, 'design': design,'usability':usability, 'content':content})
@login_required(login_url='/accounts/login/')
def profileEdit(request):
    user = request.user
    if request.method=='POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile= form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
    else:
        form = EditProfileForm(request.POST, request.FILES)
    return render(request, 'update_profile.html',{'form': form})
@login_required(login_url='/accounts/login/')
def comment(request,id):
    id = id
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            project = Project.objects.get(id=id)
            comment.project_id=project
            comment.save()
            return redirect('home')
        else:
            project_id=id
            messages.info(request, 'Fill in all the fields')
            return redirect('comment', id=project_id)
    else:
        id = id
        form = CommentForm()
        return render(request, 'comment.html', {'form':form, 'id':id})
@login_required(login_url='/accounts/login/')
def Rate(request, id):
    if request.method =='POST':
        rates = Rating.objects.filter(id=id)
        for rate in rates:
            if rate.user == request.user:
                messages.info(request, 'You can only rate a project once')
                return redirect('singleproject', id)
        design = request.POST.get('design')
        usability = request.POST.get('usability')
        content = request.POST.get('content')
        if design and usability and content:
            project = Project.objects.get(id=id)
            rate = Rating(design = design, usability = usability, content = content, project_id = project, user = request.user)
            rate.save()
            return redirect('singlproject', id)
        else:
            messages.info(request,'Input all fields')
            return redirect('singleproject', id)
    else:
        messages.info(request, 'Input all fields')
        return redirect('singleproject', id)
            
@login_required(login_url='/accounts/login/')
def logoutRequest(request):
    logout(request)
    return redirect('home')
class ProjectRest(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self, request, format=None):
        all_project = Project.objects.all()
        serializers = ProjectSerializer(all_project, many=True)
        return Response(serializers.data)
    def post(self, request, format=None):
        serializers = ProjectSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
class ProifleRest(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self, request, format=None):
        all_profile = Profile.objects.all()
        serializers = ProlfileSerializer(all_profile, many=True)
        return Response(serializers.data)
    def post(self, request, format=None):
        serializers = ProlfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)