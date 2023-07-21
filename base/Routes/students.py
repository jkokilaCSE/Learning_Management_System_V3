from django.shortcuts import render, get_object_or_404, redirect
from base import models
from .Forms import student_forms
from ..models import Users, Student, SocialMedia, Sec_Daily_test_mark, Department, Teacher
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from base import models as QMODEL
from django.contrib.auth.models import User
# for showing signup/login button for student
from .Tool.Tools import student_detials, staff_detials
from django.views.decorators.csrf import csrf_exempt
from .study import is_admin
from django.contrib.auth.decorators import login_required, user_passes_test
# views.py


def students_list(request):
    students = Student.objects.all()
    departments = set([student.department for student in students])
    context = {
        'students': students,
        'departments': departments,
    }
    return render(request, 'student/students_list.html', context)

@user_passes_test(is_admin)
def admin_students_list(request):
    students = Student.objects.all()

    # Get unique departments, joined years, and semesters
    departments = set([student.department for student in students])
    department = Department.objects.all()
    joined_years = set([student.joinned_year for student in students])

    context = {
        'students': students,
        'departments': departments,
        'joined_years': joined_years,
    }
    return render(request, 'student/admin_students_list.html',staff_detials(request,'Student list',context) )

def students_list_by_dep(request):
    usr_id = request.user.id
    usr_obj = User.objects.get(id=usr_id)
    name = Users.objects.get(user_name=usr_obj.username)
    faculty_details = Teacher.objects.get(user=usr_obj)
    print(faculty_details.department)
    students = Student.objects.filter(department=faculty_details.department)
    departments = set([student.department for student in students])
    context = {
        'students': students,
        'departments': departments,
        'data':'std'
    }
    return render(request, 'student/students_list.html',  staff_detials(request, 'Manage Students',context))

def staff_list_by_dep(request):
    usr_id = request.user.id
    usr_obj = User.objects.get(id=usr_id)
    faculty_details = Teacher.objects.get(user=usr_obj)
    students = Teacher.objects.filter(department=faculty_details.department,role='staff')
    departments = set([student.department for student in students])
    context = {
        'students': students,
        'departments': departments,
    }
    return render(request, 'student/students_list.html',  staff_detials(request, 'Manage Staff',context))



def student_delete(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = User.objects.get(id=student.user.id)
    obj= Users.objects.get(connect_id= user.id)
    
    students = Student.objects.all()
    departments = set([student.department for student in students])
    user.delete()
    obj.delete()
    student.delete()
    print("both are deleted")
    
    context = {
        'students': students,
        'departments': departments,
        'student': student
    }
    
    if Teacher.objects.get(user=User.objects.get(id=request.user.id)).role == 'admin':
        return redirect('admin_students_list')
    else:
        return render(request,'msg/std_deleted.html')

def student_profile(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    usr_id = request.user.id
    # usr_obj = User.objects.get(id=usr_id)
    std_data = get_object_or_404(Student, pk=student_id) # it's modifyed for admin acces if you have any problem change it usr_obj
    try:
        links = SocialMedia.objects.get(std_id=usr_id)
    except:
        links=None
    dict_data = {
        'usr': std_data,
        'page': 'Student Profile',
        'student': student,
        'links':links
    }
    try:
        Teacher.objects.get(user=User.objects.get(id=request.user.id))
        return render(request, 'student/student_profile.html', staff_detials(request, 'Student Profile' ,dict_data))
    except:
        return render(request, 'student/student_profile.html', student_detials(request, 'Student Profile' ,dict_data))


from django.contrib import messages

def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    user = User.objects.get(id=student.user.id)
    department = Department.objects.all()
    current_id = request.user.id

    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()

        student.mail_id = request.POST['email']
        student.parent_mail_id = request.POST['parent_mail_id']
        student.address = request.POST['address']
        student.mobile = request.POST['mobile']
        student.joinned_year = request.POST['joinned_year']
        student.role_no = request.POST['role_no']
        student.department = request.POST['department']
        
        # Check if a new profile picture is provided
        profile_pic = request.FILES.get('file_', None)
        if profile_pic:
            student.profile_pic = profile_pic

        password = request.POST.get('password', None)
        if password:
            user.set_password(password)
            user.save()
            # Important: Update the session to keep the user logged in after password change

        student.save()

        messages.success(request, 'Profile updated successfully!')
        return render(request, 'msg/profile_updated.html', {'pk': pk})
    else:
        context = {'student': student, 'department': department}
        try:
            Teacher.objects.get(user=User.objects.get(id=request.user.id))
            return render(request, 'student/eddit_staff_handle.html', staff_detials(request, 'Edit Detials', context))
        except Exception as e:
            print(e)
            return render(request, 'student/edit_student_profile.html', student_detials(request, 'Edit Detials', context))

def staff_edit(request, pk):
    student = get_object_or_404(Teacher, pk=pk)
    department = Department.objects.all()
    current_id = request.user.id
    if request.method == 'POST':
        student.user.first_name = request.POST['first_name']
        student.user.last_name = request.POST['last_name']
        student.mail_id = request.POST['email']
        student.address = request.POST['address']
        student.mobile = request.POST['mobile']
        student.joinned_year = request.POST['joinned_year']
        student.role_no = request.POST['role_no']
        student.department = request.POST['department']
        student.profile_pic = request.FILES['file_']
        student.user.save()
        student.save()
        return redirect('student_edit',pk=pk)
    else:
        context = {'student': student,'department':department}
        return render(request, 'student/edit_staff_profile.html', staff_detials(request, 'Edit Detials', context))


def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'student/studentclick.html')
 

def student_signup_view(request):
    userForm = student_forms.StudentUserForm()
    studentForm = student_forms.StudentForm()
    mydict = {'userForm': userForm, 'studentForm': studentForm}
    if request.method == 'POST':
        userForm = student_forms.StudentUserForm(request.POST)
        studentForm = student_forms.StudentForm(request.POST, request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            student = studentForm.save(commit=False)
            student.user = user
            student.save()
            add_user = Users(user_name=user.username,
                             mail_id=user.username, password=user.password, role='4')
            add_user.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request, 'student/studentsignup.html', context=mydict)


def add_student_signup_view(request):
    userForm = student_forms.StudentUserForm()
    studentForm = student_forms.StudentForm()
    mydict = {'userForm': userForm, 'studentForm': studentForm}
    if request.method == 'POST':
        userForm = student_forms.StudentUserForm(request.POST)
        studentForm = student_forms.StudentForm(request.POST, request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            student = studentForm.save(commit=False)
            student.user = user
            student.save()
            add_user = Users(user_name=user.username, connect_id= user.id,
                             mail_id=user.username, password=user.password, role='4')
            add_user.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
            return HttpResponseRedirect('addstudentlogin')
        else:
            # If the form data is not valid, render the form with the errors
            return render(request, 'msg/std_error.html', staff_detials(request, 'Add Student', {'userForm': userForm, 'studentForm': studentForm}))
    return render(request, 'student/studentsignup.html', staff_detials(request,'Add Student',mydict))


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):

    usr_id = request.user.id
    usr_obj = User.objects.get(id=usr_id)
    std_data = Student.objects.get(user=usr_obj)
    data = Sec_Daily_test_mark.objects.filter(
        user_name=Student.get_name).order_by('Date')
    for i in data:
        print(i.class_id, i.user_name)
    dict = {
        'datas': data,
        'total_course': QMODEL.Course.objects.all().count(),
        'total_question': QMODEL.Question.objects.all().count(),
        'usr': std_data,
        'page': 'Dashboard'
    }

    return render(request, 'student/student_dashboard.html', context=dict)


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/student_exam.html', student_detials(request, 'Examination', {'courses': courses}))


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    total_questions = QMODEL.Question.objects.all().filter(course=course).count()
    questions = QMODEL.Question.objects.all().filter(course=course)
    total_marks = 0
    for q in questions:
        total_marks = total_marks + q.marks

    return render(request, 'student/take_exam.html', student_detials(request, 'Take Exam', {'course': course, 'total_questions': total_questions, 'total_marks': total_marks}))


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    questions = QMODEL.Question.objects.all().filter(course=course)
    if request.method == 'POST':
        pass
    response = render(request, 'student/start_exam.html', student_detials(request,
                      'start-exam', {'course': course, 'questions': questions}))
    response.set_cookie('course_id', course.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
@csrf_exempt
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course = QMODEL.Course.objects.get(id=course_id)

        total_marks = 0
        questions = QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):

            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks = total_marks
        result.exam = course
        result.student = student
        result.save()

        return HttpResponseRedirect('view-result')


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/view_result.html', student_detials(request,'View Result',{'courses': courses}))


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results = QMODEL.Result.objects.all().filter(
        exam=course).filter(student=student)
    return render(request, 'student/check_marks.html', student_detials(request,"Check Mark",{'results': results}))


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/student_marks.html', student_detials(request, 'My Marks', {'courses': courses}))
