from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import *
from django.template.loader import render_to_string
from django.http import JsonResponse, response, HttpResponse, HttpResponseRedirect
from django.db.models import Sum
from django.contrib import messages
from .forms import Course_Detail_Form


class BaseView(View):
    def get(self, request):
        return render(request, 'base.html')


class HomeView(View):
    def get(self, request):
        if request.user.groups.filter(name="Course Author Group").exists():
            admin_url = reverse('admin:index')
            return redirect(admin_url)

        categories = Categories.objects.all().order_by('id')[0:]
        course = Course.objects.filter(status='PUBLISH').order_by('-id')
        context = {"category": categories, "course": course}
        response = render(request, 'Main/home.html', context)
        response.delete_cookie('user_login_enrollment_msg')
        return response


def singlecourse(request):
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    FreeCourse_count = Course.objects.filter(price=0).count()
    PaidCourse_count = Course.objects.filter(price__gte=1).count()

    context = {
        'category': category,
        'level': level,
        'course': course,
        'FreeCourse_count': FreeCourse_count,
        'PaidCourse_count': PaidCourse_count,
    }
    return render(request, 'Main/singlecourse.html', context)


def filterdata(request):
    category = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')

    if price == ['PriceFree']:
        course = Course.objects.filter(price=0)
    elif price == ['PricePaid']:
        course = Course.objects.filter(price__gte=1)
    elif price == ['PriceAll']:
        course = Course.objects.all()
    elif category:
        course = Course.objects.filter(category__id__in=category).order_by('-id')
    elif level:
        course = Course.objects.filter(level__id__in=level).order_by('-id')
    else:
        course = Course.objects.all().order_by('-id')

    context = {
        'course': course
    }
    t = render_to_string('ajax/course.html', context)
    return JsonResponse({'data': t})


def contactus(request):
    category = Categories.get_all_category(Categories)

    context = {
        'category': category
    }
    return render(request, 'Main/contactus.html', context)


def aboutus(request):
    category = Categories.get_all_category(Categories)

    context = {
        'category': category
    }

    return render(request, 'Main/aboutus.html', context)


def searchcourse(request):
    category = Categories.get_all_category(Categories)

    query = request.GET['query']
    course = Course.objects.filter(title__icontains=query)
    context = {
        'course': course,
        'category': category,

    }
    return render(request, 'search/search.html', context)


def coursedetails(request, slug):
    category = Categories.get_all_category(Categories)
    time_duration = Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))
    course_id = Course.objects.get(slug=slug)
    # membership = request.user.groups.filter(name="gold members").exists()
    # print(membership)
    user_login_enrollment_msg = request.COOKIES.get('user_login_enrollment_msg')
    try:
        check_enroll = UserCourse.objects.get(user=request.user, course=course_id)
    except Exception as e:
        check_enroll = None

    course = Course.objects.filter(slug=slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')

    context = {
        'course': course,
        'category': category,
        'time_duration': time_duration,
        'enrol_status': check_enroll,
        # 'gold_member': membership,
        'user_login_enrollment_msg': user_login_enrollment_msg
    }
    return render(request, 'course/course_details.html', context)


def pagenotfound(request):
    category = Categories.get_all_category(Categories)

    context = {
        'category': category
    }
    return render(request, 'error/404.html', context)


def checkout(request, slug):
    if request.user.is_authenticated:
        # membership = request.user.groups.filter(name="gold members").exists()
        course = Course.objects.get(slug=slug)
        context = {'course': course}

        if course.price == 0:
            course = UserCourse(
                user=request.user,
                course=course,
            )
            course.save()
            messages.success(request, 'Success you have enrolled in the course')
            return redirect('mycourse')
        elif request.method == "POST":
            name = request.POST.get('first_name')
            course = UserCourse(
                user=request.user,
                course=course,
            )
            course.save()
            messages.success(request,
                             'payment successful ' + str(name) + ' you have enrolled in the course ' + str(slug))
            return redirect('mycourse')
        return render(request, 'checkout/checkout.html', context)
    else:
        response = redirect('coursedetails', slug)
        msg = "You need to login into your account before enrolling"
        response.set_cookie('user_login_enrollment_msg', msg, max_age=15)
        return response

    return redirect('coursedetails', slug)


def mycourse(request):
    if request.user.is_authenticated:
        categories = Categories.objects.all().order_by('id')[0:]
        courses = UserCourse.objects.filter(user=request.user)
        context = {
            'course': courses, "category": categories
        }
        return render(request, 'course/mycourse.html', context)
    return redirect('home')


def paidregistered(request, slug):
    course = Course.objects.get(slug=slug)
    if request.method == "POST":
        email = request.POST.get('email')
        course = UserCourse(
            user=request.user,
            course=course,
        )
        course.save()
        messages.success(request, 'payment successful ' + email + ' you have enrolled in the course' + course)
        return redirect('mycourse')
    context = {
        'category': "category"
    }
    return render(request, 'error/404.html', context)


def register_course_details(request):
    if request.method == "GET":
        course_form = Course_Detail_Form();
        return render(request, 'registration/register_course.html', {"course_form": course_form})
    else:
        formset = Course_Detail_Form(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Course detail added')
            return redirect('registerCourse')
        else:
            field_errors = formset.errors.as_data()

            # Concatenate error messages for each field into a single string
            error_message = "Invalid Data. "
            for field_name, errors in field_errors.items():
                error_message += f"{field_name}: {', '.join(errors[0].messages)}. "
            messages.error(request, error_message)
            return render(request, 'registration/register_course.html', {"course_form": formset})


def auther_course_details(request):
    return render(request, "course/author_course_detail.html")
