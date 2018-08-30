from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import Course,CourseOutcome, CourseAvailable, CoPo, CourseProgram
from program.models import ProgramOutcome, Program
from user.models import Profile
from .forms import Course_Form, CourseProg_Form, CourseOffer_Form, Enroll_Form
from program.forms import Course_Outcome_Form, CoPo_Link_Form
from django.contrib import messages
from django.db.models import Q
from enumerations.enum import Semester
from student.models import Student


class IndexView(generic.ListView):
    template_name = 'course/index.html'
    def get_queryset(self):
        return Course.objects.filter(deleted=False)


def DetailView(request,pk):
    course = get_object_or_404(Course, pk=pk)
    programs = CourseProgram.objects.filter(course=course.id)
    pro = ""
    #type = request.user.user_type
    type = 'F'
    for p in programs:
        pro += str(p.program.name) + " "

    context = {"course": course,
               "pro": pro,
               "type":type
              }
    return render(request, 'course/detail.html', context)


def CourseCreate(request):
    if request.method == "POST":
        course_form = Course_Form(request.POST)
        prog_form = CourseProg_Form(request.POST)

        if course_form.is_valid() and prog_form.is_valid():
            course = course_form.save()
            p = prog_form.save(commit=False)
            p.course = Course.objects.get(name=course)
            p.save()
            return redirect('course:index')

    else:
        course_form = Course_Form()
        prog_form = CourseProg_Form()

    context = {"course_form": course_form,"prog_form": prog_form,}
    return render(request, 'course/course_form.html', context)


def CourseUpdate(request, pk):
    instance = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        course_form = Course_Form(request.POST, instance=instance)
        if course_form.is_valid():
            course_form.save()
            return redirect('course:index')
    else:
        course_form = Course_Form(instance=instance)
    return render(request, 'course/course_form.html', {'course_form': course_form})


def CourseDelete(request, pk):
        instance = Course.objects.get(pk=pk)
        instance.deleted = True
        instance.save()
        return redirect('course:index')


def search(request):
    if request.method=='POST':
        srch = request.POST['srh']


        if srch:
            match = Course.objects.filter(Q(name__icontains=srch)|
                                          Q(course_code__icontains=srch)|
                                          Q(course_type__icontains=srch)|
                                          Q(semester__icontains=srch)
                                          )
            if match:
                return render(request,'course/search.html',{'sr':match})
            else:
                print(srch)
                messages.error(request,'no result found')
                return render(request, 'course/search.html', {'sr': match})
        else:
            return HttpResponseRedirect(reverse('course:index'))


def Add_CO(request,pk):
    if request.method == "POST":
        co_form = Course_Outcome_Form(request.POST)
        all_cos = CourseOutcome.objects.filter(course=pk)

        if co_form.is_valid():
            outcome = co_form.save(False)
            outcome.course = Course.objects.get(pk=pk)
            outcome = co_form.save()

            return redirect('course:po-select', co=outcome.id )

    else:
        co_form = Course_Outcome_Form
        course = Course.objects.get(pk=pk)
        all_cos = CourseOutcome.objects.filter(course=pk)

    context = {"co_form": co_form,
               "course" : course,
               "all_cos" : all_cos,
              }
    return render(request, 'course/co_form.html', context)


def Select_PO(request,co):
    no_pos = ProgramOutcome.objects.count()
    LinkFormSet = formset_factory(CoPo_Link_Form, max_num=no_pos-1)
    outcome = CourseOutcome.objects.get(pk=co)
    course = Course.objects.get(name=outcome.course)
    all_pos = ProgramOutcome.objects.all()
    if request.method == "POST":
        print("post")
        formset = LinkFormSet(request.POST)
        if (formset.is_valid()):
            print("valid")
            for form in formset:
                link = form.save(False)
                if link.level != 'N':
                    link.course_outcome = outcome
                    link.user = request.user
                    link.save()
            return redirect('course:co-new', pk=course.pk)

    else:
        formset = LinkFormSet(initial=[{'program_outcome': x.id} for x in all_pos])

    context = {"formset": formset,
               "all_pos": all_pos,
               "outcome": outcome,
               "course": course,
              }
    return render(request, 'course/select_po.html', context)


def OfferCoursesIndex(request):
    av_courses =  CourseAvailable.objects.filter(active=True)
    context = {"av_courses": av_courses,}
    return render(request, 'course/offered.html', context)


def OfferCourses(request):
    all_courses = Course.objects.filter(deleted=False)
    courseDict = {}
    for c in all_courses:
        #fetch programs from CourseProgram
        programs = CourseProgram.objects.filter(course=c.id)
        program_list = ""
        for p in programs:
            #pr = Program.objects.get
            program_list+=str(p.program.id)+";"
        courseDict[c.id]={}
        courseDict[c.id]['name']=c.name
        courseDict[c.id]['semester'] = c.semester
        courseDict[c.id]['code'] = c.course_code
        #courseDict[c.id]['programdetails']=#listOfPrograms
        courseDict[c.id]['programdetails'] = program_list
    #print (courseDict)
    form = CourseOffer_Form()
    progs = Program.objects.all()
    if request.method == "POST":
        course = request.POST.get('course')
        crse = Course.objects.get(id=course)
        year = request.POST.get('year')

        offCourses = CourseAvailable.objects.filter(course=crse.id,year=year).count()
        print(crse.id)
        print(offCourses)
        if offCourses == 0:
            off_course = form.save(commit=False)
            off_course.course = crse
            off_course.faculty = request.user
            off_course.year = year
            off_course.save()
        else:
            return HttpResponse('Already offered!')
        return redirect('course:course-offeredlist')
    sems = {d.name:d for d in Semester}
    context = {"all_courses": courseDict,
               "progs": progs, 'sems':sems }
    return render(request, 'course/offer.html', context)



def Enroll_Student(request, ca_id):
    courses = CourseAvailable.objects.get(id = ca_id)
    crse = Course.objects.get(id=courses.course.id)
    sem = crse.semester
    pro = CourseAvailable.objects.raw("select *from course_courseavailable, course_courseprogram where course_courseprogram.id=%s and "
                                      "course_courseprogram.course_id = course_courseavailable.course_id", [ca_id])
    print(pro)
    return render(request)


def Enroll_Faculty(request):
    students = Profile.objects.all()
    context = {"students": students
               }
    return render(request, 'course/enroll-faculty.html', context)


def See_Links(request,co):
    outcome = CourseOutcome.objects.get(pk=co)
    po_links = CoPo.objects.filter(course_outcome=outcome.id)
    context = {"po_links": po_links,
               "outcome": outcome,
              }
    return render(request, 'course/see_links.html', context)
