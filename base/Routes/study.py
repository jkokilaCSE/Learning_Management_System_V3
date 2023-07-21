import requests
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Users,Department,Internal_test_mark,Sec_Daily_test_mark,Upload_Assignment,ClassRooms,Daily_test_mark, YouTubeLink,  Assignment, Student, Faculty_details, Internal_test_mark, Course, Sec_Daily_test_mark, Room, ClassRooms, class_enrolled, NoteCourse, Attendees, Student, Teacher, EbookForClass, daily_test
from django.contrib.auth.models import User
from .Tool.Tools import get_user_mail, get_user_name, get_user_role, get_user_obj, get_user_name_byid
import datetime
from datetime import datetime
from .Tool.Code_scriping_Tool import get_image_url
from .Forms.Notes_form import EbookClassForm
from base import models as TMODEL
from django.utils import timezone
from googlesearch import search
import urllib.parse
from django.db.models import Sum, Max
from django.http import JsonResponse
from random import choice
from django.db.models import Count
from dateutil import rrule
import xlwt
from io import BytesIO
from base.export import Internal_test_markResource
from .Tool.Tools import student_detials, staff_detials
from django.core.mail import send_mail
from django.conf import settings
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dateutil.relativedelta import relativedelta
import openpyxl
from django.http import HttpResponse
from io import BytesIO

def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_admin(user):
    obj = User.objects.get(id=user.id)
    get_role = Users.objects.get(user_name=obj.username)
    if get_role.role == 1:
        return True

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def leave_classroom(request,class_id,owner):
    if owner == 1:
        Assignment.objects.filter(class_id=class_id).delete()
        YouTubeLink.objects.filter(class_id=class_id).delete()
        Daily_test_mark.objects.filter(class_id=class_id).delete()
        Sec_Daily_test_mark.objects.filter(class_id=class_id).delete()
        Internal_test_mark.objects.filter(class_id=class_id).delete()
        ClassRooms.objects.get(subject_code=class_id).delete()
    else:
        a = class_enrolled.objects.get(user_id=request.user.id,class_id=class_id)
        a.delete()
        
    return render(request,"msg/leave_class.html")

def nave_home_classroom(request, pk, class_id):
    if pk == "join":
        try:
            if class_enrolled.objects.filter(user_id=request.user.id, subject_code=class_id).exists():
                print("connection passed...")
            else:
                class_en = class_enrolled(
                    user_id=request.user.id, mail_id=get_user_mail(request), subject_code=class_id)
                class_en.save()
        except:
            if class_enrolled.objects.filter(user_id=request.user.id, subject_code=class_id).exists():
                print("connection passed...")
            else:
                class_en = class_enrolled(
                    user_id=request.user.id, mail_id=request.user.username, subject_code=class_id)
                class_en.save()
        peoples = []
        people = class_enrolled.objects.filter(subject_code=class_id)
        for i in people:
            print(i.class_id, i.mail_id)
            person_obj = User.objects.get(id=i.user_id)
            try:
                obj = Student.objects.get(user=person_obj)
                print(obj.role_no)
                peoples.append(obj)
            except:
                pass
                # obj = Teacher.objects.get(user=person_obj) if database are clear it will work properly
                # print(obj.role)
        try:
            detials = ClassRooms.objects.get(subject_code=class_id)
        except:
            try:
                Teacher.objects.get(user=User.objects.get(id=request.user.id))
                return render(request,'msg/staff_class_404.html')
            except:
                return render(request,'msg/std_class_404.html')

        # create new chat room..........

        if Room.objects.filter(name=class_id).exists():
            return render(request, 'class_room/class_joinned.html', {'people': peoples, "detail": detials})
        else:
            new_room = Room.objects.create(name=class_id)
            new_room.save()
            return render(request, 'class_room/class_joinned.html', {'people': peoples, "detail": detials})
    elif pk == "attendes":
        peoples = []
        people = class_enrolled.objects.filter(subject_code=class_id)
        for i in people:
            print(i.class_id, i.mail_id)
            person_obj = User.objects.get(id=i.user_id)
            try:
                obj = Student.objects.get(user=person_obj)
                print(obj.role_no)
                peoples.append(obj)
            except:
                pass
                # obj = Teacher.objects.get(user=person_obj) if database are clear it will work properly
                # print(obj.role)
        detials = ClassRooms.objects.get(subject_code=class_id)
        # print("users", [str(i.username) for i in peoples])
        return render(request, 'class_room/attendes.html', staff_detials(request,'Attendes',{'people': [[j, i] for i, j in enumerate(peoples)], "ids": [str(i.id) for i in peoples], "detail": detials, "date": datetime.now().date()}))
    else:
        peoples = []
        people = class_enrolled.objects.filter(subject_code=class_id)
        test = class_enrolled.objects.all()
        detials = ClassRooms.objects.get(subject_code=class_id)
        obj = User.objects.get(id=request.user.id)
        get_role = Users.objects.get(user_name=obj.username)
        for i in test:
            print(i.class_id, i.mail_id, i.subject_code)
        for i in people:
            print(i.class_id, i.mail_id, i.subject_code)
            person_obj = User.objects.get(id=i.user_id)
            try:
                obj = Student.objects.get(user=person_obj)
                print(obj.role_no)
                peoples.append(obj)
            except:
                pass
        books = EbookForClass.objects.filter(Class_id=class_id)
        
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
        table_datas = Assignment.objects.filter(class_id=class_id)[::-1]
        try:
            updated_by = [get_user_name_byid(i.update_by) for i in table_datas]
        except:
            updated_by=[]
            # updated_by = [get_user_name_byid(i.update_by) for i in table_datas]
            
        collected = []
        status_data = []
        notes = []
        for i in table_datas:
            try:
                datas = Upload_Assignment.objects.filter(Assignment_id=i.id)
                notes.append(datas)
                user_count = Upload_Assignment.objects.filter(Assignment_id=i.id).values('update_by').distinct().count()
                collected.append(user_count)
                print("user_count",user_count)
                if len(peoples) == 0:
                    status_data.append(False)
                elif len(peoples) <= user_count:
                    status_data.append(True)
                else:
                    if len(peoples) == 0:
                        status_data.append(False)
                    elif len(peoples) <= user_count:
                        status_data.append(True)
                    else:
                        status_data.append(False)
            except:
                user_count = Upload_Assignment.objects.filter(Assignment_id=i.id).values('update_by').distinct().count()
                notes.append(None)
                print("Error occered.....!")
                collected.append(0)
                if len(peoples) == 0:
                    status_data.append(False)
                elif len(peoples) <= user_count:
                    status_data.append(True)
                else:
                    status_data.append(False)
            
        empty = True if len(table_datas)>0 else False
                
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                
        if is_student(request.user):
            obj = User.objects.get(id=request.user.id)
            student_data = Student.objects.get(user=obj)
            if Room.objects.filter(name=class_id).exists():
                return render(request, 'class_room/student_class_room.html', {'student_data': student_data, 'people': peoples, "detail": detials, 'books': books, 'recent_books': books[::-1][0:4],'table_datas':zip(table_datas,updated_by,collected,status_data,notes)})
            else:
                new_room = Room.objects.create(name=class_id)
                new_room.save()
                return render(request, 'class_room/student_class_room.html', {'student_data': student_data, 'people': peoples, "detail": detials, 'books': books, 'recent_books': books[::-1][0:4],'table_datas':zip(table_datas,updated_by,collected,status_data,notes)})

        elif is_teacher(request.user):
            print("Teacher are worrking...")
            accountapproval = TMODEL.Teacher.objects.all().filter(
                user_id=request.user.id, status=True)
            if accountapproval:
                print('accountapproval are working...')
                if Room.objects.filter(name=class_id).exists():
                    print("now working...")
                    return render(request, 'class_room/staff_class_room.html', staff_detials(request,'classRoom',{'people': peoples, "detail": detials, 'books': books, 'recent_books': books[::-1][0:4],'table_datas':zip(table_datas,updated_by,collected,status_data),"empty":empty}))
                else:
                    new_room = Room.objects.create(name=class_id)
                    new_room.save()
                    return render(request, 'class_room/staff_class_room.html', staff_detials(request,'Classroom created',{'people': peoples, "detail": detials, 'books': books, 'recent_books': books[::-1][0:4],'table_datas':zip(table_datas,updated_by,collected,status_data),"empty":empty}))
            else:
                return render(request, 'teacher/teacher_wait_for_approval.html')
        if get_role.role == 1:
            return render(request, 'class_room/staff_class_room.html', {'people': peoples, "detail": detials, 'books': books, 'recent_books': books[::-1][0:4],'table_datas':zip(table_datas,updated_by,collected,status_data),"empty":empty})
        if get_role.role == 3:
            return render(request, 'class_room/staff_class_room.html', {'people': peoples, "detail": detials, 'books': books, 'recent_books': books[::-1][0:4],'table_datas':zip(table_datas,updated_by,collected,status_data),"empty":empty})
        else:
            if Room.objects.filter(name=class_id).exists():
                return render(request, 'class_room/student_class_room.html', {'people': peoples, "detail": detials, 'books': books, 'recent_books': books[::-1][0:4],'table_datas':zip(table_datas,updated_by,collected,status_data),"empty":empty})
            else:
                new_room = Room.objects.create(name=class_id)
                new_room.save()
                return render(request, 'class_room/student_class_room.html', {'people': peoples, "detail": detials, 'books': books, 'recent_books': books[::-1][0:4],'table_datas':zip(table_datas,updated_by,collected,status_data),"empty":empty})


def home_classroom(request):
    classes = []
    img = {}
    dep = []
    sem = [1, 2, 3, 4, 5, 6, 7, 8]
    try:
        enroll_classes = class_enrolled.objects.filter(
            mail_id=get_user_mail(request))
        print(get_user_mail(request),
              "this is only passed now............\n\n\n\n\n\n\n\n")
    except:
        enroll_classes = class_enrolled.objects.filter(
            mail_id=request.user.email)
        print(str(request.user.email), "this is only passed now............\n\n\n\n\n\n\n\n",
              request.user.email)

    for i in enroll_classes:
        classrooms = ClassRooms.objects.filter(subject_code=i.subject_code)
        print(i.class_id)
        print(classrooms)
        for i in classrooms:
            print(i.id, i.class_name)
            classes.append(i)
            if i.department not in dep:
                dep.append(i.department)
    if is_student(request.user):
        print("It's Student Login......")
        classes = []
        classes_img = []
        try:
            enroll_classes = class_enrolled.objects.filter(
                mail_id=get_user_mail(request))
            print(get_user_mail(request),
                  "this is only passed now............\n\n\n\n\n\n\n\n")
        except:
            enroll_classes = class_enrolled.objects.filter(
                mail_id=request.user.username)

        def get_emails_for_class(class_id):
            # get all instances of the class_enrolled model with the given class_id
            class_enrollments = class_enrolled.objects.filter(
                class_id=class_id)
            # create a list to hold the email IDs
            emails = []
            # iterate over the class_enrollments and add each mail_id to the emails list
            for enrollment in class_enrollments:
                emails.append(enrollment.mail_id)
            # return the list of email IDs
            return emails

        for i in enroll_classes:
            classrooms = ClassRooms.objects.filter(subject_code=i.subject_code)
            for i in classrooms:
                classes.append(i)
                if i.department not in dep:
                    dep.append(i.department)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> get images >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        class_es = []
        for i in classes:
            class_enrollments = class_enrolled.objects.get(
                class_id=i.id)
            class_es.append(class_enrollments)

        img = []
        peoples = []
        temp = []
        for j, i in enumerate(class_es):
            peoples.append(temp)
            temp = []
            print("sub : ", i.subject_code)
            people = class_enrolled.objects.filter(
                subject_code=i.subject_code)
            print('people : ', peoples)
            for i in people:
                person_obj = User.objects.get(id=i.user_id)
                try:
                    obj = Student.objects.get(user=person_obj)
                    temp.append(obj)
                except Exception as e:
                    print(e)
        peoples.append(temp)
        peoples.pop(0)
        temp_people = []
        # ------------------------------------------ to manage the 4 peoples -----------------------------
        for i, j in enumerate(peoples):
            if len(j) >= 4:
                temp_people.append(j)
            else:
                temp_people.append(j[0:4])
        peoples = temp_people
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        obj = User.objects.get(id=request.user.id)
        student_data = Student.objects.get(user=obj)
        try:
            if len(classes) == 0:
                return render(request, 'class_room/no_classes.html')
            else:
                return render(request, 'class_room/student_classroom.html', {'student_data': student_data, 'classes': [[i, j] for i, j in zip(classes, peoples)], 'img': img, 'sem_': sem, 'dep': dep, "user_name": get_user_name(request), "User_role": get_user_role(request), "usr_img": get_user_obj(request)})
        except:
            if len(classes) == 0:
                return render(request, 'class_room/no_classes.html',student_detials(request,"Class Not Enrolled"))
            else:
                return render(request, 'class_room/student_classroom.html', {'student_data': student_data, 'classes': [[i, j] for i, j in zip(classes, peoples)], 'img': img, 'sem_': sem, 'dep': dep, "user_name": request.user.username})
    elif is_teacher(request.user):
        obj = User.objects.get(id=request.user.id)
        teacher_data = Teacher.objects.get(user=obj)
        
        teacher_data_1 = Faculty_details.objects.get(user_name=obj.username)
        
        get_role = Users.objects.get(user_name=obj.username)
        accountapproval = TMODEL.Teacher.objects.all().filter(
            user_id=request.user.id, status=True)
        
        if accountapproval:
            print('department',teacher_data.department)
            
            classrooms = ClassRooms.objects.filter(department=teacher_data.department)
            
            all_classroom = ClassRooms.objects.all()
            
            print(get_role.role, type(get_role.role))
            try:
                if get_role.role == 2:
                    peoples = []
                    temp = []
                    for j, i in enumerate(classrooms):
                        peoples.append(temp)
                        temp = []
                        print("sub : ", i.subject_code)
                        people = class_enrolled.objects.filter(
                            subject_code=i.subject_code)
                        print('people : ', peoples)
                        for i in people:
                            person_obj = User.objects.get(id=i.user_id)
                            try:
                                obj = Student.objects.get(user=person_obj)
                                temp.append(obj)
                            except Exception as e:
                                print(e)
                    peoples.append(temp)
                    peoples.pop(0)
                    temp_people = []
                    # ------------------------------------------ to manage the 4 peoples -----------------------------
                    for i, j in enumerate(peoples):
                        if len(j) >= 4:
                            temp_people.append(j)
                        else:
                            temp_people.append(j[0:4])
                    peoples = temp_people
                    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    
                    return render(request, 'class_room/staff_classroom.html', staff_detials(request,'ClassRoom',{'detail': teacher_data_1, 'teacher_obj':teacher_data , 'teacher_data': teacher_data, 'classes': [[i, j] for i, j in zip(classrooms, peoples)], 'img': img, 'sem_': sem, 'dep': [teacher_data.department], "user_name": get_user_name(request), "User_role": get_user_role(request), "usr_img": get_user_obj(request)}))
                if get_role.role == 3:
                    peoples = []
                    temp = []
                    for j, i in enumerate(classes):
                        peoples.append(temp)
                        temp = []
                        print("sub : ", i.subject_code)
                        people = class_enrolled.objects.filter(
                            subject_code=i.subject_code)
                        print('people : ', peoples)
                        for i in people:
                            person_obj = User.objects.get(id=i.user_id)
                            try:
                                obj = Student.objects.get(user=person_obj)
                                temp.append(obj)
                            except Exception as e:
                                print(e)
                    peoples.append(temp)
                    peoples.pop(0)
                    temp_people = []
                    # ------------------------------------------ to manage the 4 peoples -----------------------------
                    for i, j in enumerate(peoples):
                        if len(j) >= 4:
                            temp_people.append(j)
                        else:
                            temp_people.append(j[0:4])
                    peoples = temp_people
                    return render(request, 'class_room/staff_classroom.html', staff_detials(request,'ClassRoom',{'detail': teacher_data_1, 'teacher_obj':teacher_data , 'teacher_data': teacher_data, 'classes':  [[i, j] for i, j in zip(classes, peoples)], 'img': img, 'sem_': sem, 'dep': dep, "user_name": get_user_name(request), "User_role": get_user_role(request), "usr_img": get_user_obj(request)}))
                if get_role.role == 1:
                    peoples = []
                    temp = []
                    for j, i in enumerate(all_classroom):
                        peoples.append(temp)
                        temp = []
                        print("sub : ", i.subject_code)
                        people = class_enrolled.objects.filter(
                            subject_code=i.subject_code)
                        print('people : ', peoples)
                        for i in people:
                            person_obj = User.objects.get(id=i.user_id)
                            try:
                                obj = Student.objects.get(user=person_obj)
                                temp.append(obj)
                            except Exception as e:
                                print(e)
                    peoples.append(temp)
                    peoples.pop(0)
                    temp_people = []
                    # ------------------------------------------ to manage the 4 peoples -----------------------------
                    for i, j in enumerate(peoples):
                        if len(j) >= 4:
                            temp_people.append(j)
                        else:
                            temp_people.append(j[0:4])
                    peoples = temp_people
                    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    
                    return render(request, 'class_room/staff_classroom.html', staff_detials(request,'ClassRoom',{'detail': teacher_data_1, 'teacher_obj':teacher_data , 'teacher_data': teacher_data, 'classes': [[i, j] for i, j in zip(all_classroom, peoples)], 'img': img, 'sem_': sem, 'dep': dep, "user_name": get_user_name(request), "User_role": get_user_role(request), "usr_img": get_user_obj(request)}))
            except:
                if get_role.role == 2:
                    return render(request, 'class_room/staff_classroom.html', {'teacher_data': teacher_data,'teacher_obj':teacher_data , 'classes': classrooms, 'img': img, 'sem_': sem, 'dep': [teacher_data.department], "user_name": request.user.username})
                if get_role.role == 3:
                    return render(request, 'class_room/staff_classroom.html', {'teacher_data': teacher_data,'teacher_obj':teacher_data , 'classes': classes, 'img': img, 'sem_': sem, 'dep': dep, "user_name": request.user.username})
                if get_role.role == 1:
                    return render(request, 'class_room/staff_classroom.html', {'teacher_data': teacher_data,'teacher_obj':teacher_data , 'classes': all_classroom, 'img': img, 'sem_': sem, 'dep': dep, "user_name": request.user.username})
        else:
            return render(request, 'teacher/teacher_wait_for_approval.html')
    else:
       if get_role.role == 1:
            return render(request, 'class_room/staff_classroom.html', {'teacher_data': teacher_data, 'classes': all_classroom, 'img': img, 'sem_': sem, 'dep': dep, "user_name": request.user.username})


def Class_msg(request):
    return render(request, 'class_room/no_classes.html')

def add_class(request):
    courses = Department.objects.all()
    return render(request, 'class_room/new_add.html',staff_detials(request, 'Add New Class',{"course":courses}))


def delete_class(request, room):
    class_room = ClassRooms.objects.get(id=room)
    class_room.delete()
    return render(request, 'class_room/new_add.html')

def class_added(request):
    return render(request,'attandees/class_added.html')

def save_add_class(request):
    class_name = request.POST.get('class_name')
    subject_code = request.POST.get('subject_code')
    department = request.POST.get('department')
    semester = request.POST.get('semester')
    discription = request.POST.get('discription')
    ctype = request.POST.get('type')
    try:
        class_room = ClassRooms(class_type=ctype,class_image=choice(get_image_url(class_name+" logos")), class_name=class_name, subject_code=subject_code,
                                department=department, semester=semester, discription=discription, owner=Faculty_details.objects.get(mail=get_user_mail(request)))
        class_room.save()
    except:
        return render(request,'msg/subject_code_unique.html')
    class_id = ClassRooms.objects.get(subject_code=subject_code)
    enroll_class = class_enrolled(
        user_id=request.user.id, mail_id=request.user.username, subject_code=subject_code, class_id=class_id.id)
    enroll_class.save()

    return redirect('class_added')


def edit_classroom(request, classroom_id):
    # Retrieve the classroom object from the database
    classroom = get_object_or_404(ClassRooms, subject_code=classroom_id)
    obj = Department.objects.all()
    if request.method == 'POST':
        # Retrieve the updated data from the HTML form
        classroom.class_name = request.POST.get('class_name')
        classroom.subject_code = request.POST.get('subject_code')
        classroom.semester = request.POST.get('semester')
        classroom.department = request.POST.get('department')
        classroom.discription = request.POST.get('discription')
        classroom.class_image = request.POST.get('image_url')

        # Save the updated data to the database
        classroom.save()

        # Redirect to the detail view of the updated classroom
        return render(request, 'msg/class_edited.html')

    # If the request method is not POST, render the edit form with the current data
    # return render(request, 'class_room/edit_class.html', {'classroom': classroom})
    return render(request,'class_room/edit_class.html',staff_detials(request,'Edit Classroom',{'classroom': classroom,'dep':obj}))


def attendes(request):
    return render(request, 'class_room/attendes.html',staff_detials(request,'Update Attendes'))

def attendes_error(request):
    return render(request,'attandees/message.html')

def attendes_added(request):
    return render(request,'msg/attendes_updated.html')

def no_usr_exit(request):
    return render(request,'msg/no_usr_exit.html')

def update_attendes(request):
    my_date_time = timezone.now()
    data: str = []
    print("length is : ", request.POST.get('length'))
    if request.POST.get('length') == '0':
        print("runned")
        return JsonResponse({"status":"no_usr","msg":"Empty Users"})
        
    for i in range(int(request.POST.get('length'))):
        datas = request.POST.get('#cars'+str(i))
        data.append(datas)
    for i in data:
        splited = i.split('~~')
        print(i.split('~~'), i)
        if Attendees.objects.filter(class_id=splited[2], roll_no=splited[3], Date=my_date_time).exists():
            print("Data Already Exists....")
            return JsonResponse({"redirect": 1})
            # return render(request,'attandees/message.html',{'message':'Data Already Exists..!','url':[" {% url 'teacher-dashboard' %}","{% url 'class_room' %}"],'btn':['Dashboard','ClassRoom Dashboard']})
        else :
            if splited[0] == "Absent":
                # date
                today = date.today()
                # Set start_date to the beginning of the current month
                start_date = today.replace(day=1)
                # Set end_date to today's date
                end_date = today
                c_attendees = Attendees.objects.filter(class_id=splited[2], Date__range=[start_date, end_date])
                total_count = c_attendees.filter(class_id=splited[2]).values('Date').distinct().count()
                c_attendee = Attendees.objects.get(roll_no=splited[3])
                current_month = (c_attendee.subject_states.count('Present') / total_count) * 100 # im
                no_of_days = c_attendee.subject_states.count('Present')
                # Calculate the start_date of the previous month
                start_date = today.replace(day=1) - relativedelta(months=1)
                # Calculate the end_date of the previous month
                end_date = start_date + relativedelta(day=31)
                attendees = Attendees.objects.filter(class_id=splited[2], Date__range=[start_date, end_date])
                total_count = attendees.filter(class_id=splited[2]).values('Date').distinct().count()
                attendee = Attendees.objects.get(roll_no=splited[3],class_id=splited[2])
                try:
                    prev_month = (attendee.subject_states.count('Present') / total_count) * 100 # im
                except:
                    prev_month = 0
                obje = Student.objects.get(role_no=splited[3])
                sender_email = settings.EMAIL_HOST_USER
                password = settings.EMAIL_HOST_PASSWORD
                message = MIMEMultipart("alternative")
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
                server.ehlo()
                server.login(sender_email, password)
                subject = f'Absence Notification ({today}) - {obje.get_name} from JEC'
                
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ["glorysherin22@gmail.com"]
                
                class_obj = ClassRooms.objects.get(subject_code=splited[2])
                queryset = Internal_test_mark.objects.filter(
                    roll_no=splited[3]
                ).order_by('-Date').order_by('-assesment_no')

                year = request.GET.get('year')
                if year:
                    start_date = datetime.strptime(f"{year}-01-01", "%Y-%m-%d").date()
                    end_date = datetime.strptime(f"{year}-12-31", "%Y-%m-%d").date()

                    queryset = queryset.filter(
                        Date__range=(start_date, end_date)
                    )

                # Generate HTML table with inline styles
                html_table = '<table style="width: 100%; border-collapse: collapse;">'
                html_table += '<thead><tr><th style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd; background-color: #f2f2f2;">ID</th><th style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd; background-color: #f2f2f2;">Class ID</th><th style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd; background-color: #f2f2f2;">Roll No</th><th style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd; background-color: #f2f2f2;">Subject</th><th style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd; background-color: #f2f2f2;">Mark</th><th style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd; background-color: #f2f2f2;">Assessment No</th><th style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd; background-color: #f2f2f2;">Date</th></tr></thead>'
                html_table += '<tbody>'
                for item in queryset:
                    html_table += f'<tr><td style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd;">{item.id}</td><td style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd;">{item.class_id}</td><td style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd;">{item.roll_no}</td><td style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd;">{item.subject}</td><td style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd;">{item.mark}</td><td style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd;">{item.assesment_no}</td><td style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd;">{item.Date}</td></tr>'
                html_table += '</tbody>'
                html_table += '</table>'
                
                # send_mail( subject, message, email_from, recipient_list )
                from django.core.mail import EmailMultiAlternatives
                
                html_content = f"""

<!-- email_template.html -->
<!DOCTYPE html>
<html>
<head>
    <style>
        /* Add your custom CSS styles here */
    </style>
</head>
<body>
    <p>Dear Parent,</p>
    <p>
        I hope this email finds you well. I am writing to inform you that your child, { obje.get_name }, was absent from college today.
    </p>
    <p>
        <strong>Reason for Absence (if known):</strong> 
    </p>
    <p>
        <strong>Absence Today:</strong> I would like to inform you that your child was absent from college today. The reason for their absence, if known, is illness, personal reasons, etc.
        We understand that occasional absences may occur due to unforeseen circumstances, and we appreciate your prompt communication regarding your child's absence.
        If there are any extenuating circumstances or if your child requires any academic support to catch up on missed work, please let us know, and we will be happy to assist.
    </p>
    <p>
        <strong>Attendance Percentage:</strong> Your child, { obje.get_name }, has maintained a regular presence in the college. The attendance percentage for the current academic month is { current_month }%.
    </p>
    <p>
        <strong>Number of Working Days:</strong> During the past month, our college had a total of { total_count } working days.
        I am pleased to inform you that your child attended { no_of_days } days out of these, which demonstrates their dedication towards their studies.
    </p>
    <p>
        <strong>Last Month Attendance Percentage:</strong> In the previous month, { obje.get_name } achieved an attendance percentage of { prev_month }%.
    </p>
    <p>
        <strong>Test Marks:</strong> Regarding academic performance, I am delighted to share that { obje.get_name } 
        Their test marks demonstrate a thorough understanding of the subjects and reflect their consistent efforts and hard work.
    </p>
    <h2>Internal Test Mark :</h2>
    {html_table}
    <p>
        Should you have any concerns or queries regarding your child's progress or any other matter, please do not hesitate to reach out to us.
        We are always here to provide guidance and support.
    </p>
    <p>
        Thank you for your understanding and cooperation.
    </p>
    <p>
        Warm regards,
        <br>
        { class_obj.owner.name }
        <br>
        { class_obj.department }
        <br>
        Jaya Engineering College
    </p>
</body>
</html>
"""
                
                text_content = 'JEC Site'  
                email = EmailMultiAlternatives(subject, text_content, email_from, [obje.parent_mail_id])
                email.attach_alternative(html_content, "text/html")
                email.send()
        
                
        for i in Attendees.objects.all():
            print(i.user_name, i.subject_states)
        obj = Attendees(
                class_id=splited[2], user_name=splited[1], subject_states=splited[0], roll_no=splited[3]
            )
        obj.save()
        print("Attendees Updated")
    return JsonResponse({"status":"sucess"})


def update_edited_attendes(request):
    print("running..... update data")
    date = request.POST.get('date')
    print(request.POST.get('date'))
    my_date=datetime.strptime(date, '%Y-%m-%d').date()
    print("my date : ",my_date)
    data: str = []
    print("length is : ", request.POST.get('length'))
    for i in range(int(request.POST.get('length'))):
        datas = request.POST.get('#cars'+str(i))
        data.append(datas)
    for i in data:
        splited = i.split('~~')
        print(i.split('~~'), i)
        obj = Attendees.objects.get(
            class_id=splited[2], roll_no=splited[3], Date=my_date)
        print('obj',obj)
       
        obj.subject_states = splited[0]
        obj.save()
        print(obj.class_id, obj.subject_states)
        print("updated....")
        print(
            f"states : states-{splited[0]}, classid = {splited[2]},roll_no:{splited[3]}")
    return render(request, 'attandees/attendes_alert.html',{'message':'Attendees are updated sucessfully...!'})

def message_possitive(request):
    return render(request,'attandees/attendes_alert.html',{'message':'Attendees are updated sucessfully...!'})

def edit_attendes_home(request):
    return render(request, 'class_room/edit_attendes_home.html',staff_detials(request,'Edit Attendes'))

from django.http import HttpResponse
from base.export import AttendeesResource

def edit_attendes(request):
    class_id = request.GET.get('class_id')
    date = request.GET.get('date')
    action = request.GET.get('action')
    if action == 'filter':
        print(class_id,date)
        for i in Attendees.objects.all():
            print(i.class_id, f"[{i.Date}]", i.user_name)
        attendees = Attendees.objects.filter(class_id=class_id, Date=date)
        context = {'attendees': [[i, j] for i, j in enumerate(attendees)],'date':date}
        print(context)
        return render(request, 'class_room/edit_attendes.html',staff_detials(request,'Edit Attendes',context))

    elif action == 'download':
        # Get the attendees queryset
        attendees = Attendees.objects.filter(class_id=class_id, Date=date)

        # Generate the export data
        resource = AttendeesResource()
        data = resource.export(attendees)

        # Create a response with the rendered data as a file
        response = HttpResponse(data.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="upload_assignments.xls"'

        return response
    


def view_attendes(request):
    class_id = request.GET.get('class_id')
    date = request.GET.get('date')
    action = request.GET.get('action')
    attendees = Attendees.objects.filter(class_id=class_id, Date=date)
    context = {'attendees': attendees}
    if action == 'filter':
        for i in Attendees.objects.all():
            print(i.class_id, f"[{i.Date}]", i.user_name, i.subject_states)
        attendees = Attendees.objects.filter(class_id=class_id, Date=date)
        context = {'attendees': attendees}
    elif action == 'download':
        # Get the attendees queryset
        attendees = Attendees.objects.filter(class_id=class_id, Date=date)

        # Generate the export data
        resource = AttendeesResource()
        data = resource.export(attendees)

        # Create a response with the rendered data as a file
        response = HttpResponse(data.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="upload_assignments.xls"'

        return response
    return render(request, 'class_room/sample.html',staff_detials(request,'View Attendes', context))
    

def add_class_notes(request, pk):
    if request.method == 'POST':
        form = EbookClassForm(request.POST, request.FILES)
        if form.is_valid():
            ebook = form.save(commit=False)
            ebook.Class_id = pk
            ebook.cover_image = choice(get_image_url(str(ebook.title)+" cover image"))
            ebook.save()
            return redirect('course_list')
    else:
        form = EbookClassForm()
    return render(request, 'class_room/notes/add_notes.html', staff_detials(request,'Add Notes',{'form': form, 'class_id': pk}))


def class_ebook_edit(request, pk):
    ebook = get_object_or_404(EbookForClass, pk=pk)
    if request.method == 'POST':
        form = EbookClassForm(request.POST, request.FILES, instance=ebook)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = EbookClassForm(instance=ebook)
    return render(request, 'class_room/notes/ebook_edit.html', {'form': form})


def class_ebook_delete(request, pk):
    ebook = get_object_or_404(EbookForClass, pk=pk)
    ebook.delete()
    return redirect('course_list')


def class_book_list(request):
    books = EbookForClass.objects.all()
    return render(request, 'class_room/notes/ebook_list.html', {'books': books})


def mark(request, class_id):
    peoples = []
    people = class_enrolled.objects.filter(subject_code=class_id)
    for i in people:
        print(i.class_id, i.mail_id)
        person_obj = User.objects.get(id=i.user_id)
        try:
            obj = Student.objects.get(user=person_obj)
            print(obj.role_no)
            peoples.append(obj)
        except:
            pass
    detials = ClassRooms.objects.get(subject_code=class_id)
    courses = NoteCourse.objects.all()
    return render(request, "class_room/add_mark.html", staff_detials(request,'Update Daily Test',{'courses': courses, 'people': [[j, i] for i, j in enumerate(peoples)], "ids": [str(i.id) for i in peoples], "detail": detials, "date": datetime.now().date()}))


def update_mark(request):
    my_date_time = request.POST.get('#date')
    data: str = []
    for i in range(int(request.POST.get('length'))):
        datas = request.POST.get('#cars'+str(i))
        data.append(datas)
    for i in data:
        splited = i.split('~~')
        print(i.split('~~'), i)
        print(request.POST.get('#course'), my_date_time)
        if Sec_Daily_test_mark.objects.filter(class_id=splited[2], roll_no=splited[3], Date=my_date_time).exists():
            print("Data Already Exists....")
        else:
            obj = Sec_Daily_test_mark(
                class_id=splited[2], user_name=splited[1], mark=splited[0], roll_no=splited[3], Date=my_date_time, subject=request.POST.get(
                    '#course')
            )
            obj.save()
    return render(request, 'class_room/attendes.html',staff_detials(request,'Update mark'))


def edit_mark_home(request):
    return render(request, 'class_room/edit_mark_home.html',staff_detials(request,'Edit Mark Home'))


def edit_mark(request):
    class_id = request.GET.get('class_id')
    date = request.GET.get('date')
    for i in Sec_Daily_test_mark.objects.all():
        print(i.class_id, f"[{i.Date}]", i.user_name)
    attendees = Sec_Daily_test_mark.objects.filter(
        class_id=class_id, Date=date)
    courses = NoteCourse.objects.all()
    context = {'attendees': [[i, j]
                             for i, j in enumerate(attendees)], 'courses': courses, 'date': date}
    print(context)
    return render(request, 'msg/mark_edited.html')


def update_edited_mark(request):
    print("running..... update data")
    data: str = []
    print("length is : ", request.POST.get('length'))

    for i in range(int(request.POST.get('length'))):
        datas = request.POST.get('#cars'+str(i))
        data.append(datas)
    for i in data:
        splited = i.split('~~')
        print(i.split('~~'), i)
        obj = Sec_Daily_test_mark.objects.get(
            class_id=splited[2], roll_no=splited[3], user_name=splited[1], Date=request.POST.get('#date'))
        obj.mark = splited[0]
        obj.subject = request.POST.get('#course')
        obj.save()
    return render(request, 'class_room/edit_mark.html')


def add_test_marks(request, class_id):
    if request.method == 'POST':
        for i in range(int(request.POST.get('num_rows'))):
            class_id = request.POST.get('class_id_' + str(i))
            ass_no = request.POST.get('ass_no_' + str(i))
            roll_no = request.POST.get('roll_no_' + str(i))
            subject = request.POST.get('subject_' + str(i))
            mark = request.POST.get('mark_' + str(i))
            date = request.POST.get('date_' + str(i))
            daily_test = Internal_test_mark(
                class_id=class_id, assesment_no=ass_no, roll_no=roll_no, subject=subject, mark=mark, Date=date)
            daily_test.save()
        print(class_id)
        return redirect('test_marks', class_id=request.POST.get('class_id_'+str(0)))
   
    peoples = []
    people = class_enrolled.objects.filter(subject_code=class_id)
    test = class_enrolled.objects.all()
    for i in test:
        print(i.class_id, i.mail_id, i.subject_code)
    for i in people:
        print(i.class_id, i.mail_id, i.subject_code)
        person_obj = User.objects.get(id=i.user_id)
        try:
            obj = Student.objects.get(user=person_obj.id)
            print(obj.role_no)
            peoples.append(obj)
        except:
            pass
    sub = NoteCourse.objects.all()
    print("sub", sub)
    context ={'class_id': class_id, 'subjects': sub, 'comp': [[i, j] for i, j in enumerate(peoples)]}
    return render(request, 'class_room/add_test_marks.html', staff_detials(request,'Update mark',context))
  
def test_marks(request, class_id):
    
    if request.method == 'POST':
        test_marks = Internal_test_mark.objects.filter(class_id=class_id).order_by('roll_no').order_by('assesment_no')
        # Create the workbook and worksheet
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Test Marks')

        # Write the headers
        headers = ['#', 'Roll No', 'Name', 'Assessment No', 'Subject', 'Mark', 'Date']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        # Write the data rows
        row = 1
        current_assessment_no = None
        print([[ j, Student.objects.filter(role_no=j.roll_no)[0].get_name] for i, j in enumerate(test_marks)])
        for mark,name in [[ j, Student.objects.filter(role_no=j.roll_no)[0].get_name] for i, j in enumerate(test_marks)]:
            if mark.assesment_no != current_assessment_no:
                if current_assessment_no is not None:
                    # Add two empty lines between different assessment numbers
                    row += 2
                current_assessment_no = mark.assesment_no

            worksheet.write(row, 0, row)
            worksheet.write(row, 1, mark.roll_no)
            worksheet.write(row, 2, name if name else '')
            worksheet.write(row, 3, mark.assesment_no if mark.assesment_no else '')
            worksheet.write(row, 4, mark.subject)
            worksheet.write(row, 5, mark.Date.strftime('%Y-%m-%d'))
            worksheet.write(row, 6, mark.mark)

            row += 1

        # Create a response with the workbook data as a file
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="test_marks.xls"'
        workbook.save(response)

        return response
        
    peoples = []
    people = class_enrolled.objects.filter(subject_code=class_id)
    for i in people:
        person_obj = User.objects.get(id=i.user_id)
        try:
            obj = Student.objects.get(user=person_obj.id)
            peoples.append(obj)
        except:
            pass
    test_marks = Internal_test_mark.objects.filter(class_id=class_id).order_by('roll_no').order_by('assesment_no')
    
    test_marks_ass = Internal_test_mark.objects.filter(class_id=class_id).values('assesment_no').distinct()
    print(test_marks)
   
    return render(request, 'class_room/test_marks.html',staff_detials(request,'Add test Mark', {'test_marks_ass':[ i['assesment_no'] for i in test_marks_ass],'class_id': class_id, 'test_marks': [[i, j, Student.objects.filter(role_no=j.roll_no)[0].get_name] for i, j in enumerate(test_marks)], 'students': peoples}))


def edit_test_marks(request, class_id, sub, ass_no):
    if request.method == 'POST':
        for i in range(int(request.POST.get('num_rows'))):
            test = Internal_test_mark.objects.get(
                id=request.POST.get('test_id_' + str(i)))
            class_id = request.POST.get('class_id_' + str(i))
            ass_no = request.POST.get('ass_no_' + str(i))
            roll_no = request.POST.get('roll_no_' + str(i))
            subject = request.POST.get('subject_' + str(i))
            mark = request.POST.get('mark_' + str(i))
            date = request.POST.get('date_' + str(i))
            test.class_id = class_id
            test.assesment_no = ass_no
            test.roll_no = roll_no
            test.subject = subject
            test.mark = mark
            test.Date = date
            test.save()
        print(class_id)
        return redirect('test_marks', class_id=request.POST.get('class_id_'+str(0)))

    test = Internal_test_mark.objects.filter(
        class_id=class_id, subject=sub, assesment_no=ass_no)
    sub = NoteCourse.objects.all()

    return render(request, 'class_room/edit_test_mark.html',staff_detials(request,'Edit Test Mark', {'subjects': sub, 'class_id': class_id, 'comp': [[i, j] for i, j in enumerate(test)]}))


def marks_by_class(request, class_id):
    # retrieve all Sec_Daily_test_mark objects for the specified class
    marks = Sec_Daily_test_mark.objects.filter(class_id=class_id)

    # create a nested dictionary to store the marks by user and subject
    class_data = {}
    for mark in marks:
        user = mark.user_name
        subject = mark.subject
        if user and subject and mark.mark is not None:
            if user not in class_data:
                class_data[user] = {}
            if subject not in class_data[user]:
                class_data[user][subject] = []
            class_data[user][subject].append(mark)

    # pass the data to the template
    context = {'class_id': class_id, 'class_data': class_data}
    return render(request, 'class_room/daily_mark.html',staff_detials(request,'Marks By Class',context))


def user_marks(request, user_name):
    user_marks = Sec_Daily_test_mark.objects.filter(
        user_name=user_name).order_by('Date')
    user_subjects = set([mark.subject for mark in user_marks])
    context = {'user_marks': user_marks, 'user_subjects': user_subjects}
    return render(request, 'user_marks.html', context)


def show_actions(request, class_id):
    cls_obj = ClassRooms.objects.get(subject_code=class_id)
    return render(request, "class_room/action_options.html", staff_detials(request,'Mark Actions',{'class_obj': cls_obj,'class_id':class_id}))


def mark_option(request, class_id):
    cls_obj = ClassRooms.objects.get(subject_code=class_id)
    return render(request, "class_room/mark_option.html", staff_detials(request,'Mark Actions',{'class_obj': cls_obj}))


def attendes_option(request, class_id):
    cls_obj = ClassRooms.objects.get(subject_code=class_id)
    return render(request, "class_room/attendes_actions.html", staff_detials(request,'Attendes Options',{'class_obj': cls_obj}))

def attendes_option1(request, class_id):
    cls_obj = ClassRooms.objects.get(subject_code=class_id)
    return render(request, "class_room/attendes_actions1.html", staff_detials(request,'Attendes Options',{'class_obj': cls_obj}))


def Dailytest_marksby_date(request, user_name):
    # Retrieve all marks for the given user
    user_marks = Sec_Daily_test_mark.objects.filter(
        user_name=user_name).order_by('Date')

    # Get all unique dates for the retrieved marks
    dates = user_marks.values_list('Date', flat=True).distinct()

    # Get all unique subjects for the retrieved marks
    subjects = user_marks.values_list('subject', flat=True).distinct()

    # Generate HTML table
    table = '<table><thead><tr><th>Subject</th>'
    for date in dates:
        table += f'<th>{date}</th>'
    table += '</tr></thead><tbody>'
    for subject in subjects:
        table += f'<tr><td>{subject}</td>'
        for date in dates:
            try:
                mark = user_marks.get(subject=subject, Date=date).mark
                table += f'<td>{mark}</td>'
            except Sec_Daily_test_mark.DoesNotExist:
                table += '<td></td>'
        table += '</tr>'
    table += '</tbody></table>'

    context = {'marks_table': table}
    # return render(request, 'user_marks.html', context)
    return render(request, 'class_room/Dailytest_marksby_date.html', staff_detials(request,"Student Test Mark", context))


def list_user_for_mark(request, class_id):
    peoples = []
    people = class_enrolled.objects.filter(subject_code=class_id)
    test = class_enrolled.objects.all()
    for i in test:
        print(i.class_id, i.mail_id, i.subject_code)
    for i in people:
        print(i.class_id, i.mail_id, i.subject_code)
        person_obj = User.objects.get(id=i.user_id)
        try:
            obj = Student.objects.get(user=person_obj.id)
            print(obj.role_no)
            peoples.append(obj)
        except:
            pass
    return render(request, 'class_room/list_user_for_mark.html', staff_detials(request,'View students Mark',{'people': peoples}))


def user_mark_view(request, class_id):
    peoples = []
    people = class_enrolled.objects.filter(subject_code=class_id)
    test = class_enrolled.objects.all()
    sub = NoteCourse.objects.all()
    for i in test:
        print(i.class_id, i.mail_id, i.subject_code)
    for i in people:
        print(i.class_id, i.mail_id, i.subject_code)
        person_obj = User.objects.get(id=i.user_id)
        try:
            obj = Student.objects.get(user=person_obj.id)
            print(obj.role_no)
            peoples.append(obj)
        except:
            pass
    if request.method == 'POST':
        user_name = request.POST['user_name']
        date = request.POST['date']
        department = request.POST['department']
        if department == '':
            marks = Sec_Daily_test_mark.objects.filter(
                user_name=user_name, Date=date)
        else:
            marks = Sec_Daily_test_mark.objects.filter(
                user_name=user_name, Date=date, subject=department)
        context = {'marks': marks}
        return render(request, 'class_room/user_marks.html', context)
    return render(request, 'class_room/user_mark_form.html', staff_detials(request,'View Daily Test',{'people': peoples,"sub":sub}))


def get_internal_test_marks(request):
    class_id = request.GET.get('class_id')
    assesment_no = request.GET.get('assesment_no')
    date_str = request.GET.get('date')
    marks = None

    if class_id and assesment_no:
        marks = Internal_test_mark.objects.filter(
            class_id=class_id, assesment_no=assesment_no)

        if date_str:
            # Parse the date string to get the year
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            year = date.year

            # Filter marks based on year
            marks = marks.filter(Date__year=year)

    context = {
        'marks': marks,
        'class_id': class_id,
        'assesment_no': assesment_no,
        'date': date_str,
    }

    return render(request, 'class_room/internal_test_marks.html', staff_detials(request, 'Get Internal Test Mark', context))


def Dailystudenttest_marksby_date(request, user_name):
    # Retrieve all marks for the given user
    user_marks = Sec_Daily_test_mark.objects.filter(
        user_name=user_name).order_by('Date')

    # Get all unique dates for the retrieved marks
    dates = user_marks.values_list('Date', flat=True).distinct()

    # Get all unique subjects for the retrieved marks
    subjects = user_marks.values_list('subject', flat=True).distinct()

    # Generate HTML table
    table = '<table><thead><tr><th>Subject</th>'
    for date in dates:
        table += f'<th>{date}</th>'
    table += '</tr></thead><tbody>'
    for subject in subjects:
        table += f'<tr><td>{subject}</td>'
        for date in dates:
            try:
                mark = user_marks.get(subject=subject, Date=date).mark
                table += f'<td>{mark}</td>'
            except Sec_Daily_test_mark.DoesNotExist:
                table += '<td></td>'
        table += '</tr>'
    table += '</tbody></table>'

    context = {'marks_table': table}
    # return render(request, 'user_marks.html', context)
    return render(request, 'class_room/Dailystudenttest_marksby_date.html', context)


def ToDoList(request):
    print(student_detials(request, 'ToDo-List'))
    return render(request, "ToDoList/index.html", student_detials(request, 'ToDo-List'))


def staffToDoList(request):
    print(staff_detials(request, 'ToDo-List'))
    return render(request, "ToDoList/staff_index.html", staff_detials(request, 'ToDo-List'))


def student_mark_option(request, class_id):
    cls_obj = ClassRooms.objects.get(subject_code=class_id)
    return render(request, "class_room/student_mark_option.html", student_detials(request, 'Mark Options', {'class_obj': cls_obj}))


def student_get_mark(request, user_name):
    # Retrieve all marks for the given user
    user_marks = Sec_Daily_test_mark.objects.filter(
        roll_no=user_name).order_by('Date')

    # Get all unique dates for the retrieved marks
    dates = user_marks.values_list('Date', flat=True).distinct()

    # Get all unique subjects for the retrieved marks
    subjects = user_marks.values_list('subject', flat=True).distinct()

    # Generate HTML table
    table = '<table><thead><tr><th>Subject</th>'
    for date in dates:
        table += f'<th>{date}</th>'
    table += '</tr></thead><tbody>'
    for subject in subjects:
        table += f'<tr><td>{subject}</td>'
        for date in dates:
            try:
                mark = user_marks.filter(subject=subject, Date=date).mark
                table += f'<td>{mark}</td>'
            except Sec_Daily_test_mark.DoesNotExist:
                table += '<td></td>'
        table += '</tr>'
    table += '</tbody></table>'

    context = {'marks_table': table}
    # return render(request, 'user_marks.html', context)
    return render(request, 'class_room/get_test__mark.html', context)


def student_int_test_marks(request, roll_no):
    queryset = Internal_test_mark.objects.filter(
        roll_no=roll_no
    ).order_by('-assesment_no', '-Date')

    year = request.GET.get('year')
    if year:
        start_date = datetime.strptime(f"{year}-01-01", "%Y-%m-%d").date()
        end_date = datetime.strptime(f"{year}-12-31", "%Y-%m-%d").date()

        queryset = queryset.filter(
            Date__range=(start_date, end_date)
        )

    context = {
        'roll_no': roll_no,
        'queryset': queryset
    }

    return render(request, 'class_room/internal_test_mark_by_user.html', student_detials(request, 'Internal Test Mark', context))



import json
from datetime import date

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


def export_filtered_attendees(request):
    # Get the start date and end date from the request parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Filter the attendees based on the date range
    attendees = Attendees.objects.filter(Date__range=[start_date, end_date])

    # Create an Excel workbook and worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Attendees Data'

    # Write headers to the worksheet
    worksheet.append(['Date', 'Class ID', 'User Name', 'Roll No', 'Subject/State'])

    # Write attendees data to the worksheet
    for attendee in attendees:
        worksheet.append([attendee.Date, attendee.class_id, attendee.user_name, attendee.roll_no, attendee.subject_states])

    # Create a BytesIO object to store the Excel file in memory
    excel_file = BytesIO()

    # Save the workbook to the BytesIO object
    workbook.save(excel_file)

    # Set the response headers for Excel download
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=filtered_attendees.xlsx'

    # Write the Excel file from the BytesIO object to the response
    excel_file.seek(0)
    response.write(excel_file.read())

    return response


def view_attendees_by_roolno(request, roll_no):
    attendees = Attendees.objects.filter(roll_no=roll_no).order_by('-Date')

    attendees_list = []
    for attendee in attendees:
        attendee_dict = {
            'Date': attendee.Date,
            'subject_states': attendee.subject_states
        }
        attendees_list.append(attendee_dict)

    context = {
        'roll_no': roll_no,
        'attendees':attendees,
        'attendeesj': json.dumps(attendees_list, cls=CustomJSONEncoder),
    }
    return render(request, 'class_room/view_attendeesbyroolno.html', student_detials(request, 'View Attendence', context))

def course_material(request,class_id):
    return render(request,'class_room/course_material.html',staff_detials(request,'Course Material',{"class_id":class_id}))

def search_view(request):
    if request.method == 'GET':
        query = request.GET.get('google_search')
        if query:
            try:
                query = urllib.parse.quote(query)
                results = []
                for url in search(query, num_results=50):
                    # process the search results
                    results.append(url)
                return render(request, 'class_room/search_results.html', {'results': results, 'query': query})
            except:
                try:
                    Teacher.objects.get(user=User.objects.get(id=request.user.id))
                    return render(request, 'msg/search_404.html',{'role':1})
                except:
                    return render(request, 'msg/search_404.html',{'role':0})
    return render(request, 'class_room/search_results.html',staff_detials(request,'Search Results',))


def mark_list(request, roll_no):
    # retrieve all the unique dates for the specified roll number
    dates = Sec_Daily_test_mark.objects.filter(
        roll_no=roll_no
    ).values('Date').annotate(max_id=Max('id')).order_by('-Date').values_list('Date', flat=True)

    # create a dictionary to hold the marks for each date
    mark_dict = {}
    for query_date in dates:
        marks = Sec_Daily_test_mark.objects.filter(
            roll_no=roll_no,
            Date=query_date
        ).values('subject', 'mark')
        total_marks = marks.aggregate(Sum('mark'))['mark__sum']
        mark_dict[query_date] = {'marks': marks, 'total_marks': total_marks}

    context = {'roll_no': roll_no, 'mark_dict': mark_dict}
    return render(request, 'class_room/mark_list.html',student_detials(request,'Mark List', context))

def parent_session(request):
    return render(request,"")

def fournotfourerror(request, exception):
    return render(request,'error/404.html')

def fivehundrederror(request):
    return render(request,'error/500.html')

def studenterror(request):
    return render(request,'error/studenterror.html')

def stafferror(request):
    return render(request,'error/stafferror.html')

def adminerror(request):
    return render(request,'error/adminerror.html')

def fournotthree(request,exception):
    return render(request,'error/403.html')

def fourhundred(request, exception):
    return render(request,'error/400.html')

def view_attendees_by_roolno_graph(request, roll_no):
    attendees = Attendees.objects.filter(roll_no=roll_no).order_by('-Date')

    attendees_list = []
    for attendee in attendees:
        attendee_dict = {
            'Date': attendee.Date,
            'subject_states': attendee.subject_states
        }
        attendees_list.append(attendee_dict)

    context = {
        'roll_no': roll_no,
        'attendees':attendees,
        'attendeesj': json.dumps(attendees_list, cls=CustomJSONEncoder),
    }
    return render(request, 'class_room/graph_attendees.html', student_detials(request, 'View Attendence', context))

def view_attendees_by_roolno_percentage(request, roll_no):
    attendees = Attendees.objects.filter(roll_no=roll_no).order_by('-Date')
    attendees_list = []
    for attendee in attendees:
        attendee_dict = {
            'Date': attendee.Date,
            'subject_states': attendee.subject_states
        }
        attendees_list.append(attendee_dict)

    context = {
        'roll_no': roll_no, 
        'attendees':attendees,
        'attendeesj': json.dumps(attendees_list, cls=CustomJSONEncoder),
    }
    return render(request, 'class_room/percentage_attendees.html', student_detials(request, 'View Attendence', context))
def assignments(request):
    return render(request, 'teacher/assignments.html',staff_detials(request,'Assignment'))

from django.core import serializers

def filter_attendees(request):
    
    # Get the filter criteria from the request's GET parameters
    class_id = request.GET.get('class_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    action = request.GET.get('action')
    context = {}
    
    print("action",action)
    if action == 'Export':
    
        attendees = Attendees.objects.filter(class_id=class_id, Date__range=[start_date, end_date])

        # Calculate the counts and percentages
        total_count = attendees.filter(class_id=class_id).values('Date').distinct().count()

        present_count = attendees.filter(class_id=class_id,subject_states='Present').count()
        absent_count = attendees.filter(class_id=class_id,subject_states='Absent').count()
        on_duty_count = attendees.filter(class_id=class_id,subject_states='OnDuty').count()

        if total_count > 0:
            present_percentage = (present_count / total_count) * 100
            absent_percentage = (absent_count / total_count) * 100
            on_duty_percentage = (on_duty_count / total_count) * 100
        else:
            present_percentage = 0
            absent_percentage = 0
            on_duty_percentage = 0

        # Calculate the person percentages
        person_percentages = {}
        for attendee in attendees:
            person_percentage = (attendee.subject_states.count('Present') / total_count) * 100
            person_percentages[attendee.user_name] = person_percentage
            
        person_present_count = {}
        for attendee in attendees:
            if attendee.subject_states == 'Present':
                person_present_count[attendee.user_name] = person_present_count.get(attendee.user_name, 0) + 1

        # Create the workbook and worksheet
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Attendees')

        # Write the headers
        headers = ['ID', 'Class ID', 'User Name', 'Roll No', 'Subject States', 'Date', 'Person Percentage', 'Present Count']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        # Write the data rows
        for row, attendee in enumerate(attendees, start=1):
            worksheet.write(row, 0, attendee.id)
            worksheet.write(row, 1, attendee.class_id)
            worksheet.write(row, 2, attendee.user_name)
            worksheet.write(row, 3, attendee.roll_no)
            worksheet.write(row, 4, attendee.subject_states)
            worksheet.write(row, 5, attendee.Date.strftime('%Y-%m-%d'))
            worksheet.write(row, 6, person_percentages.get(attendee.user_name, 0))
            worksheet.write(row, 7, person_present_count.get(attendee.user_name, 0))

        # Write the total values
        total_row = len(attendees) + 2
        worksheet.write(total_row, 0, 'Total Classes')
        worksheet.write(total_row, 1, "present_count")
        worksheet.write(total_row, 2, "absent_count")
        worksheet.write(total_row, 3, "on_duty_count")
        worksheet.write(total_row, 4, "present_percentage")
        worksheet.write(total_row, 5, "absent_percentage")
        worksheet.write(total_row, 6, "on_duty_percentage")
        total_row = total_row +1
        worksheet.write(total_row, 0, total_count)
        worksheet.write(total_row, 1, present_count)
        worksheet.write(total_row, 2, absent_count)
        worksheet.write(total_row, 3, on_duty_count)
        worksheet.write(total_row, 4, present_percentage)
        worksheet.write(total_row, 5, absent_percentage)
        worksheet.write(total_row, 6, on_duty_percentage)

        # Create a BytesIO object to save the workbook
        output = BytesIO()
        workbook.save(output)

        # Create a response with the workbook data as a file
        response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="attendees_data.xls"'

        return response

    
    
    if action == 'Filter':
        # Filter the attendees based on the class_id and date range
        attendees = Attendees.objects.filter(class_id=class_id, Date__range=[start_date, end_date])
        attendees_json = serializers.serialize('json', attendees)
        # Calculate the count of present and absent attendees
        present_count = attendees.filter(subject_states='Present').count()
        absent_count = attendees.filter(subject_states='absent').count()

        # Calculate the total number of attendees
        total_count = attendees.filter(class_id=class_id).values('Date').distinct().count()


        person_present_count = {}
        for attendee in attendees:
            if attendee.subject_states == 'Present':
                person_present_count[attendee.user_name] = person_present_count.get(attendee.user_name, 0) + 1
        
        # Calculate the percentage of each person's attendance
        person_percentages = {}
        for attendee in attendees:
            person_percentage = (attendee.subject_states.count('Present') / total_count) * 100
            person_percentages[attendee.user_name] = person_percentage
            
            # Calculate the count of working days
        working_days = rrule.rrule(rrule.DAILY, dtstart=datetime.strptime(start_date, '%Y-%m-%d'),
                                until=datetime.strptime(end_date, '%Y-%m-%d'),
                                byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR))
        attendance_counts = []
        
        for i in Attendees.objects.all():
            print(i.subject_states)
        
        for day in working_days:
            count = Attendees.objects.filter(class_id=class_id, Date=day, subject_states='Present').count()
            attendance_counts.append(count)
            
        working_days_json = json.dumps([date.strftime('%Y-%m-%d') for date in working_days])
        working_days_count = rrule.rrule(rrule.DAILY, dtstart=datetime.strptime(start_date, '%Y-%m-%d'),
                                until=datetime.strptime(end_date, '%Y-%m-%d'),
                                byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR)).count()
        # Calculate the absent percentage for each working day
        total_count = attendees.count()
        absent_percentages = []
        for day in working_days:
            attendees_on_day = attendees.filter(Date=day)
            attendees_on_day_count = attendees_on_day.count()
            if attendees_on_day_count > 0:
                absent_count_on_day = attendees_on_day.filter(subject_states='absent').count()
                absent_percentage = (absent_count_on_day / attendees_on_day_count) * 100
            else:
                absent_percentage = 0
            absent_percentages.append(absent_percentage)
        # Calculate the total number of attendees
        context = {
            'attendees': attendees,
            'class_id': class_id,
            'start_date': start_date,
            'end_date': end_date,
            'present_count': present_count,
            'absent_count': absent_count,
            'person_percentages': person_percentages,
            'working_days': zip(working_days,attendance_counts),
            'working_days_count': working_days_count,
            'attendees_json': attendees_json,
            'working_days_json': working_days_json,
            'absent_percentages': absent_percentages
        }

    return render(request, 'class_room/filter_attendees.html', context)
