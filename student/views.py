from django.shortcuts import render
from .forms import StudentProfile, StudentProfileSubmit
from django.shortcuts import redirect
from .models import Student
from django.contrib.auth.models import Group
from user.views import group_required
# Creating a Student Profile


def update(request):
    if request.method == 'POST':
            try:
                if request.user.student.submit:
                    form = StudentProfileSubmit(request.POST, instance=request.user.student)
                else:
                    form = StudentProfile(request.POST, instance=request.user.student)
            except:
                form = StudentProfile(request.POST)

            if form.is_valid():
                student = form.save(commit=False)
                if 'Submit' in request.POST:
                    student.submit = True
                student.user = request.user
                form.save()
                return redirect('student:update')
            context = {'form': form}
            return render(request, 'student/student_form.html', context)

    else:
        try:
            if request.user.student.submit:
                form = StudentProfileSubmit(instance=request.user.student)
                student = request.user.student
                context = {'form': form , 'student': student}
            else:
                form = StudentProfile(instance=request.user.student)
                context = {'form': form}
        except:
            form = StudentProfile()
            context = {'form': form}
        return render(request, 'student/student_form.html', context)


# Faculty Will have the link
@group_required('Faculty')
def profile(request, pk):
    student = Student.objects.get(pk=pk)
    return render(request, 'student/student_profile_detail.html', {'student':student})


#@group_required('Faculty', 'Student')
def show_student_list(request):
    detail = Student.objects.all()
    return render(request, 'student/show_student_list.html', {'detail': detail})