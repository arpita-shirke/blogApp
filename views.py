from django.shortcuts import render, redirect,HttpResponse
from blogApp.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
import razorpay
from django.http import HttpResponseBadRequest
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

def home(request):
    if request.method == 'POST':
        p_title=request.POST['title']
        p_content=request.POST['content']
        Author=request.POST['Author']
        created_at=request.POST['created_at']
        updated_at=request.POST['updated_at']

        #print("Name is: ",n,mail,mob,msg)
        m=Post.objects.create(title=p_title,content=p_content,Author=Author,created_at=created_at,updated_at=updated_at)
        m.save()
        # return HttpResponse("Data Inserted Successfully")
        return redirect('/dashboard')
    print("request is: ",request.method)
    return render(request, 'home.html')

def dashboard(request):
    m=Post.objects.all()
    print(m)
    context={}
    context['data']=m
    #return HttpResponse("Data Inserted Successfully!!!")
    return render(request,'dashboard.html',context)

def delete(request,rid):
    print("id of record to be deleted: ",rid)
    m=Post.objects.filter(id=rid)
    m.delete()
    return redirect('/dashboard')
    # return HttpResponse("Id is "+rid)
    
def edit(request,rid):
    if request.method== 'POST':
       p_title=request.POST['title']
       p_content=request.POST['content']
       Author=request.POST['Author']
       created_at=request.POST['created_at']
       updated_at=request.POST['updated_at']
       m=Post.objects.filter(id=rid)
       m=Post.objects.create(tile=p_title,content=p_content,Author=Author,created_at=created_at,updated_at=updated_at)
       return redirect('/dashboard')
    else:
        # display form with old data
        m=Post.objects.get(id=rid)
        context={}
        context['Data']=m
    # print("Id of record to be Edited : "+rid)
    #return Httpresponse("Id is "+rid)
    return render(request,'edit.html',context)

def register(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        if uname=="" or upass=="" or ucpass=="":
            context={}
            context['errmsg']="Field can not be empty"
            return render(request,'register.html',context)
        elif upass!=ucpass:
            context={}
            context['errmsg']="Password Did not Match"
            return render(request,'register.html',context)
        else:
            # print(uname,upass,ucpass)
            try:
                u=User.objects.create(username=uname,email=uname,password=upass)
                u.set_password(upass)
                u.save()
                context={}
                context['success']="User Created Successfully.."
                return render(request,'register.html',context)
            except Exception:
                context={}
                context['errmsg']="user with same username already exists"
                return render(request,'register.html',context)

    else:
        return render(request,'register.html')

def user_login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        # print(uname,upass)
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Field can not be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            print(u)#none
            if u is not None:
                login(request,u)
                return redirect('/home')
            else:
                context['errmsg']="Invalid username and password."
                return render(request,'login.html',context)
        # return HttpResponse("Login Successfully...")
    else:
     return render(request,'login.html')
 
def user_logout(request):
    logout(request)
    return redirect('/home')



def subscription_page(request):
    plans = [
        {
            'name': 'BASIC',
            'price': 99,
            'features': {
                'Post 30 blogs/month': True,
                'Turn Readers into Subscribers': False,
                'Add Paywalls to Selected Posts': False,
                'Setup Payment Schedules': False,
            }
        },
        {
            'name': 'Standard',
            'price': 199,
            'features': {
                'Post 100 blogs/month': True,
                'Turn Readers into Subscribers': True,
                'Add Paywalls to Selected Posts': False,
                'Setup Payment Schedules': False,
            }
        },
        {
            'name': 'Premium',
            'price': 299,
            'features': {
                'Post unlimited blogs/month': True,
                'Turn Readers into Subscribers': True,
                'Add Paywalls to Selected Posts': True,
                'Setup Payment Schedules': True,
            }
        }
    ]
    return render(request, 'subscription.html', {'plans': plans})

def payment_page(request):
    try:
        price_rupees = int(request.GET.get('price', 0))
    except ValueError:
        return HttpResponseBadRequest("Invalid price format.")

    if price_rupees < 1:
        return HttpResponseBadRequest("Amount must be at least ₹1.")

    price_paise = price_rupees * 100  # convert to paise

    client = razorpay.Client(auth=("rzp_test_q11uqwqvK75cTL", "LAR5UWeyUG2qGDhnDldlBbHS"))
    payment = client.order.create({
        "amount": price_paise,
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        'price_display': price_rupees,
        'payment': payment,
        'razorpay_key_id': "rzp_test_q11uqwqvK75cTL"
    }

    return render(request, 'payment.html', context)




@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        # verify signature here (optional)

        # send email
        try:
            if request.user.is_authenticated and request.user.email:
                send_mail(
                    subject="Payment Successful - MyBlog",
                    message="Thank you for your subscription to MyBlog!",
                    from_email="arpitashirke9804@gmail.com",
                    recipient_list=[request.user.email],
                    fail_silently=False,
                )
        except Exception as e:
            print(f"Error sending email: {e}")

        return render(request, 'mail_success.html')

    elif request.method == "GET":
        # Just render success page (no email sent)
        return render(request, 'mail_success.html')

    else:
        return HttpResponse("Invalid request method", status=400)



