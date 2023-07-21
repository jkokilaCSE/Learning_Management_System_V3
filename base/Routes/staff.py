
import datetime
from django.shortcuts import render
from ..models import Faculty_details, Users, Teacher
from django.contrib.auth.models import User
from django.shortcuts import render
from .Forms import teacher_forms
from django.shortcuts import render
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from base import models as QMODEL
from base import models as SMODEL
from .Forms import exam_forms as QFORM
from .Tool.Tools import student_detials, staff_detials
from django.contrib.auth.decorators import user_passes_test

def is_superuser(user):
    return user.is_superuser

# for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'teacher/teacherclick.html')


def user_added_message(request):
    obj = Teacher.objects.get(user=User.objects.get(id=request.user.id)).role
    return render(request,'attandees/add_staff_message.html',{'role':obj})

def teacher_signup_view(request):
    userForm = teacher_forms.TeacherUserForm()
    teacherForm = teacher_forms.TeacherForm()
    mydict = {'userForm': userForm, 'teacherForm': teacherForm}
    if request.method == 'POST':
        userForm = teacher_forms.TeacherUserForm(request.POST)
        teacherForm = teacher_forms.TeacherForm(request.POST, request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            teacher = teacherForm.save(commit=False)
            teacher.user = user
            print(teacher.role)
            if teacher.role == 'hod':
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='2')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()
            if teacher.role == 'admin':
                teacher.status = True
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='1')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()
            elif teacher.role == 'staff': 
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='3')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
        else:
            print("not valied....at staff/teacher_signup_view")
            return render(request,'msg/user_cant_create.html')
        return HttpResponseRedirect('user_added_message')
    
    return render(request, 'teacher/teachersignup.html',staff_detials(request, 'Add Staff',mydict))

def teacher_signup_view1(request):
    userForm = teacher_forms.TeacherUserForm()
    teacherForm = teacher_forms.TeacherForm()
    mydict = {'userForm': userForm, 'teacherForm': teacherForm}
    if request.method == 'POST':
        userForm = teacher_forms.TeacherUserForm(request.POST)
        teacherForm = teacher_forms.TeacherForm(request.POST, request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            teacher = teacherForm.save(commit=False)
            teacher.user = user
            print(teacher.role)
            if teacher.role == 'hod':
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='2')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()
            if teacher.role == 'admin':
                teacher.status = True
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='1')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()
            elif teacher.role == 'staff':
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='3')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
        else:
            print("not valied....1")
            return render(request,'msg/user_cant_create.html')
        return HttpResponseRedirect('teacherlogin')
    
    return render(request, 'teacher/teachersignup.html',mydict)

def teacher_signup_viewhod(request):
    userForm = teacher_forms.TeacherUserForm()
    teacherForm = teacher_forms.TeacherForm()
    mydict = {'userForm': userForm, 'teacherForm': teacherForm}
    if request.method == 'POST':
        userForm = teacher_forms.TeacherUserForm(request.POST)
        teacherForm = teacher_forms.TeacherForm(request.POST, request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            teacher = teacherForm.save(commit=False)
            teacher.user = user
            print(teacher.role)
            if teacher.role == 'hod':
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='2')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()
            if teacher.role == 'admin':
                teacher.status = True
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='1')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()
            elif teacher.role == 'staff':
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='3')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
        else:
            print("not valied....1")
            return render(request,'msg/user_cant_create.html')
        return HttpResponseRedirect('teacherlogin')
    
    return render(request, 'teacher/teachersignup.html',mydict)


def adminsignup(request):
    userForm = teacher_forms.TeacherUserForm()
    teacherForm = teacher_forms.TeacherForm()
    mydict = {'userForm': userForm, 'teacherForm': teacherForm}
    if request.method == 'POST':
        userForm = teacher_forms.TeacherUserForm(request.POST)
        teacherForm = teacher_forms.TeacherForm(request.POST, request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            teacher = teacherForm.save(commit=False)
            teacher.user = user
            print(teacher.role)
            if teacher.role == 'hod':
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='2')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()
            if teacher.role == 'admin':
                teacher.status = True
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='1')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()
            elif teacher.role == 'staff':
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='3')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
        else:
            return render(request,'msg/user_cant_create.html')
        return HttpResponseRedirect('teacherlogin')
    
    return render(request, 'teacher/adminsignup.html',mydict)




def add_admin(request):
    userForm = teacher_forms.TeacherUserForm()
    teacherForm = teacher_forms.TeacherForm()
    mydict = {'userForm': userForm, 'teacherForm': teacherForm}
    if request.method == 'POST':
        userForm = teacher_forms.TeacherUserForm(request.POST)
        teacherForm = teacher_forms.TeacherForm(request.POST, request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            teacher = teacherForm.save(commit=False)
            teacher.user = user
            print(teacher.role)
            
            
            if teacher.role == 'hod':
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='2')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()
            if teacher.role == 'admin':
                teacher.status = True
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='1')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()
            elif teacher.role == 'staff':
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='3')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
        else:
            print("not valied")
            print("Form data is not valid")
            print(userForm.errors)
            print(teacherForm.errors)
            return render(request,'msg/user_cant_create.html')
        return HttpResponseRedirect('user_added_message')
    return render(request, 'teacher/addadmin.html',mydict)



@user_passes_test(is_superuser)
def add_admin1(request):
    userForm = teacher_forms.TeacherUserForm()
    teacherForm = teacher_forms.TeacherForm1()
    mydict = {'userForm': userForm, 'teacherForm': teacherForm}
    if request.method == 'POST':
        userForm = teacher_forms.TeacherUserForm(request.POST)
        teacherForm = teacher_forms.TeacherForm1(request.POST, request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            teacher = teacherForm.save(commit=False)
            teacher.user = user
            print(teacher.role)
            
            
            if teacher.role == 'hod':
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='2')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()
            if teacher.role == 'admin':
                teacher.status = True
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='1')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()
            elif teacher.role == 'staff':
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='3')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
        else:
            print("not valied")
            print("Form data is not valid")
            print(userForm.errors)
            print(teacherForm.errors)
            return render(request,'msg/admin_user_error.html')
        return HttpResponseRedirect('admin_added')
    return render(request, 'teacher/addadmin.html',mydict)


def add_teacher_hod(request):
    userForm = teacher_forms.TeacherUserForm()
    teacherForm = teacher_forms.TeacherFormhod()
    mydict = {'userForm': userForm, 'teacherForm': teacherForm}
    if request.method == 'POST':
        userForm = teacher_forms.TeacherUserForm(request.POST)
        teacherForm = teacher_forms.TeacherFormhod(request.POST, request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            teacher = teacherForm.save(commit=False)
            teacher.user = user
            print(teacher.role)
            
            
            if teacher.role == 'hod':
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='2')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()
            if teacher.role == 'admin':
                teacher.status = True
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='1')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()
            elif teacher.role == 'staff':
                teacher.save()
                add_user = Users(user_name=user.username, connect_id= user.id,
                                 mail_id=user.username, password=user.password, role='3')
                add_user.save()
                current_user = Users.objects.get(mail_id=user.username)
                Fac_del = Faculty_details(user_name=user.username, mail=user.username,
                                          role=current_user, id_number=0, name=str(user.first_name)+" "+str(user.last_name))
                Fac_del.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
        else:
            print("not valied")
            print("Form data is not valid")
            print(userForm.errors)
            print(teacherForm.errors)
            return render(request,'msg/user_cant_create.html')
        return HttpResponseRedirect('user_added_message')

    return render(request, 'teacher/hodsignup.html',staff_detials(request,'Add User',mydict))

def admin_added(request):
    return render(request,"attandees/admin_message.html")

def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    dict = {

        'total_course': QMODEL.Course.objects.all().count(),
        'total_question': QMODEL.Question.objects.all().count(),
        'total_student': SMODEL.Student.objects.all().count()
    }
    return render(request, 'teacher/teacher_dashboard.html', staff_detials(request, 'Dashboard', dict))

 
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    return render(request, 'teacher/teacher_exam.html', staff_detials(request, 'Manage Marks'))


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_exam_view(request):
    courseForm = QFORM.CourseForm()
    if request.method == 'POST':
        courseForm = QFORM.CourseForm(request.POST)
        if courseForm.is_valid():
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-exam')
    return render(request, 'teacher/teacher_add_exam.html', staff_detials(request,'Add Course',{'courseForm': courseForm}))


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_exam_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'teacher/teacher_view_exam.html', staff_detials(request,'View Course',{'courses': courses}))


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_exam_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')


@login_required(login_url='adminlogin')
def teacher_question_view(request):
    return render(request, 'teacher/teacher_question.html', staff_detials(request, 'Manage Mcq'))


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_question_view(request):
    questionForm = QFORM.QuestionForm()
    if request.method == 'POST':
        questionForm = QFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            course = QMODEL.Course.objects.get(id=request.POST.get('courseID'))
            question.course = course
            question.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-question')
    return render(request, 'teacher/teacher_add_question.html', staff_detials(request,'Add Question',{'questionForm': questionForm}))


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_question_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'teacher/teacher_view_question.html', staff_detials(request,'View Question',{'courses': courses}))


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_question_view(request, pk):
    questions = QMODEL.Question.objects.all().filter(course_id=pk)
    return render(request, 'teacher/see_question.html', staff_detials(request,'See Questions',{'questions': questions})) 


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def remove_question_view(request, pk):
    question = QMODEL.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/teacher/teacher-view-question')

from base import models as TMODEL
from base import models as SMODEL
from base import models
from ..models import Department

# --------------------------
def Personal_detials(request):
    usr_id = request.user.id
    usr_obj = User.objects.get(id=usr_id)
    faculty_details = Faculty_details.objects.get(mail=usr_obj.username)
    # request and get datas ..............
    role = Users.objects.get(mail_id=usr_obj.username)
    id_number = request.POST.get('idcard')
    name1 = request.POST.get('F_name')
    name2 = request.POST.get('surname')
    name = name1+' '+name2
    designation = request.POST.get('designation')
    department = request.POST.get('department')
    experience = request.POST.get('experience')
    qualififcation = request.POST.get('qualififcation')
    assessment_period = request.POST.get('AP')
    date_of_join = request.POST.get('date')
    bio = request.POST.get('about')
    d = date_of_join.split("-")
    date_formate = datetime.date(int(d[0]), int(d[1]), int(d[2]))
    my_uploaded_file = request.FILES['file_upload']
    print(date_of_join)
    usr_id = request.user.id
    usr_obj = User.objects.get(id=usr_id)
    edit = Faculty_details.objects.get(mail=usr_obj.username)
    print(edit.mail)
    edit.role = role
    edit.name = name 
    edit.id_number = id_number
    edit.designation = designation
    edit.department = department
    edit.experience = experience
    edit.qualififcation = qualififcation
    edit.assessment_period = assessment_period
    edit.date_of_join = date_formate
    edit.image = my_uploaded_file
    edit.bio = bio
    edit.save()
    usr_id = request.user.id
    usr_obj = User.objects.get(id=usr_id)
    name = Users.objects.get(user_name=usr_obj.username)
    faculty_details = Faculty_details.objects.get(user_name=name.user_name)
    department = Department.objects.all()
    context = {
        'total_student': SMODEL.Student.objects.all().count(),
        'total_teacher': TMODEL.Teacher.objects.filter(status=True,role="staff").count(),
        'total_course': models.NoteCourse.objects.all().count(),
        'user_name': usr_obj.username, 'detials': faculty_details,
        'name_s': faculty_details.name.split(' '),
        'rolenum':name.role,
        'department':department,
        'user_name': usr_obj.username, 'detials': faculty_details
    }
    return render(request, "home/staff.html", context)
