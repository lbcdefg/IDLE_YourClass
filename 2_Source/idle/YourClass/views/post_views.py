from django.shortcuts import render, redirect, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from YourClass.models import *
from YourClass.forms import *
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q


#메인페이지(나중에 세션만들고나서 세션유무에따라서 다시 분리해줘야함)
def index(request):
    template = loader.get_template('index.html')
    session = request.session.get('login_')    
    if session:
        member = Member.objects.get(email=session)
        
        # Line 24 ~ Line 31 내용이 context에 함께 넘어가야 네비게이션 바의 자료실에 카테고리가 뜸 + 메인페이지 네모네모에 카테고리별 게시판과 게시판설명이 뜨게하는 내용
        categories = Categories.objects.values_list('Cat_name', flat=True)
        classes = ClassNames.objects.values_list('classnames', flat=True)
        categoryli = []
        for category in categories:
            categoryli.append(category)

        categories_info = []
        category_information = Categories.objects.filter(Cat_name__in=categoryli)
        for x in category_information:
            categories_info.append(x.Cat_info)
        boards = zip(categories, categories_info)
        
        context = {
            'member' : member,
            'categories' : categories,
            'categories_info' : categories_info,
            'boards' : boards,
            'classes' : classes,
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse(template.render({}, request))
   
#마이페이지(로그인시 메인에서 ~~님 눌렀을 때 화면)
# 0302 진형추가
def mypage(request):
    session = request.session.get('login_')
    if session:
        template = loader.get_template('mypage.html')
        member = Member.objects.get(email=session) # 기본context 네비게이션 이름
        categories = Categories.objects.values_list('Cat_name', flat=True) # 기본context 네비게이션바 드롭다운에 뜨게하기 위함
        
        tab_title = '내가 작성한 글'
        posts = Post.objects.select_related('author').all()
        posts = posts.filter(author_id=session)
        
        # 페이지에서 유저가 선택한 기준에 따른 정렬
        sort = request.GET.get('sort','')
        if sort == 'viewcount':
            posts =posts.order_by('-viewcount')
        elif sort == 'likes' : 
            posts = posts.order_by('-post_like')
        else:
            posts = posts.order_by('-id')
        
        # 마이페이지의 내가작성한 글 페이징
        page = request.GET.get('page', '1')
        posts = posts.order_by('-date')
        paginator = Paginator(posts, 10)
        page_obj = paginator.get_page(page)

        
        # 각 글 별로 달린 댓글 수
        for post in page_obj:
            post.commentCount = len(Comment.objects.filter(post_id=post.id))
        
        context = {
            'member' : member,
            'posts' : posts,
            'categories' : categories,
            'post_list': page_obj,
            'tab_title' : tab_title
        }
        return HttpResponse(template.render(context, request))
    else: 
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))

# 0302진형추가
def mypage_likes(request):
    session = request.session.get('login_')
    if session:
        template = loader.get_template('mypage.html')
        member = Member.objects.get(email=session) # 기본context 네비게이션 이름
        categories = Categories.objects.values_list('Cat_name', flat=True) # 기본context 네비게이션바 드롭다운에 뜨게하기 위함
        
        tab_title = '내가 추천한 글'
        likeposts = Like.objects.prefetch_related('like_user')
        likeposts = likeposts.filter(like_user=session)

        # session과 동일한 유저 id로 추천한 글 번호들을 likeposts_idlist 에 담아준다
        likeposts_idlist = []
        for dict in likeposts.values():
            print('dict:',dict)
            for key, value in dict.items():
                if key=='like_post_id':
                    likeposts_idlist.append(value)

        # 위에서 생성한 리스트 값을 필터값으로 넣어 나(session=like_user_id)의 추천 리스트를 뽑는다       
        posts = Post.objects.select_related('author').all().filter(pk__in=likeposts_idlist)
        
        # 페이지에서 유저가 선택한 기준에 따른 정렬
        sort = request.GET.get('sort','')
        if sort == 'viewcount':
            posts =posts.order_by('-viewcount')
        elif sort == 'likes' : 
            posts = posts.order_by('-post_like')
        else:
            posts = posts.order_by('-id')
        
        # 마이페이지의 내가작성한 글 페이징
        page = request.GET.get('page', '1')
        posts = posts.order_by('-date')
        paginator = Paginator(posts, 10)
        page_obj = paginator.get_page(page)
        
        # 각 글 별로 달린 댓글 수
        for post in page_obj:
            post.commentCount = len(Comment.objects.filter(post_id=post.id))
        
        context = {
            'member' : member,
            'posts' : posts,
            'categories' : categories,
            'post_list': page_obj,
            'tab_title': tab_title,
        }
        return HttpResponse(template.render(context, request))
    else: 
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))

#일정
def calendar():
    pass

# 새 글 작성화면
def createPost(request):
    session = request.session.get('login_')
    if session:
        member = Member.objects.get(email=session)
        post = Post.objects.values()
        categories = Categories.objects.values_list('Cat_name', flat=True)
        context = {
            'member' : member,
            'post' : post,
            'categories' : categories,
        }
        if request.method == 'POST':                # 작성버튼 눌렀을 때 POST방식으로 DB에 전송할준비
            form = CreatePost(request.POST)
            if form.is_valid():                     # form 이 notnull 조건에 맞게 모두 잘 입력되었을 때 전송
                title = form.data.get('title')
                category = form.data.get('category')
                category = Categories.objects.get(pk=category)
                body = form.data.get('body')
                post_fix = form.data.get('post_fix')
                if form.data.get("post_fix") == "on":
                    post_fix = True
                else:
                    post_fix = False
                post = Post(title=title, category=category, body=body, file='Null', author=Member.objects.get(pk=session), post_fix=post_fix)
                post.save()
                return redirect('/YourClass/board1/'+str(category.Cat_name), context) # 작성완료시 전체 게시글목록 화면으로 보냄
            else:
                return redirect('/YourClass/createPost')       # form이 미완일경우 재귀호출, 그런데 장고내장 폼 기능으로 커버됨
        else:                                        # 페이지를 처음 열었을 때 form 띄우는 부분
            form = CreatePost()
            context['form'] = form
            return render(request, 'createPost.html', context)
    else:
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))

# 게시글 id에 따른 글 상세화면
def detail(request, post_id):
    session = request.session.get('login_')
    if session:
        member = Member.objects.get(email=session) # 기본context : 네비게이션바에 이름
        categories = Categories.objects.values_list('Cat_name', flat=True) #기본context : 네비게이션바에 게시판드롭다운
        post_detail = get_object_or_404(Post, pk=post_id) # 없는 글번호로 주소창에 입력하면 404띄움
        post_detail.viewcount +=1                         # 상세화면페이지가 열리면 조회수 자동 +1증가
        post_detail.save()    
        posts = Post.objects.select_related('author').all()
        postAuthor = posts.get(pk=post_id).author.name
        
        context={
            'member' : member,
            'categories' : categories,
            'postAuthor' : postAuthor,
        }
        
        # 댓글수 띄워주기, 쿼리셋 존재하지 않을시(결과물 없을경우) 0으로 
        commentCount = Comment.objects.filter(post_id=post_id)
        if commentCount.exists():
            context['commentCount'] = len(commentCount)
        else:
            commentCount = 0
            context['commentCount'] = commentCount
        
        comments = Comment.objects.select_related('comment_user').all()
        comments = comments.filter(post_id=post_id).order_by('-comment_date')
        if request.method == 'POST':
            # 댓글란의 댓글쓰기 버튼을 누를 경우 POST 방식으로 보내지도록
            comment_form = PostCommentForm(request.POST)
            if comment_form.is_valid():
                content = comment_form.cleaned_data['comment_text']
                comment = Comment(comment_text=content, post_id=post_id, comment_user=Member.objects.get(pk=session))
                comment.save()
                print(content)
                return redirect('../{}'.format(post_id), context)
        else:
            # 처음에 글 상세보기 화면이 띄워진 직후, 즉 댓글란 작성하기 버튼을 누르기 전까지 띄워져야 하는 내용
            comment_form = PostCommentForm()
            context['post_detail'] = post_detail
            context['comments'] = comments
            context['comment_form'] = comment_form
            context['post_id'] = post_id
            return render(request, 'detail.html', context)
    else: 
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))

# 게시글 id에 따른 글 수정 함수
def updatepost(request, post_id):
    session = request.session.get('login_')
    post = Post.objects.get(pk=post_id)
    if session:
        member = Member.objects.get(email=session) # 기본context : 네비게이션바에 이름
        categories = Categories.objects.values_list('Cat_name', flat=True) #기본context : 네비게이션바에 게시판드롭다운
        # 글상세보기의 작성자와 session이 동일한지 체크하고, 맞으면 작성폼에 기존데이터 넣은채로 띄움
        if post.author_id == session: 
            form = CreatePost(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                title = form.data.get('title')
                category = form.data.get('category')
                body = form.data.get('body')
                file = form.data.get('file')
                post = Post(id=post_id, title=title, category=Categories.objects.get(pk=category), body=body, file=file, author=Member.objects.get(pk=session))
                post.save()
                messages.success(request, '수정되었습니다')
                return redirect('/YourClass/board1')
            else:
                form = CreatePost(instance=post)
                context = {
                    'form' : form,
                    'pageTitle' : '내글수정',
                    'member' : member,
                    'categories' : categories,
                }
                return render(request, 'createPost.html', context)
        else:
            messages.error(request, '본인 게시글이 아닙니다')
            return redirect('/YourClass/board1/detail/'+str(post_id))
    else:
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))

# 게시글 id에 따른 글 삭제 함수
def deletepost(request, post_id):
    session = request.session.get('login_')
    if session:
        post = Post.objects.get(pk=post_id)
        if post.author_id == session:
            post.delete()
            messages.success(request, '삭제되었습니다')
            return redirect('/YourClass/board1')
        else:
            messages.error(request, '본인 게시글이 아닙니다')
            return redirect('/YourClass/board1/detail/'+str(post_id))
    else:
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))

# 핸드폰걸의 검색창에 입력했을 때 게시글 검색하는 함수(게시판 구분없이 전체적용->작성자검색도 가능)
def searchpost(request):
    session = request.session.get('login_')
    if session:
        member = Member.objects.get(email=session) # 기본context : 네비게이션바에 이름
        categories = Categories.objects.values_list('Cat_name', flat=True) #기본context : 네비게이션바에 게시판드롭다운
        result = Post.objects.select_related('author').all()
        r = request.GET.get('r','')
        if r:
            result = result.filter(Q(title__icontains=r)|Q(file__icontains=r)|Q(body__icontains=r)|Q(author__name__icontains=r))
        
        # 페이지에서 유저가 선택한 기준에 따른 정렬
        sort = request.GET.get('sort','')
        if sort == 'viewcount':
            posts =result.order_by('-viewcount')
        elif sort == 'likes' : 
            posts = result.order_by('-post_like')
        else:
            posts = result.order_by('-id')

        # 게시글 페이징
        page = request.GET.get('page', '1')
        paginator = Paginator(posts, 10)
        page_obj = paginator.get_page(page)
        
        # 각 글 별로 달린 댓글 수
        for post in page_obj:
            post.commentCount = len(Comment.objects.filter(post_id=post.id))
            
        context = {
            'post_search': page_obj,
            'r' : r,
            'member' : member,
            'categories' : categories,
        }
        
        return render(request, 'searchpost.html', context)
    else:
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))

# 카테고리값을 가지지 않는 보드 => 전체 게시글 나오는 리스트
def board1(request):
    session = request.session.get('login_')
    if session:
        member = Member.objects.get(email=session)
        categories = Categories.objects.values_list('Cat_name', flat=True)
        posts = Post.objects.select_related('author').all() # Post의 작성자(email)를 통한 Member의 name을 뽑기 위해 join
    
        # 페이지에서 유저가 선택한 기준에 따른 정렬
        sort = request.GET.get('sort','')
        if sort == 'viewcount':
            posts =posts.order_by('-viewcount')
        elif sort == 'likes' : 
            posts = posts.order_by('-post_like')
        else:
            posts = posts.order_by('-id')

        # 게시글 페이징
        page = request.GET.get('page', '1')
        paginator = Paginator(posts, 10)
        page_obj = paginator.get_page(page)
        
        # 각 글 별로 달린 댓글 수
        for post in page_obj:
            post.commentCount = len(Comment.objects.filter(post_id=post.id))
         
        context = {
            'member' : member,
            'categories' : categories,
            'post_list': page_obj,
        }    
        template = loader.get_template('board1.html')
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))

# 카테고리값을 가지는 보드 => 해당 게시판에 올린 글만 나오는 리스트
def board_category(request, category_name):
    session = request.session.get('login_')
    if session:
        member = Member.objects.get(email=session) # 기본context : 네비게이션바에 이름
        categories = Categories.objects.values_list('Cat_name', flat=True) #기본context : 네비게이션바에 게시판드롭다운
        posts = Post.objects.select_related('author').all()
        category_posts = posts.filter(category_id=category_name)
        
        # 페이지에서 유저가 선택한 기준에 따른 정렬
        sort = request.GET.get('sort','')
        if sort == 'viewcount':
            posts =category_posts.order_by('-viewcount')
        elif sort == 'likes' : 
            posts = category_posts.order_by('-post_like')
        else:
            posts = category_posts.order_by('-id')
        
        # 위에서 정렬된 리스트를 페이징
        page = request.GET.get('page', '1')
        paginator = Paginator(posts, 10) 
        page_obj = paginator.get_page(page)

        # 각 글 별로 달린 댓글 수
        for post in page_obj:
            post.commentCount = len(Comment.objects.filter(post_id=post.id))

        context = {
            'member' : member,
            'categories' : categories,
            'post_list': page_obj,
            'category_posts':category_posts,
            'category_name' : category_name,
        }  
        return render(request, 'board1.html', context)
    else:
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))

# 댓글id에 맞는 댓글 수정...(사실상 구현못함)
def updateComment(request, comment_id):
    session = request.session.get('login_')
    if session:
        member = Member.objects.get(email=session) # 기본context : 네비게이션바에 이름
        categories = Categories.objects.values_list('Cat_name', flat=True) #기본context : 네비게이션바에 게시판드롭다운
        comment = Comment.objects.get(pk=comment_id)
        post_id = comment.post_id
        post_detail = Post.objects.select_related('author').all().get(pk=post_id)
        print(post_detail)
        if comment.comment_user_id==session:
            form = PostCommentForm(request.POST)
            if request.method == 'POST':
                if form.is_valid():
                    content = form.data.get('comment_text')
                    comment = Comment(id=comment_id, comment_text=content, post_id=post_id, comment_user_id=session)
                    comment.save()
                    messages.success(request, '댓글이 수정되었습니다')
                    return redirect('/YourClass/board1/detail/'+str(comment.post_id), post_id)
                else:
                    form = PostCommentForm(instance=comment)
                    
                    context={
                        'member':member,
                        'categories':categories,
                        'form':form,
                        'comment':comment,
                        'post_detail':post_detail,
                    }
                    return render(request, 'updateComment.html', context)
            else:
                form = PostCommentForm(instance=comment)
                context={
                        'member':member,
                        'categories':categories,
                        'form':form,
                        'comment':comment,
                        'post_detail':post_detail,
                    }
                return render(request, 'updateComment.html', context)
        else:
            messages.error(request, '댓글 작성자가 아닙니다')
            return redirect('/YourClass/board1/detail/'+str(comment.post_id), post_id)
    else:
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))

# 댓글id에 맞는 댓글 삭제
def deleteComment(request, comment_id):
    session = request.session.get('login_')
    if session:
        comment = Comment.objects.get(pk=comment_id)
        post_id = comment.post_id
        if comment.comment_user== Member.objects.get(pk=session):
            comment.delete()
            messages.success(request, '삭제되었습니다')
            return redirect('/YourClass/board1/detail/'+str(comment.post_id), post_id)
        else:
            messages.error(request, '본인 게시글이 아닙니다')
            return redirect('/YourClass/board1/detail/'+str(comment.post_id), post_id)
    else:
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))
    
##############################################################
# (선생님일경우only) 마이페이지 학생관리
def admin_member(request):
    session = request.session.get('login_')
    if session:
        template = loader.get_template('admin_member.html')
        member = Member.objects.get(email=session)
        post = Post.objects.filter(author_id=session) # 작성자가 session인 경우에만 post로담기
        categories = Categories.objects.values_list('Cat_name', flat=True) # 네비게이션바 드롭다운에 뜨게하기 위함
        
        # 마이페이지의 내가작성한 글 페이징
        page = request.GET.get('page', '1')
        posts = post.order_by('-date').values()
        paginator = Paginator(posts, 10)
        page_obj = paginator.get_page(page)

        context = {
            'member' : member,
            'post' : post,
            'categories' : categories,
            'post_list': page_obj,
        }
        return HttpResponse(template.render(context, request))
    else: 
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))

# (선생님일경우only) 마이페이지 게시판관리
def admin_board(request):
    session = request.session.get('login_')
    if session:
        template = loader.get_template('admin_board.html')
        member = Member.objects.get(email=session)
        post = Post.objects.filter(author_id=session) # 작성자가 session인 경우에만 post로담기
        categories = Categories.objects.values_list('Cat_name', flat=True) # 네비게이션바 드롭다운에 뜨게하기 위함
        categorydata = Categories.objects.all()
        context = {
            'member' : member,
            'post' : post,
            'categories' : categories,
            'categorydata' : categorydata,
        }
        return HttpResponse(template.render(context, request))
    else: 
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))

# (선생님일경우only) 게시판 추가기능
def createBoard(request):
    session = request.session.get('login_')
    if session:
        member = Member.objects.get(email=session) # 기본context : 네비게이션바에 이름
        categories = Categories.objects.values_list('Cat_name', flat=True) #기본context
        template = loader.get_template('createBoard.html')
        category_form = CategoryForm(request.POST)
        context = {
            'member' : member,
            'categories' : categories,
            'category_form' : category_form,
        }
        if request.method == 'POST':
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                cat_name = category_form.data.get('Cat_name')
                cat_info = category_form.data.get('Cat_info')
                category = Categories(Cat_name=cat_name, Cat_info=cat_info)
                category.save()
                return redirect('/YourClass/mypage/admin_board', context)
        else:
            category_form = CategoryForm()
            context['category_form'] = category_form
            return render(request, 'createBoard.html', context)
    else: 
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))

# (선생님일경우only) 게시판 소개글 수정기능
def updateCategory(request, Cat_name):
    session = request.session.get('login_')
    if session:
        template = loader.get_template('createBoard.html')
        member = Member.objects.get(email=session)
        categories = Categories.objects.values_list('Cat_name', flat=True) # 네비게이션바 드롭다운에 뜨게하기 위함
        categorydata = Categories.objects.all()
        category = Categories.objects.get(pk=Cat_name)
        if request.method == 'POST': 
            categoryUpdate_form = CategoryUpdateForm(request.POST)
            if categoryUpdate_form.is_valid():
                category = categoryUpdate_form.save(commit=False)
                info = categoryUpdate_form.data.get('Cat_info')
                category = Categories(Cat_name=Cat_name, Cat_info=info)
                category.save()
                messages.success(request, str(Cat_name)+' 게시판의 소개글이 수정되었습니다')
                return redirect('/YourClass/mypage/admin_board')
            else:
                context={
                'member':member,
                'categories':categories,
                'categoryUpdate_form' : categoryUpdate_form,
                'categorydata' : categorydata
            }
                return render(request, 'createBoard.html', context)
        else:
            categoryUpdate_form = CategoryUpdateForm(instance=category)
            context={
                'member':member,
                'categories':categories,
                'Cat_name':Cat_name,
                'categoryUpdate_form' : categoryUpdate_form,
                'categorydata' : categorydata
            }
            return render(request, 'createBoard.html', context)      
    else: 
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))
    
# (선생님일경우only) 게시판 삭제기능
def deleteCategory(request, Cat_name):
    session = request.session.get('login_')
    category = Categories.objects.get(pk=Cat_name)
    if session:
        category.delete()
        messages.success(request, str(Cat_name)+' 게시판이 삭제되었습니다')
        return redirect('mypage')
    else: 
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))

# 좋아요(추천기능)
def like(request, post_id):    
    session = request.session.get('login_')
    if session:
        likes = Like.objects.filter(like_user=session)
        like_list = likes.values()
        try:
            if len(likes):
                for x in like_list:
                    for k, v in x.items():
                        if k == 'like_post_id':
                            if post_id == v:
                                messages.success(request, '이미 추천한 게시물입니다')
                                return redirect('/YourClass/board1/detail/'+str(post_id))
        except:
            print("예외 발생:")
            pass                
        thispost = Post.objects.get(pk=post_id)
        like_user = Member.objects.get(pk=session)
        like_ = Like(like_user=like_user, like_post=thispost)
        like_.save()
        thispost = Post(pk=post_id, title= thispost.title, date=thispost.date, body=thispost.body, author_id=thispost.author_id,post_like=thispost.post_like+1,
                        category_id=thispost.category_id)
        thispost.save()
        messages.success(request, '게시물을 추천하였습니다')
        return redirect('/YourClass/board1/detail/'+str(post_id))
    else:
        template = loader.get_template('pleaselogin.html')
        return HttpResponse(template.render({}, request))
    
    