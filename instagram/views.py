from django.shortcuts import render,redirect,get_object_or_404
from instagram import views
from django.contrib.auth.models import User
from django.contrib.auth import login, views, forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from .forms import LikesForm, CommentsForm, UpdateProfileForm, UploadPicForm,Image,Profile,Like
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,Http404,HttpResponseRedirect

from .forms import UserLoginForm, UserRegisterForm

# Create your views here.

def landingpage(request):
  
    return render(request, 'landingpage.html')

def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('login')
    context = {
        'form': form,
    }
    return render(request, "register.html", context)

    
def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('home')

    context = {
        'form': form,
    }
    return render(request, "login.html", context)
def home(request):
  likesForm = LikesForm
  commentForm = CommentsForm
  images = Image.objects.all()
  user = request.user.get_username()
  profile = Profile.objects.all()
  likes = Like.objects.all()
  
  return render(request,'home.html', locals())

def profile(request):
    likesForm = LikesForm
    commentForm = CommentsForm
    images = Image.objects.all()
    user = request.user.get_username()
    current_user = request.user
    photos = Image.objects.filter(profile=current_user.id)
    profile = Profile.objects.all()
    likes = Like.objects.all()
    
     
    return render(request,'profile.html', locals())
def likes(request,image_id):
  likesForm = LikesForm()
  #  CRUD     
  obj1=Like.objects.create(user=request.user,image=get_object_or_404(Image,pk=image_id),likes=1)
  obj1.save()
  print(obj1)
  return redirect('home')


def comments(request,image_id):
  commentsForm = CommentsForm()
  if request.method == 'POST':
    commentsForm = CommentsForm(request.POST)
    if commentsForm.is_valid():
      form = commentsForm.save(commit=False)
      form.user=request.user
      form.image = get_object_or_404(Image,pk=image_id)
      form.save()
  
  return redirect('home')

#search feature
# @login_required(login_url='/accounts/login')
def search_results(request):
  likesForm = LikesForm
  commentForm = CommentsForm
  images = Image.objects.all()
  user = request.user.get_username()
  current_user = request.user
  photos = Image.objects.filter(profile=current_user.id)
  profile = Profile.objects.all()
  likes = Like.objects.all()
        
  try:
    user = User.objects.get(id =request.user.id)
  except ObjectDoesNotExist:
    raise Http404()
  message = 'based on your search term'
  return render(request, 'search.html',locals())
      
  if 'username' in request.GET and request.GET["username"]:
    form = forms.AuthenticationForm
    images = Image.objects.all()
    user = request.user.get_username()
    profile = Profile.objects.all()
    search_term = request.GET.get("username")
    searched_users = Image.search_by_username(search_term)
    message = f"{search_term}"
    photos = Image.objects.filter(profile=User.objects.get(username=search_term))

    return render(request, 'search.html',locals())

  else:
    message = "You haven't searched for any term"
    return render(request, 'search.html',locals())

#profile page
# @login_required(login_url='/accounts/login')


#update current user profile
@login_required(login_url='/accounts/login')
def updateProfile(request):
  current_user = request.user
  my_prof = Profile.objects.get(user=current_user.id)
  updateForm = UpdateProfileForm(instance=request.user)
 
  if request.method == 'POST':
    updateForm = UpdateProfileForm(request.POST,request.FILES,instance=request.user.profile)

    if updateForm.is_valid():
      updateForm.save()      
            
    return redirect('profile')
  else:
    updateForm = UpdateProfileForm(instance=request.user.profile)

  return render(request,'update_profile.html', locals())

#upload feed/pic/video page
# @login_required(login_url='/accounts/login')
def uploadPic(request):
  current_user = request.user
  uploadForm = UploadPicForm()
  print(uploadForm)

  if request.method == 'POST':
    uploadForm = UploadPicForm(request.POST,request.FILES)
    user = request.user.id

    if uploadForm.is_valid():
      upload = uploadForm.save(commit=False)
      upload.user = request.user.profile
      upload.profile = current_user
      upload.save()    
            
    return redirect('profile')
  else:
    uploadForm = UploadPicForm()

  return render(request,'uploadpic.html', locals()) 