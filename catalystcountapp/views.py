from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import UploadFileForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Company,UploadedFile
from .forms import AddUserForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .serializer import CompanySerializer
from django.http import HttpResponseRedirect
import os
# Create your views here.
def home(request):
    return HttpResponseRedirect("/accounts/")
@login_required
def homepagedata(request):
    """Home Page Template to render"""
    return render(request,"homepageshow.html")
def handle_uploaded_file(file):
    """This function is responsible for file data handle"""
    #saving the file in database instead of file handling read write concept
    uploaded_file=UploadedFile(file=file)
    uploaded_file.save()
"""upload file view function"""            
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #handle_uploaded_file(request.FILES['file'], os.path.join('uploads', request.FILES['file'].name))
            ##no requirement to pass os.pasth.join uploadf,request.FILES['file'].name as we are saving file in database in upload file mode upload/  it will save
            handle_uploaded_file(request.FILES['file'])
            return JsonResponse({'message': 'File uploaded successfully'})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
def users_list(request):
    """displaying the users"""
    User = get_user_model()
    users = User.objects.all()
    form = AddUserForm()
    return render(request, 'users.html', {'users': users, 'form': form})

@login_required
def query_builder(request):
    """query builder"""
    return render(request, 'query_builder.html')

@csrf_exempt
def add_user(request):
    """this function is responsible for adding the user"""
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return JsonResponse({'success': True, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email})
    return JsonResponse({'success': False, 'errors': form.errors})

@csrf_exempt
def delete_user(request, user_id):
    """this function is responsible for delete_user"""
    try:
        User = get_user_model()
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User does not exist'})
    
"""django rest framework"""
@api_view(['GET'])
def query_companies(request):
    """making query set to filter """
    keyword = request.GET.get('keyword', '')
    industry = request.GET.get('industry', '')
    year_founded = request.GET.get('year_founded', '')
    city = request.GET.get('city', '')
    state = request.GET.get('state', '')
    country = request.GET.get('country', '')
    employees_from = request.GET.get('employees_from', '')
    employees_to = request.GET.get('employees_to', '')
    #Django ORM fetching all the data
    companies = Company.objects.all()

    if keyword:
        companies = companies.filter(name__icontains=keyword)
    if industry:
        companies = companies.filter(industry__icontains=industry)
    if year_founded:
        companies = companies.filter(year_founded=year_founded)
    if city:
        companies = companies.filter(city__icontains=city)
    if state:
        companies = companies.filter(state__icontains=state)
    if country:
        companies = companies.filter(country__icontains=country)
    if employees_from:
        companies = companies.filter(employees__gte=employees_from)
    if employees_to:
        companies = companies.filter(employees__lte=employees_to)
    serializers=CompanySerializer(companies,many=True)#for validation purpose serilizartion data structure
    count = companies.count()
    return Response({'count': count,'data':serializers.data})
