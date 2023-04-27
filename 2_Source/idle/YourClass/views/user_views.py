from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from ..models import *
from django.contrib import messages

   
#회원가입
def signup(request): #회원가입 페이지
    template = loader.get_template('signup.html')
    classnames = ClassNames.objects.values_list('classnames', flat=True)
    context = {
        'classnames' : classnames,
    }
    return HttpResponse(template.render(context, request))

#로그인 (로그인 성공하여 리다이렉트시 models.py의 Member객체가 전부 함께 넘어가야합니당)
from django.shortcuts import redirect, render
def login(request): #로그인 페이지
    return render(request, 'login.html')


#회원정보수정(마이페이지에서 정보수정 눌렀을때화면)
def editinfo(request): #회원정보 수정 페이지
    session=request.session.get('login_')
    if session:
        login_ = Member.objects.get(email=session)
        template = loader.get_template('editinfo.html')
        member = Member.objects.get(email=login_.email)
        classnames = ClassNames.objects.values_list('classnames', flat=True)
        context = {
            'classnames' : classnames,
            'member':member,
            'login_':login_,
        }
        return HttpResponse(template.render(context, request))
    else: 
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))

######################추가#############################################

from ..models import Member
def login_ok(request): #로그인페이지 로그인버튼
    x = request.POST['email']
    y = request.POST['password']
    res_data={}
    try:
        login_=Member.objects.get(email=x) #입력한 아이디가 DB에 있는지 확인
        if login_.password== y: #위에 입력한 DB에 있는지 확인된 아이디의 비밀번호와 입력한 비밀번호 확인
            request.session['login_'] = login_.email 
            return redirect('/YourClass') 
        else:
            res_data['error']="비밀번호가 틀렸습니다."
            return render(request,'login.html',res_data)
    except:
        res_data['error']="아이디가 없습니다."
        return render(request,'login.html',res_data)

from django.utils import timezone
from django.db.utils import IntegrityError
def signup_ok(request): #회원가입페이지 회원가입버튼
    if request.method == "POST": 
        if request.POST["password1"] == request.POST["password2"]:
            nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            if request.POST.get("dept"): 
                try:
                    if request.POST["dept"] == ("선생님"): 
                        classnames1 = ClassNames.objects.create(classnames=request.POST["classnames1"]) #텍스트필드에 입력한 값classnames1을 DB의 classnames에 생성
                        member = Member.objects.create(
                            email=request.POST["email"],name=request.POST["name"],password=request.POST["password1"],rdate=nowDatetime,dept=request.POST["dept"],fire="N",classnames=classnames1)#멤버 생성에 필요한 Member의 구성요소
                        fileBoard = Categories(Cat_name='자료실', Cat_info='파일공유가 가능한 필수게시판입니다')
                        fileBoard.save()
                    else:
                        classnames2 = ClassNames.objects.get(classnames=request.POST["classnames"]) #dept값을 선생님 이외로 선택했다면 DB에서 가져온 classnames값 콤보박스로 보여주고 선택한 값을 아래 멤버생성때 입력
                        member = Member.objects.create(
                            email=request.POST["email"],name=request.POST["name"],password=request.POST["password1"],rdate=nowDatetime,dept=request.POST["dept"],fire="N",classnames=classnames2)
                        
                    return redirect('signup') #로그인 실패시 signup페이지로
                except IntegrityError: #프라이머리키인 classnames가 겹칠때를 처리하기 위한 except
                    messages.error(request, "중복된 클래스명이 있습니다 클래스명을 바꿔주세요")
                    return redirect('signup') #로그인 실패시 signup페이지로
            else:
                messages.error(request, "dept값을 선택해주세요.")
                return redirect('signup')
        else:
            messages.error(request, "비밀번호가 일치하지 않습니다.")
            return redirect('signup')
    return redirect('signup')

def logout(request): #인덱스페이지 로그아웃버튼
    if request.session.get('login_'): 
        del(request.session['login_']) 
    return redirect('/YourClass')

from django.urls import reverse 
from django.http import HttpResponse, HttpResponseRedirect
def editinfo_ok(request): #회원정보수정페이지 회원정보수정버튼
    session = request.session.get('login_')
    if session:
        email = request.POST['email']
        name = request.POST['name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        member = Member.objects.get(email=email) #입력한 email과 DB에 있는 email이 동일한 Member의 값을 가져옴
        member.email = email #입력한 email값을 DB의 email값에 덮어씌움(변경)
        member.name = name #입력한 name값을 DB의 name값에 덮어씌움(변경)
        if password1 == password2: #비밀번호와 비밀번호확인값이 같다면
            member.password = password1 #입력한 비밀번호값을 DB의 비밀번호값에 덮어씌움(변경)
        if request.POST.get("dept"): #DB에서 dept값을 가져왔을때
            try:
                if request.POST["dept"] == ("선생님"): #dept값이 선생님이라면
                    classnames1 = ClassNames.objects.create(classnames=request.POST["classnames1"]) #입력한 classnames1값을
                    member.classnames = classnames1 #DB의 classnames에 생성
                else: #dept값이 선생님이 아니라면
                    classnames2 = ClassNames.objects.get(classnames=request.POST["classnames2"]) #DB에서 classnames를 가져오고
                    member.classnames = classnames2 #입력한(콤보박스에서 선택한) classnames2값을 DB에 입력
            except IntegrityError:
                return HttpResponse("중복된 클래스명이 있습니다 클래스명을 바꿔주세요")
        else:
            messages.error(request, "dept값을 선택해주세요.")
            return redirect('editinfo')
        member.save()
        return HttpResponseRedirect(reverse('index'))

    else: 
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))

def deleteuser(request, email): #회원정보수정페이지 회원탈퇴버튼
    session = request.session.get('login_')
    if session:
        member = Member.objects.get(email=email)#현재 로그인한 유저의 email과 DB의 email이 같은 Member의 값을 가져와서
        member.delete() #가져온 멤버값을 삭제(여기까지만 하면 세션은 남아있는데 DB에 데이터가 없어서 오류가 남)
        request.session.flush() #세션값 삭제
        return redirect('/YourClass')
    else: 
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))

def searchid(request): #아이디(이메일)비밀번호 찾기페이지
    return render(request, 'searchid.html')
    
def searchemail(request): #아이디(이메일)비밀번호 찾기페이지의 아이디(이메일)찾기 탭에서 아이디(이메일)찾기 버튼
    template = loader.get_template('searchid.html')
    namex = request.POST['name'] #입력한 이름값
    member = Member.objects.filter(name=namex) #입력한 이름값과 DB에 있는 이름값이 같은 멤버의 값을 '모두' 가져옴 get은 하나만 가능 filter는 전부 가져오기 가능
    if member:
        messages.success(request, ', '.join([m.email for m in member])) #가져온 멤버(들)의 email값을 메세지에 출력
        context = {
            'member' : member,
        }   
    else:
        messages.error(request, '입력하신 이름은 사용되지 않습니다')  
        context = {}        
    return HttpResponse(template.render(context, request))

def searchpass(request): #아이디(이메일)비밀번호 찾기페이지 비밀번호 찾기 탭에서 비밀번호 찾기 버튼
    template = loader.get_template('searchid.html')
    emailx = request.POST['email'] #입력한 email값
    try:
        member = Member.objects.get(email=emailx) #입력한 email값과 DB에 있는 email값이 같은 멤버의 값을 가져옴 email은 프라이머리키로 고유하므로 get사용 가능
        messages.success(request, member.password) #가져온 멤버의 password값을 메세지에 출력
        context = {
            'member' : member,
        }
    except Member.DoesNotExist:
        messages.error(request, '입력하신 이메일은 사용되지 않습니다')
        context = {}    
    
    return HttpResponse(template.render(context, request))