from django.shortcuts import render, redirect
from base import models
from .Forms import exam_forms
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from base import models as TMODEL
from base import models as SMODEL
from .Forms import teacher_forms as TFORM
from .Forms import student_forms as SFORM
from django.contrib.auth.models import User
from .common import staff_home, student_home
from ..models import Users,Teacher, Department
from django.contrib.auth.decorators import login_required, user_passes_test
from .Tool.Tools import student_detials, staff_detials


def is_admin(user):
    try:
        obj = User.objects.get(id=user.id)
        get_role = Users.objects.get(user_name=obj.username)
    except:
        return False
    if get_role.role == 1:
        return True
    else:
        return False

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'exam/index.html')


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    if is_student(request.user):
        # return redirect('student/student-dashboard')
        return redirect(student_home)

    elif is_teacher(request.user):
        accountapproval = TMODEL.Teacher.objects.all().filter(
            user_id=request.user.id, status=True)
        print("runned....in the teacher")
        if accountapproval:
            return redirect(staff_home)
        else:
            return render(request, 'teacher/teacher_wait_for_approval.html')
    if is_admin(request.user):
            return redirect('admin-dashboard')
    else:
            return redirect('add_admin1')


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    dict_ = {
        'total_student': SMODEL.Student.objects.all().count(),
        'total_teacher': TMODEL.Teacher.objects.all().filter(status=True).count(),
        'total_course': models.Course.objects.all().count(),
        'total_question': models.Question.objects.all().count(),
    }
    return render(request, 'exam/admin_dashboard.html', staff_detials(request,'Admin Dashboard',dict_))


@login_required(login_url='adminlogin')
def admin_teacher_view(request):
    if Teacher.objects.get(user=request.user.id).role == 'admin':
        dict = {
            'total_teacher': TMODEL.Teacher.objects.all().filter(status=True).exclude(role='admin').count(),
            'pending_teacher': TMODEL.Teacher.objects.all().filter(status=False).count(),
            'salary': TMODEL.Teacher.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
        }
    elif Teacher.objects.get(user=request.user.id).role == 'hod':
        dict = {
            'total_teacher': TMODEL.Teacher.objects.all().filter(status=True,role='staff').count(),
            'pending_teacher': TMODEL.Teacher.objects.all().filter(status=False).count(),
            'salary': TMODEL.Teacher.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
        }
    return render(request, 'exam/admin_teacher.html',staff_detials(request,'admin teacher view ', dict))


def admin_view_teacher_view(request):
    if Teacher.objects.get(user=request.user.id).role == 'admin':
        teachers = TMODEL.Teacher.objects.all().filter(status=True).exclude(role='admin')
        
    elif Teacher.objects.get(user=request.user.id).role == 'hod':
        teachers = TMODEL.Teacher.objects.all().filter(status=True,role='staff')
    return render(request, 'exam/admin_view_teacher.html', staff_detials(request,'Staff Details',{'teachers': teachers}))


@login_required(login_url='adminlogin')
def update_teacher_view(request, pk):
    teacher = Teacher.objects.get(id=pk)
    user_pass = teacher.user.id
    user = User.objects.get(id = user_pass)
    obj = Department.objects.all()
    print(obj)
    if request.method == 'POST':
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        role = request.POST.get('role')
        department = request.POST.get('department')
        annauni_num = request.POST.get('Annauni_num')
        new_password = request.POST.get('new_password')

        # Update the fields with the new values
        teacher.address = address
        teacher.mobile = mobile
        teacher.role = role
        teacher.department = department
        teacher.Annauni_num = annauni_num
        user.set_password(new_password)
        user.save()

        # Check if a new profile picture is selected
        if 'profile_pic' in request.FILES:
            profile_pic = request.FILES['profile_pic']
            # Only update the profile_pic field if a new picture is selected
            if profile_pic:
                teacher.profile_pic = profile_pic

        teacher.save()
        return redirect('admin-view-teacher')
    else:
        return render(request, 'exam/update_teacher.html', staff_detials(request,'Update User Details',{'teacher': teacher,'obj':obj}))



@login_required(login_url='adminlogin')
def delete_teacher_view1(request, pk):
    teacher = TMODEL.Teacher.objects.get(id=pk)
    print(teacher.user_id)
    user = User.objects.get(id=teacher.user_id)
    obj= Users.objects.get(connect_id= user.id)
    user.delete()
    teacher.delete()
    obj.delete()
    print("both are deleted")
    return redirect('hod_list')

@login_required(login_url='adminlogin')
def delete_teacher_view(request, pk):
    teacher = TMODEL.Teacher.objects.get(id=pk)
    print(teacher.user_id)
    user = User.objects.get(id=teacher.user_id)
    obj= Users.objects.get(connect_id= user.id)
    user.delete()
    teacher.delete()
    obj.delete()
    print("both are deleted")
    return redirect('teacher_list')


def admin_view_pending_teacher_view(request):
    try:
        if Teacher.objects.get(user=request.user.id).role == 'hod':
            teachers = TMODEL.Teacher.objects.all().filter(status=False,role='staff')
        elif Teacher.objects.get(user=request.user.id).role == 'admin':
            teachers = TMODEL.Teacher.objects.all().filter(status=False)
    except:
        return render(request,"msg/already_accept.html")
    return render(request, 'exam/admin_view_pending_teacher.html', staff_detials(request,'Pending Teacher',{'teachers': teachers}))


@login_required(login_url='adminlogin')
def approve_teacher_view(request, pk):
    teacherSalary = exam_forms.TeacherSalaryForm()
    if request.method == 'POST':
        teacherSalary = exam_forms.TeacherSalaryForm(request.POST)
        if teacherSalary.is_valid():
            teacher = TMODEL.Teacher.objects.get(id=pk)
            teacher.salary = teacherSalary.cleaned_data['salary']
            teacher.status = True
            teacher.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-pending-teacher')
    return render(request, 'exam/salary_form.html', staff_detials(request,'Approve Teacher',{'teacherSalary': teacherSalary}))


@login_required(login_url='adminlogin')
def reject_teacher_view(request, pk):
    teacher = TMODEL.Teacher.objects.get(id=pk)
    user = User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-pending-teacher')


@login_required(login_url='adminlogin')
def admin_view_teacher_salary_view(request):
    teachers = TMODEL.Teacher.objects.all().filter(status=True)
    return render(request, 'exam/admin_view_teacher_salary.html', {'teachers': teachers})


@login_required(login_url='adminlogin')
def admin_student_view(request):
    dict = {
        'total_student': SMODEL.Student.objects.all().count(),
    }
    return render(request, 'exam/admin_student.html',staff_detials(request,'Student MCQ', dict))


@login_required(login_url='adminlogin')
def admin_view_student_view(request):
    students = SMODEL.Student.objects.all()
    return render(request, 'exam/admin_view_student.html',staff_detials(request,'View Students', {'students': students}))


@login_required(login_url='adminlogin')
def update_student_view(request, pk):
    student = SMODEL.Student.objects.get(id=pk)
    user = SMODEL.User.objects.get(id=student.user_id)
    userForm = SFORM.StudentUserForm(instance=user)
    studentForm = SFORM.StudentForm(request.FILES, instance=student)
    mydict = {'userForm': userForm, 'studentForm': studentForm}
    if request.method == 'POST':
        userForm = SFORM.StudentUserForm(request.POST, instance=user)
        studentForm = SFORM.StudentForm(
            request.POST, request.FILES, instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('admin-view-student')
    return render(request, 'exam/update_student.html',staff_detials(request,'Update Student', mydict))


@login_required(login_url='adminlogin')
def delete_student_view(request, pk):
    student = SMODEL.Student.objects.get(id=pk)
    user = User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-student')


@login_required(login_url='adminlogin')
def admin_course_view(request):
    return render(request, 'exam/admin_course.html',staff_detials(request,'Mcq Courses Details'))


@login_required(login_url='adminlogin')
def admin_add_course_view(request):
    courseForm = exam_forms.CourseForm()
    if request.method == 'POST':
        courseForm = exam_forms.CourseForm(request.POST)
        if courseForm.is_valid():
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-course')
    return render(request, 'exam/admin_add_course.html',  staff_detials(request,'Add Course',{'courseForm': courseForm}))


@login_required(login_url='adminlogin')
def admin_view_course_view(request):
    courses = models.Course.objects.all()
    return render(request, 'exam/admin_view_course.html', staff_detials(request,'Course Details',{'courses': courses}))


@login_required(login_url='adminlogin')
def delete_course_view(request, pk):
    course = models.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/admin-view-course')


@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request, 'exam/admin_question.html' ,staff_detials(request,' Manage MCQ'))


@login_required(login_url='adminlogin')
def admin_add_question_view(request):
    questionForm = exam_forms.QuestionForm()
    if request.method == 'POST':
        questionForm = exam_forms.QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            course = models.Course.objects.get(id=request.POST.get('courseID'))
            question.course = course
            question.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-question')
    return render(request, 'exam/admin_add_question.html', staff_detials(request,'Add Question',{'questionForm': questionForm}))


@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    courses = models.Course.objects.all()
    return render(request, 'exam/admin_view_question.html',staff_detials(request,'View Questions', {'courses': courses}))


@login_required(login_url='adminlogin')
def view_question_view(request, pk):
    questions = models.Question.objects.all().filter(course_id=pk)
    return render(request, 'exam/view_question.html',staff_detials(request,'View Questions',{'questions': questions}))


@login_required(login_url='adminlogin')
def delete_question_view(request, pk):
    question = models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')


@login_required(login_url='adminlogin')
def admin_view_student_marks_view(request):
    students = SMODEL.Student.objects.all()
    return render(request, 'exam/admin_view_student_marks.html',staff_detials(request,'Student Marks', {'students': students}))


@login_required(login_url='adminlogin')
def admin_view_marks_view(request, pk):
    courses = models.Course.objects.all()
    response = render(request, 'exam/admin_view_marks.html',staff_detials(request,'view marks', {'courses': courses}))
    response.set_cookie('student_id', str(pk))
    return response


@login_required(login_url='adminlogin')
def admin_check_marks_view(request, pk):
    course = models.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student = SMODEL.Student.objects.get(id=student_id)

    results = models.Result.objects.all().filter(
        exam=course).filter(student=student)
    return render(request, 'exam/admin_check_marks.html', staff_detials(request,'Check mark',{'results': results}))


def aboutus_view(request):
    return render(request, 'exam/aboutus.html')


def contactus_view(request):
    sub = exam_forms.ContactusForm()
    if request.method == 'POST':
        sub = exam_forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email), message, settings.EMAIL_HOST_USER,
                      settings.EMAIL_RECEIVING_USER, fail_silently=False)
            return render(request, 'exam/contactussuccess.html')
    return render(request, 'exam/contactus.html', {'form': sub})
