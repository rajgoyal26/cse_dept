from django.shortcuts import render,redirect
from django.contrib.auth.models import User, Group
from user.views import group_required
from .forms import FacultyRegistrationForm,FacultyRegistrationFormSubmit
from .models import Faculty
from student.models import Student
from django.contrib.auth.decorators import permission_required

# Create your views here.


#@permission_required('user.view_profile')
def updateFacultyProfile(request):
    if request.method == "POST":
        try:
            if request.user.faculty.submit is True:
                faculty_form = FacultyRegistrationFormSubmit(request.POST, instance=request.user.faculty)
            else:
                faculty_form = FacultyRegistrationForm(request.POST, instance=request.user.faculty)
        except:
            faculty_form = FacultyRegistrationForm(request.POST)

        if faculty_form.is_valid():
            fprofile = faculty_form.save(commit=False)
            fprofile.user = request.user
            if 'Submit' in request.POST:
                faculty_group = Group.objects.get(name='Faculty')
                request.user.groups.add(faculty_group)
                fprofile.submit = True
            fprofile.save()
        return redirect('faculty:register')

    else:
        try:
            if request.user.faculty.submit is True:
                faculty_form = FacultyRegistrationFormSubmit(instance=request.user.faculty)
            else:
                faculty_form = FacultyRegistrationForm(instance=request.user.faculty)
        except:
            faculty_form = FacultyRegistrationForm()
    return render(request, 'faculty/updateFacultyForm.html', {'form': faculty_form})


def showFacultyList(request):
    detail=Faculty.objects.all()
    return render(request,'faculty/showfacultylist.html',{'detail':detail})


@group_required('Faculty')
def viewProfileFaculty(request):
    faculty = Faculty.objects.get(user_id=request.user.id)
    return render(request, 'faculty/profile.html', {'faculty':faculty})


@group_required('Faculty')
def student_list(request):
    student_list = Student.objects.all()
    return render(request,'faculty/student_list.html',{'student_list':student_list})
