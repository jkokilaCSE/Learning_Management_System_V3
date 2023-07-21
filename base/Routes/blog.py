from base.models import blog, Draft_blog, Teacher
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .Tool.blogTool import get_blog, get_course, get_blog_by_cat,get_blog_by_cat1, get_draft_blog, get_course_review, get_draft_blog_by_cat, get_draft_blog_unreview
from .Tool.Tools import student_detials, staff_detials
from django.http import JsonResponse

# ...............Blog........................................
def blog_edit(request):
    return render(request, "blog/blog_edit.html", student_detials(request, 'Create Blog'))


def staff_create_blog(request):
    return render(request, "blog/staff_blog_create.html", staff_detials(request, 'Create Blog'))


def admin_create_blog(request):
    return render(request, "blog/admin_blog_create.html", staff_detials(request,'Create Blog',{'page': 'Create Blog'}))

 
def save_blog(request):
    ids = ['#title', '#description', '#content', '#Category', '#Thumbnail']

    title = request.POST.get(ids[0])
    description = request.POST.get(ids[1])
    content = request.POST.get(ids[2])
    Category = request.POST.get(ids[3])
    Thumbnail = request.POST.get(ids[4])
    blog_type = request.POST.get('#type_')
    action = request.POST.get('#action')
    
    if title and description and content and Category and Thumbnail :
        print("action : ",action)
        if action == 'Save and Publish':
            obj = Draft_blog(title=title, userid=request.user.id, blog_type=blog_type, description=description, content=content,
                    categories=Category, blog_profile_img=Thumbnail,reviewed=False,Submitreview=True)
            obj.save()
            response_data = {'status': 'success', 'message': 'Blog published successfully'}
        elif action == 'Save Draft':
            print("Submitreview False")
            obj = Draft_blog(title=title, userid=request.user.id, blog_type=blog_type, description=description, content=content,
                    categories=Category, blog_profile_img=Thumbnail,reviewed=False,Submitreview=False)
            obj.save()
            response_data = {'status': 'success', 'message': 'Blog draft saved successfully'}
        else:
            response_data = {'status': 'error', 'message': 'Invalid action'}
    else:
        response_data = {'status': 'err', 'message': 'Please Provide the all of details'}
    
    return JsonResponse(response_data)

def blog_saved(request):
    return render(request,'attandees/Blog_Saved.html')

def blog_draft_saved(request):
    return render(request,'attandees/Blog_draft_Saved.html',staff_detials(request,"Draft Articals"))

def st_blog_draft_saved(request):
    return render(request,'attandees/st_Blog_draft_Saved.html',student_detials(request,"Draft Articals"))

def list_draft_blog(request):
    obj =  get_draft_blog(request)
    return render(request,"blog/draft_blog.html",staff_detials(request,'Drafted Blog',{"obj":obj}))

def st_list_draft_blog(request):
    obj =  get_draft_blog(request)
    return render(request,"blog/st_draft_blog.html",student_detials(request,'Drafted Blog',{"obj":obj}))

def list_unrevied_draft_blog(request):
    obj =  get_draft_blog_unreview(request)
    print(obj)
    return render(request,"blog/blog_review.html",staff_detials(request,'drafted blog',{"obj":obj}))

def save_edit_blog(request, pk):
    ids = ['#title', '#description', '#content', '#Category', '#Thumbnail']
    title = request.POST.get(ids[0])
    description = request.POST.get(ids[1])
    content = request.POST.get(ids[2])
    Category = request.POST.get(ids[3])
    Thumbnail = request.POST.get(ids[4])
    blog_type = request.POST.get('#type_')
    action = request.POST.get('#action')
    
    if title and description and content and Category and Thumbnail :
        print("action : ",action)
        if action == 'Save and Publish':
            obj = Draft_blog.objects.get(id=pk)
            obj.content = content
            obj.blog_type=blog_type
            obj.title = title
            obj.description = description
            obj.categories = Category
            obj.blog_profile_img = Thumbnail
            obj.reviewed=False
            obj.Submitreview=True
            obj.save()
            response_data = {'status': 'success', 'message': 'Blog published successfully'}
        elif action == 'Save Draft':
            print("Submitreview False")
            obj = Draft_blog.objects.get(id=pk)
            obj.content = content
            obj.blog_type=blog_type
            obj.title = title
            obj.description = description
            obj.categories = Category
            obj.blog_profile_img = Thumbnail
            obj.reviewed=False
            obj.Submitreview=False
            obj.save()

            print("Saved...........")
            
            response_data = {'status': 'success', 'message': 'Blog draft saved successfully'}
        else:
            response_data = {'status': 'error', 'message': 'Invalid action'}
    else:
        response_data = {'status': 'err', 'message': 'Please Provide the all of details'}



    response_data = {'status': 'success', 'message': 'Blog draft saved successfully'}
    return JsonResponse(response_data) 


def draft_save_blog(request, pk):
    ids = ['#title', '#description', '#content', '#Category', '#Thumbnail']
    title = request.POST.get(ids[0])
    description = request.POST.get(ids[1])
    content = request.POST.get(ids[2])
    Category = request.POST.get(ids[3])
    Thumbnail = request.POST.get(ids[4])

    obj = blog.objects.get(id=pk)
    obj.content = content
    obj.title = title
    obj.description = description
    obj.categories = Category
    obj.blog_profile_img = Thumbnail
    obj.save()

    print("Saved...........")

    return render(request, "blog/blog_edit.html")

def student_list_blog(request):
    items = get_blog()
    return render(request, "blog/studentblog.html", student_detials(request, 'Blog', {'blogs': items}))


def staff_list_blog(request):
    items = get_blog()
    return render(request, "blog/staffblog.html", staff_detials(request, 'Blog', {'blogs': items}))


def admin_list_blog(request):
    items = get_blog()
    return render(request, "blog/adminblog.html", staff_detials(request,'Blog List',{'page': 'Blog', 'blogs': items}))


def admin_list_blog_course(request):
    items = get_course()
    return render(request, "blog/adminblog.html", staff_detials(request,'Blog List',{'page': 'Course', 'blogs': items}))

def review_list_blog(request):
    items = get_course_review(request)
    print(items)
    return render(request, "blog/blog_review.html", staff_detials(request,'Blog List',{'page': 'Review Blog', 'blogs': items}))

def accept_the_art(request,id):
    obj = Draft_blog.objects.get(id=id)
    return render(request,"attandees/blog_accept.html",{"obj" : obj})
    
def reject_the_art(request,id):
    obj = Draft_blog.objects.get(id=id)
    return render(request,"attandees/reject_the_art.html",{"obj" : obj})

def reject_blog(request,id):
    obj = Draft_blog.objects.get(id=id)
    obj.delete()
    return redirect('review_list_blog')

def accept_the_art_Db(request,id):
    print("worked")
    obj = Draft_blog.objects.get(id=id)
    create = blog(title=obj.title, userid=obj.userid, blog_type=obj.blog_type, description=obj.description, content=obj.content,
                categories=obj.categories, blog_profile_img=obj.blog_profile_img,reviewed_by=request.user.id)
    create.save()
    obj.delete()
    return redirect("admin_list_blog_course")
    

def student_list_blog_course(request):
    items = get_course()
    return render(request, "blog/studentblog.html", student_detials(request, 'Blog', {'blogs': items}))


def staff_list_blog_course(request):
    items = get_course()
    return render(request, "blog/staffblog.html", staff_detials(request, 'Course', {'blogs': items}))


def view_blog(request, pk):
    page = blog.objects.get(id=pk)
    items = get_blog_by_cat1().remove(page) if page in get_blog_by_cat1() else get_blog_by_cat1()
    print(items)
    try:
        Teacher.objects.get(user=User.objects.get(id=request.user.id))
        return render(request, "blog/view_blog.html", {'blog': page, 'item': items, 'role':1})
    except:
        return render(request, "blog/view_blog.html", {'blog': page, 'item': items,'role':0})
        
def list_cat_blog(request,cat):
    page = blog.objects.filter(categories=cat)
    return render(request,'blog/cat_blog.html',{'page':page})

def draft_view_blog(request, pk):
    page = Draft_blog.objects.get(id=pk)
    items = get_draft_blog_by_cat(page.categories,request).remove(page) if page in get_draft_blog_by_cat(
        page.categories, request) else get_draft_blog_by_cat(page.categories, request)
    return render(request, "blog/view_blog.html", {'blog': page, 'item': items})


def delete_blog(request):
    bl_id = request.GET.get("id")
    page = blog.objects.get(id=bl_id)
    page.delete()
    return render(request, "blog/view_blog.html", {'blog': page})


@login_required(login_url='/FourNotFout')
def list_edit_blog(request):
    items = get_blog()
    return render(request, "blog/edit_blog_list.html", staff_detials(request, 'Manage Blog', {'blogs': items}))


def admin_list_edit_blog(request):
    items = get_blog()
    return render(request, "blog/edit_blog_list.html", staff_detials(request,"blog",{'page': 'Manage Blog', 'blogs': items}))


def edit_blog(request, pk):
    obj = blog.objects.get(id=pk)
    return render(request, "blog/blog_re_edit.html", {'obj': obj})

def draft_edit_blog(request, pk):
    obj = Draft_blog.objects.get(id=pk)
    return render(request, "blog/blog_re_edit.html", {'obj': obj})

def teacher_list_blog(request):
    items = get_blog()
    return render(request, "blog/teacherblog.html", {'blogs': items})






