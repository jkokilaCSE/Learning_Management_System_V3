from django.urls import path, re_path
from LMS import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView, LoginView

from .Routes.common import *
from .Routes.Common_Tool import *
from .Routes.tool import *
from .Routes.parent import *
from .Routes.staff import *
from .Routes.department import *
from .Routes.students import *
from .Routes.study import *
from .Routes.notes import *
from .Routes.exam import *
from .Routes.blog import *
from .Routes.Events import *
from .Routes.home import *
from .Routes.CommonNotes import *
from .Routes.DynamicFunctionality import *
from .Routes.admin_page import *
from .Routes.staff_tools import *
from .Routes.NoCodeViews import *
from .Routes.manage_links import *
from .Routes.assignment import *
from .Routes.Upload_Assignment import *
from .Routes.compiler import *
from .Routes.social_link import *

# Initilizes........................

urlpatterns = []


def Make_Join(Componets):
    OutComponets = []
    for i in Componets:
        for j in i:
            OutComponets.append(j)
    return OutComponets

# Urls............................


tools = [
    path('Common_tool', Common_tool, name='Common_tool'),
    path('toolHome', toolHome, name='toolHome'),
    path('trans', translate_, name='trans'),
    path('convert_text', convert_text, name='convert_text'),
    path('wikipedia_summary', wikipedia_summary, name='wikipedia_summary'),
    path('convert_docx_to_pdf', convert_docx_to_pdf, name='convert_docx_to_pdf'),
    path('convert_pdf_to_docx', convert_pdf_to_docx, name='convert_pdf_to_docx'),
    path('convert_pdf_to_excel', convert_pdf_to_excel,
         name='convert_pdf_to_excel'),
    path('convert_excel_to_pdf', convert_excel_to_pdf,
         name='convert_excel_to_pdf'),
    path('convert_jpg_to_pdf', convert_jpg_to_pdf, name='convert_jpg_to_pdf'),
    path('convert_jpg_to_word', convert_jpg_to_word, name='convert_jpg_to_word'),
    path('calculator', calculator, name='calculator'),
    path('cgpa_calculator', cgpa_calculator, name='cgpa_calculator'),
    path('handwriting_converter', handwriting_converter,
         name='handwriting_converter'),
    path('keyword_to_image', keyword_to_image, name='keyword_to_image'),
    path('video_meeting/<str:room_id>', meeting, name='video_meeting'),
    path('staff_meeting/<str:room_id>', staff_meeting, name='staff_meeting'),
    path('admin_meeting/<str:room_id>', admin_meeting, name='admin_meeting'),
    path('join_meeting', join_meeting, name='join_meeting'),
    path('staff_join_meeting', staff_join_meeting, name='staff_join_meeting'),
    path('admin_join_meeting', admin_join_meeting, name='admin_join_meeting'),

    path('gpa_calculator', gpa_calculator, name='gpa_calculator'),
    path('get_subject', get_subject, name='get_subject'),
    path('Code_scriping', Code_scriping, name='Code_scriping'),
]
alternative_url = [path('student/video_meeting', meeting),
                   path('student/class_room', home_classroom),
                   path('student/chat_lobby', lobby),
                   path('student/list_blog', student_list_blog,name='list_blog'),
                   path('student/chat_home/', chat_home, name='chat_home'),
                   
                   path('student/note/notes_list',
                        notes_list, name='notes_list'),
                   path('student/note/std/notes_list',
                        student_notes_list, name='student_notes_list'),
                   path('staff/note/std/notes_list',
                        staff_notes_list, name='staff_notes_list'),
                   
                   path('student/toolHome', toolHome, name='toolHome'),
                   path('student/logout', LogoutView.as_view)

                   ]

common_tool = [
    path('Common_Common_tool', Common_Common_tool, name='Common_Common_tool'),
    path('Common_toolHome', Common_toolHome, name='Common_toolHome'),
    path('Common_trans', Common_translate_, name='Common_trans'),
    path('Common_convert_text', Common_convert_text, name='Common_convert_text'),
    path('Common_wikipedia_summary', Common_wikipedia_summary,
         name='Common_wikipedia_summary'),
    path('Common_convert_docx_to_pdf', Common_convert_docx_to_pdf,
         name='Common_convert_docx_to_pdf'),
    path('Common_convert_pdf_to_docx', Common_convert_pdf_to_docx,
         name='Common_convert_pdf_to_docx'),
    path('Common_convert_pdf_to_excel', Common_convert_pdf_to_excel,
         name='Common_convert_pdf_to_excel'),
    path('Common_convert_excel_to_pdf', Common_convert_excel_to_pdf,
         name='Common_convert_excel_to_pdf'),
    path('Common_convert_jpg_to_pdf', Common_convert_jpg_to_pdf,
         name='Common_convert_jpg_to_pdf'),
    path('Common_convert_jpg_to_word', Common_convert_jpg_to_word,
         name='Common_convert_jpg_to_word'),
    path('Common_calculator', Common_calculator, name='Common_calculator'),
    path('Common_cgpa_calculator', Common_cgpa_calculator,
         name='Common_cgpa_calculator'),
    path('Common_handwriting_converter', Common_handwriting_converter,
         name='Common_handwriting_converter'),
    path('Common_keyword_to_image', Common_keyword_to_image,
         name='Common_keyword_to_image'),
    path('Common_video_meeting', Common_video_meeting,
         name='Common_video_meeting'),

    path('Common_gpa_calculator', Common_gpa_calculator,
         name='Common_gpa_calculator'),
    path('Common_get_subject', Common_get_subject, name='Common_get_subject'),
    path('Common_Code_scriping', Common_Code_scriping,
         name='Common_Code_scriping'),
]

common = [
    path('', pre_home),
    path('pre_home', pre_home, name='pre_home'),
    path('student_home', student_home, name='student_home'),
    path('staff_home', staff_home, name='staff_home'),
    path('contactus', contactus),
    path('services', services),
    path('about', about, name='about'),
    path('parentsession', parentsession, name='parentsession'),
    path('personal_detials', Personal_detials, name='personal_detials'),
]

admin = [
    path('add_Faculty', add_faculty),
    path('teacher_list', teacher_list, name='teacher_list'),
    path('hod_list', hod_list, name='hod_list'),
    path('handle_toogle/<int:action>', handle_toogle, name='handle_toogle'),
    path('admin_list', admin_list, name='admin_list'),
    path('teacher_delete/<str:teacher_id>',
         teacher_delete, name='teacher_delete'),
    path('teacher_edit/<str:teacher_id>', teacher_edit, name='teacher_edit'),
    path('add_usr', add_usr),
    path('teachers', teachers),
    path('teacher/profile/<int:staff_id>',
         teacher_profile, name='teacher_profile'),
    path('class_list', class_list, name='class_list'),
    path('class_listout/<str:class_id>',
         get_class_peoples, name='class_listout'),
    path('students_list', students_list, name='students_list'),
    path('admin_students_list', admin_students_list, name='admin_students_list'), 
    path('students_list_by_dep', students_list_by_dep,
         name='students_list_by_dep'),
    path('class_dates', class_dates, name='class_dates'),

    path('class_dates/<int:id>/delete_attendee/', 
         delete_attendee, name='delete_attendee'),
    path('class_dates/<int:id>/edit_attendee/',
         edit_attendee, name='edit_attendee'),
    path('class_dates/<str:class_id>/<str:date>/user_details/',
         user_details, name='user_details'),
      path('manage_lms', manage_lms, name='manage_lms'),    
]


videochat = [
    path('chat_lobby', lobby),
    path('room/', video_chat_room),
    path('get_token/', getToken),

    path('create_member/', createMember),
    path('get_member/', getMember),
    path('delete_member/', deleteMember),
]


chatroom = [
    path('todolist', ToDoList, name='todolist'),
    path('staffToDoList', staffToDoList, name='staffToDoList'),
    path('chat_home/', chat_home, name='chat_home'),
    path('staff_chat_home/', staff_chat_home, name='staff_chat_home'),
    path('admin_chat_home', admin_chat_home, name='admin_chat_home'),
    # problem...................
    path('chat/<str:room>/', chat_room, name="chat_room"),
    path('staffchat/<str:room>/', staff_chat_room, name="staff_chat_room"),
    path('adminchat/<str:room>/', admin_chat_room, name="staff_chat_room"),
    path('chat_home/checkview', checkview, name="checkview"),
    path('chat_home/staff_checkview', staff_checkview, name="staff_checkview"),
    path('chat_home/admin_checkview', admin_checkview, name="admin_checkview"),
    path('chat_home/Ncheckview', Ncheckview, name="Ncheckview"),
    path('send', send, name="send"),
    path('getMessages/<str:room>/', getMessages, name="getMessages"),
]


classroom = [
   
    path('search_view', search_view, name='search_view'),
    path('course_material/<str:class_id>', course_material, name='course_material'),
    path('view_attendees_by_roolno/<int:roll_no>',
         view_attendees_by_roolno, name='view_attendees_by_roolno'),
    path('export_filtered_attendees/', export_filtered_attendees, name='export_filtered_attendees'),
    path('view_attendees_by_roolno_percentage/<int:roll_no>',
         view_attendees_by_roolno_percentage, name='view_attendees_by_roolno_percentage'),
    path('view_attendees_by_roolno_graph/<int:roll_no>',
         view_attendees_by_roolno_graph, name='view_attendees_by_roolno_graph'),
    path('student_int_test_marks/<int:roll_no>',
         student_int_test_marks, name='student_int_test_marks'),
    path('student_mark_option/<str:class_id>',
         student_mark_option, name='student_mark_option'),
    path('student_get_mark/<str:user_name>',
         student_get_mark, name='student_get_mark'),
    path('Dailystudenttest_marksby_date/<str:user_name>',
         Dailystudenttest_marksby_date, name='Dailystudenttest_marksby_date'),
    path('get_internal_test_marks',
         get_internal_test_marks, name='get_internal_test_marks'),
    path('user_mark_view/<str:class_id>',
         user_mark_view, name='user_mark_view'),
    path('Dailytest_marksby_date/<str:user_name>',
         Dailytest_marksby_date, name='Dailytest_marksby_date'),
    path('list_user_for_mark/<str:class_id>',
         list_user_for_mark, name='list_user_for_mark'),
    path('show_actions/<str:class_id>', show_actions, name='show_actions'),
    path('mark_option/<str:class_id>', mark_option, name='mark_option'),
    path('attendes_option/<str:class_id>',
         attendes_option, name='attendes_option'),
    path('attendes_option1/<str:class_id>',
         attendes_option1, name='attendes_option1'),
    path('note_by_class/<str:class_id>/', note_by_class, name='note_by_class'),
    path('note_by_class_staff/<str:class_id>/',
         note_by_class_staff, name='note_by_class_staff'),
    path('test_marks/<str:class_id>/', test_marks, name='test_marks'),
    path('add_test_marks/<str:class_id>',
         add_test_marks, name='add_test_marks'),
    path('edit_test_marks/<str:class_id>/<str:sub>/<int:ass_no>',
         edit_test_marks, name='edit_test_marks'),
    path('class_room', home_classroom, name='class_room'),
    path('message/<str:room>/', chatgetMessages, name="message"),
    path('classroom/<str:pk>/<str:class_id>', nave_home_classroom),
    path('add_class', add_class,name='add_class'),
    path('delete_class/<str:room>', delete_class),
    path("save_added_class", save_add_class),
    path("class_added", class_added,name="class_added"),
    path("edit_classroom/<str:classroom_id>",
         edit_classroom, name='edit_classroom'),
    path("attendes", attendes,name="attendes"),
    path("update_attendes", update_attendes, name='update_attendes'),
    path("mark_list/<str:roll_no>", mark_list, name='mark_list'),
    path("update_edited_attendes", update_edited_attendes),
    path("message_possitive", message_possitive,name="message_possitive"),
    path("edit_attendes_home", edit_attendes_home, name='edit_attendes_home'),
    path("view_attendes", view_attendes, name='view_attendes'),
    path("no_usr_exit", no_usr_exit, name='no_usr_exit'),
    path("attendes_added", attendes_added, name='attendes_added'),
    path("attendes_error", attendes_error, name='attendes_error'),
    path("edit_attendes", edit_attendes),
    path("mark/<str:class_id>", mark, name='mark'),
    path("update_marks", update_mark),
    path("edit_mark_home", edit_mark_home, name='edit_mark_home'),
    path("edit_mark", edit_mark,name="edit_mark"),
    path("update_edited_mark", update_edited_mark),
    path("marks_by_class/<str:class_id>",
         marks_by_class, name='marks_by_class'),
    path("add_class_notes/<str:pk>", add_class_notes,name="add_class_notes"),
    path('class_ebook/book_list', class_book_list, name='class_book_list'),
    path('class_ebook/<int:pk>/edit/', class_ebook_edit, name='class_ebook_edit'),
    path('class_ebook/<int:pk>/delete/',
         class_ebook_delete, name='class_ebook_delete'),
    path('filter_attendees', filter_attendees, name='filter_attendees'),
    path('leave_classroom/<str:class_id>', leave_classroom, name='leave_classroom'),

]


studet = [
    path('students_list', students_list, name='students_list'),
    path('students/<int:student_id>', student_profile, name='student_detail'),
    path('students_delete/<int:student_id>/delete',
         student_delete, name='student_delete'),

    path('student/<int:pk>/edit', student_edit, name='student_edit'),
    path('student/studentclick', studentclick_view),
    path('student/studentlogin',
         LoginView.as_view(template_name='student/studentlogin.html'), name='studentlogin'),
    path('student/studentsignup', student_signup_view, name='studentsignup'),
    path('student/student-dashboard',
         student_dashboard_view, name='student-dashboard'),
    path('student/student-exam', student_exam_view, name='student-exam'),
    path('student/take-exam/<int:pk>', take_exam_view, name='take-exam'),
    path('student/start-exam/<int:pk>', start_exam_view, name='start-exam'),
    path('student/calculate-marks', calculate_marks_view, name='calculate-marks'),
    path('student/view-result', view_result_view, name='view-result'),
    path('student/check-marks/<int:pk>', check_marks_view, name='check-marks'),
    path('student/student-marks', student_marks_view, name='student-marks'),
]

teacher = [
    path('teacher/teacherclick', teacherclick_view),
    path('staff/chat_lobby', staff_lobby, name='staff_chat_lobby'),
    path('staff_list_by_dep', staff_list_by_dep, name='staff_list_by_dep'),
    path('admin/chat_lobby', admin_lobby, name='admin_chat_lobby'),
    path('teacher/teacherlogin',
         LoginView.as_view(template_name='login/login.html'), name='teacherlogin'),
    
    
    path('teacher/addstudentlogin',
         LoginView.as_view(template_name='student/studentadded.html'), name='addstudentlogin'),
     # path('department/teacher/addstudentlogin',
     #     LoginView.as_view(template_name='student/studentadded.html'), name='addstudentlogin'),
     
     
    path('teacher/addstudentsignup', add_student_signup_view,
         name='add_student_signup_view'),
#     path('department/teacher/addstudentsignup', add_student_signup_view,
#          name='add_student_signup_view'),
    path('teacher/teachersignup', teacher_signup_view, name='teachersignup'),
    path('teacher/user_added_message', user_added_message, name='user_added_message'),
    path('user_added_message', user_added_message, name='user_added_message'),
    path('teacher/teachersignup1', teacher_signup_view1, name='teachersignup1'),
    path('teacher/admin_added', admin_added, name='admin_added'),
    path('teacher/adminsignup', adminsignup, name='adminsignup'),
    path('teacher/addadmin', add_admin, name='addadmin'),
    path('teacher/add_admin1', add_admin1, name='add_admin1'),
    path('teacher/teacher-dashboard',
         teacher_dashboard_view, name='teacher-dashboard'),
    path('teacher/teacher-exam', teacher_exam_view, name='teacher-exam'),
    path('teacher/teacher-add-exam',
         teacher_add_exam_view, name='teacher-add-exam'),
    path('teacher/teacher-view-exam',
         teacher_view_exam_view, name='teacher-view-exam'),
    path('teacher/delete-exam/<int:pk>', delete_exam_view, name='delete-exam'),
    path('teacher/teacher-question',
         teacher_question_view, name='teacher-question'),
    path('teacher/teacher-add-question',
         teacher_add_question_view, name='teacher-add-question'),
    path('teacher/teacher-view-question',
         teacher_view_question_view, name='teacher-view-question'),
    path('teacher/see-question/<int:pk>',
         see_question_view, name='see-question'),
    path('teacher/remove-question/<int:pk>',
         remove_question_view, name='remove-question'),
    path('teacher/assignments', assignments, name='assignments'),
    path('add_teacher_hod', add_teacher_hod, name='add_teacher_hod'),
    path('teacher_signup_viewhod', teacher_signup_viewhod, name='teacher_signup_viewhod'),
]

exam = [

    path('logout', LogoutView.as_view(
        template_name='exam/logout.html'), name='logout'),
    
    path('department/logout',  LogoutView.as_view(
        template_name='exam/logout.html'), name='logout'),
    path('contactus',  contactus_view),
    path('afterlogin',  afterlogin_view, name='afterlogin'),
    path('adminclick',  adminclick_view),
    path('adminlogin', LoginView.as_view(
        template_name='login/login.html'), name='adminlogin'),
    path('department/adminlogin', LoginView.as_view(
        template_name='login/login.html'), name='adminlogin'),
    path('admin-dashboard',  admin_dashboard_view, name='admin-dashboard'),
    path('admin-teacher',  admin_teacher_view, name='admin-teacher'),
    path('admin-view-teacher',  admin_view_teacher_view, name='admin-view-teacher'),
    path('update-teacher/<int:pk>',  update_teacher_view, name='update-teacher'),
    path('delete-teacher1/<int:pk>',  delete_teacher_view1, name='delete-teacher1'),
    path('delete-teacher/<int:pk>',  delete_teacher_view, name='delete-teacher'),
    path('admin-view-pending-teacher',  admin_view_pending_teacher_view,
         name='admin-view-pending-teacher'),
    path('admin-view-teacher-salary',  admin_view_teacher_salary_view,
         name='admin-view-teacher-salary'),
    path('approve-teacher/<int:pk>',
         approve_teacher_view, name='approve-teacher'),
    path('reject-teacher/<int:pk>',  reject_teacher_view, name='reject-teacher'),

    path('admin-student',  admin_student_view, name='admin-student'),
    path('admin-view-student',  admin_view_student_view, name='admin-view-student'),
    path('admin-view-student-marks',  admin_view_student_marks_view,
         name='admin-view-student-marks'),
    path('admin-view-marks/<int:pk>',
         admin_view_marks_view, name='admin-view-marks'),
    path('admin-check-marks/<int:pk>',
         admin_check_marks_view, name='admin-check-marks'),
    path('update-student/<int:pk>',  update_student_view, name='update-student'),
    path('delete-student/<int:pk>',  delete_student_view, name='delete-student'),

    path('admin-course',  admin_course_view, name='admin-course'),
    path('admin-add-course',  admin_add_course_view, name='admin-add-course'),
    path('admin-view-course',  admin_view_course_view, name='admin-view-course'), 
    path('delete-course/<int:pk>',  delete_course_view, name='delete-course'),

    path('admin-question',  admin_question_view, name='admin-question'),
    path('admin-add-question',  admin_add_question_view, name='admin-add-question'),
    path('admin-view-question',  admin_view_question_view,
         name='admin-view-question'),
    path('view-question/<int:pk>',  view_question_view, name='view-question'),
    path('delete-question/<int:pk>',
         delete_question_view, name='delete-question'),


]


blog_url = [
    path('student_list_blog_course',
         student_list_blog_course, name='student_list_blog_course'),
    path('staff_list_blog_course',
         staff_list_blog_course, name='staff_list_blog_course'),

    path('admin_list_blog_course',
         admin_list_blog_course, name='admin_list_blog_course'),
    path('admin_create_blog', admin_create_blog, name='admin_create_blog'),
    path('admin_list_blog', admin_list_blog, name='admin_list_blog'),

    path('list_blog', student_list_blog, name='student_list_blog'),
    path('staff_list_blog', staff_list_blog, name='staff_list_blog'),
    path('list_blog', teacher_list_blog, name='teacher_list_blog'),
    path('list_edit_blog', list_edit_blog, name='list_edit_blog'),
    path('admin_list_edit_blog', admin_list_edit_blog,
         name='admin_list_edit_blog'),
    path('view_blog/<str:pk>', view_blog, name='view_blog'),
    path('draft_view_blog/<str:pk>', draft_view_blog, name='draft_view_blog'),
    path('review_list_blog', review_list_blog, name='review_list_blog'),
    path('accept_the_art/<int:id>', accept_the_art, name='accept_the_art'),
    path('reject_the_art/<int:id>', reject_the_art, name='reject_the_art'),
    path('reject_blog/<int:id>', reject_blog, name='reject_blog'),
    path('accept_the_art_Db/<int:id>', accept_the_art_Db, name='accept_the_art_Db'),
    path('edit_blog/<str:pk>', edit_blog),
    path('draft_edit_blog/<str:pk>', draft_edit_blog),
    path('create_blog', blog_edit, name='create_blog'),
    path('staff_create_blog', staff_create_blog, name='staff_create_blog'),
    path('save_blog', save_blog),
    path('blog_draft_saved', blog_draft_saved,name="blog_draft_saved"),
    path('st_blog_draft_saved', st_blog_draft_saved,name="st_blog_draft_saved"),
    path('list_draft_blog', list_draft_blog,name="list_draft_blog"),
    path('st_list_draft_blog', st_list_draft_blog,name="st_list_draft_blog"),
    path('list_unrevied_draft_blog', list_unrevied_draft_blog,name="list_unrevied_draft_blog"),
    path('blog_saved', blog_saved,name="blog_saved"),
    path('delete_blog', delete_blog),
    path('edit_blog/save_edit_blog/<int:pk>', save_edit_blog,name="save_edit_blog"),
    path('edit_blog/draft_save_blog/<int:pk>', draft_save_blog),
]

gallery_ = [

    path("gallery", gallery),
    path('image_upload_page_gallery', image_upload_page_gallery,
         name='image_upload_page_gallery'),
    path('upload_image', upload_image),
    path('delete_image', delete_image),

]


note = [
    path('course_list', course_list, name='course_list'),
    path('course_edit/<int:pk>', course_edit, name='course_edit'),
    path('course_delete/<int:pk>', course_delete, name='course_delete'),
    path('course/<int:pk>/', course_detail, name='course_detail'),
    path('course/add/', course_add, name='course_add'),

    path('ebook/book_list/', book_list, name='book_list'),
    path('ebook/add/', ebook_add, name='ebook_add'),
    path('ebook/<int:pk>/edit/', ebook_edit, name='ebook_edit'),
    path('ebook/<int:pk>/delete/', ebook_delete, name='ebook_delete'),

    path('note/notes_list', notes_list, name='notes_list'),
    path('note/common_notes_list', common_notes_list, name='common_notes_list'),
    path('note/listout_notes', listout_notes, name='listout_notes'),
    path('note/<int:note_id>/', note_detail, name='note_detail'),
    path('note/create/', create_note, name='create_note'),
    path('note/<int:note_id>/update/', update_note, name='update_note'),
    path('note/<int:note_id>/delete/', delete_note, name='delete_note'),
]

event = [
    path('event_list', event_list, name='event_list'),
    path('event_add', event_add, name='event_add'),
    path('event_detail/<int:event_id>', event_detail, name='event_detail'),
    path('edit/<int:event_id>', event_edit, name='event_edit'),
    path('delete/<int:event_id>', event_delete, name='event_delete'),
    path('detail/<int:event_id>', event_detail, name='event_detail'),
]

dynamicFunctionality = [
    path('testimonicals_edit', Testimonicals_edit, name='testimonicals_edit'),
    path('testimonicals', Testimonicals, name='testimonicals'),
    path('testimonicals_save', Testimonicals_save, name='Testimonicals_save'),

]

AternativeUrls = [
    path('class_listout/<str:class_id>',
         get_class_peoples, name='class_listout'),
]

Staff_tool = [
    path('Staff_Staff_tool', Staff_Staff_tool),
    path('Staff_toolHome', Staff_toolHome),
    path('Staff_trans', Staff_translate_),
    path('Staff_convert_text', Staff_convert_text),
    path('Staff_wikipedia_summary', Staff_wikipedia_summary),
    path('Staff_convert_docx_to_pdf', Staff_convert_docx_to_pdf),
    path('Staff_convert_pdf_to_docx', Staff_convert_pdf_to_docx),
    path('Staff_convert_pdf_to_excel', Staff_convert_pdf_to_excel),
    path('Staff_convert_excel_to_pdf', Staff_convert_excel_to_pdf),
    path('Staff_convert_jpg_to_pdf', Staff_convert_jpg_to_pdf),
    path('Staff_convert_jpg_to_word', Staff_convert_jpg_to_word),
    path('Staff_calculator', Staff_calculator),
    path('Staff_cgpa_calculator', Staff_cgpa_calculator),
    path('Staff_handwriting_converter', Staff_handwriting_converter),
    path('Staff_keyword_to_image', Staff_keyword_to_image),
    path('Staff_video_meeting', Staff_video_meeting),

    path('Staff_gpa_calculator', Staff_gpa_calculator),
    path('Staff_get_subject', Staff_get_subject),
    path('Staff_Code_scriping', Staff_Code_scriping),
]

NoCodeMaker = [
    path('view_pages', index, name='view_pages'),
    path('add', addPage, name="addpage"),
    path('edit/<id>', editPage, name="editpage"),
    path('page/create', savePage, name="create_page"),
    path('editPage/<id>', editPageContent, name="editPageContent"),
    path('preview/<id>', previewPage, name='previewPage'),
    path('delete/<id>', deletePage, name='deletePage'),
    path('Own_Gpt', Own_Gpt, name='Own_Gpt'),
    path('savePage_download', savePage_download, name='savePage_download'),
    path('url', url, name='url'),
    path('edits', edits, name='edits'),
    path('Download_file', Download_file, name='Download_file'),
    path('ResumeBuilder', ResumeBuilder, name='ResumeBuilder'),
]

chatbot = [
    path('chatbot_res', chatbot_res,name="chatbot_res"),
    path('student/chatbot_res', chatbot_res),
    path('teacher/chatbot_res', chatbot_res),
]

department=[
    path('department_list', department_list, name='department_list'),
    path('department/<int:pk>/', department_detail, name='department_detail'),
    path('department/new', department_create, name='department_create'),
    path('department/<int:pk>/edit/', department_edit, name='department_edit'),
    path('department/<int:pk>/delete/', department_delete, name='department_delete'),
]

error=[
        path('fournotfourerror', fournotfourerror, name='fournotfourerror'),
        path('fivehundrederror',fivehundrederror,name='fivehundrederror'),
        path('studenterror',studenterror,name='studenterror'),
        path('stafferror',stafferror,name='stafferror'),
        path('adminerror',adminerror,name='adminerror'),
        path('fournotthree',fournotthree,name='fournotthree'),
        path('fourhundred',fourhundred,name='fourhundred'),
]

parent = [
     path('parent_home', parent_home, name='parent_home'),
     path('view_data/<int:roll_no>/<str:class_id>', view_data, name='view_data'),
     path('parent_class_list/<int:roll_no>', parent_class_list, name='parent_class_list'),
     path('parent_student_int_test_marks/<int:roll_no>/<str:class_id>', parent_student_int_test_marks, name='parent_student_int_test_marks'),
     path('parentmark_list/<int:roll_no>/<str:class_id>', parentmark_list, name='parentmark_list'),
     path('parentview_attendees_by_roolno/<int:roll_no>/<str:class_id>', parentview_attendees_by_roolno, name='parentview_attendees_by_roolno'),
     path('pview_attendees_by_roolno_graph/<int:roll_no>/<str:class_id>', pview_attendees_by_roolno_graph, name='pview_attendees_by_roolno_graph'),
     path('pview_attendees_by_roolno_percentage/<int:roll_no>/<str:class_id>', pview_attendees_by_roolno_percentage, name='pview_attendees_by_roolno_percentage'),
     path('pview_attendees_by_roolno_graph/<int:roll_no>/<str:class_id>', pview_attendees_by_roolno_graph, name='pview_attendees_by_roolno_graph'),
]

links_management = [
    path('links/add/<str:class_id>', add_youtube_link, name='add_youtube_link'),
    path('links/save/<str:class_id>', save_youtube_link, name='save_youtube_link'),
    path('links/list/<str:class_id>', list_youtube_links, name='list_youtube_links'),
    path('stdlinks/list/<str:class_id>', std_list_youtube_links, name='std_list_youtube_links'),
    path('links/edit/<int:pk>/<str:class_id>', edit_youtube_link, name='edit_youtube_link'),
    path('links/delete/<int:pk>/<str:class_id>', delete_youtube_link, name='delete_youtube_link'),
    path('list_notes/<str:class_id>', list_notes, name='list_notes'),
    path('st_list_notes/<str:class_id>', st_list_notes, name='st_list_notes'),
]

assignments_ = [
    path('assignments/list/<str:class_id>', assignment_list, name='assignment_list'),
    path('assignments/add/<str:class_id>', assignment_add, name='assignment_add'),
    path('assignments/edit/<int:pk>/<str:class_id>', assignment_edit, name='assignment_edit'),
    path('assignments/delete/<int:pk>/<str:class_id>', assignment_delete, name='assignment_delete'),
]

upload_assignments = [
    path('upload_assignment/<int:id>', staff_upload_assignment_create, name='upload_assignment_list'),
    path(r'^edit_assignment_mark/(?P<id>\d+)/(?P<a_id>True|False)/(?P<class_id>\w+)/(?P<student_id>\d+)/$', edit_assignment_mark, name='edit_assignment_mark'),
    re_path(r'^upload_assignment/(?P<id>\d+)/(?P<a_id>True|False)/(?P<class_id>\w+)/$', upload_assignment_list1, name='upload_assignment_list1'),
    re_path(r'^assignment_mark/(?P<id>\d+)/(?P<a_id>True|False)/(?P<class_id>\w+)/(?P<student_id>\d+)/$', assignment_mark, name='assignment_mark'),
    path('upload_assignment/create/<int:qst_id>', upload_assignment_create, name='upload_assignment_create'),
    re_path(r'^staff_upload_assignment_create/create/(?P<qst_id>\d+)/(?P<state>True|False)/(?P<class_id>\w+)/(?P<std>\d+)$', staff_upload_assignment_create, name='staff_upload_assignment_create'),
    path('upload_assignment/edit/<int:pk>', upload_assignment_edit, name='upload_assignment_edit'),
    path('upload_assignment/delete/<int:pk>/<int:qst_id>', upload_assignment_delete, name='upload_assignment_delete'),
]

compile = [
    path('compiler/', compiler_view, name='compiler')
    # Add other URL patterns as needed
]

social = [
    path('edit_social_media/<int:id>', edit_social_media, name='edit_social_media'),
    path('staff_edit_social_media', staff_edit_social_media, name='staff_edit_social_media'),
    path('classroom/join/', class_blank, name='class_blank'),
    
]

urlpatterns.extend(Make_Join([compile, social, upload_assignments, assignments_, links_management, parent,department,tools, chatbot, NoCodeMaker, common_tool, note, gallery_, blog_url, common, event,
                   admin, chatroom, classroom, videochat, studet, teacher, exam, dynamicFunctionality, alternative_url, Staff_tool,error]))

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)