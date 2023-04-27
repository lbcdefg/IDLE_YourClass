from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('mypage/', views.mypage, name='mypage'),
    path('editinfo/', views.editinfo, name='editinfo'),
    # path('calendar/', views.calendar, name='calendar'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('board1/', views.board1, name='board1'), 
    
    ############################################ 진형 ########
    path('createPost/', views.createPost, name='createPost'),
    path('board1/detail/<int:post_id>/', views.detail, name='detail'),
    path('board1/detail/<int:post_id>/updatepost', views.updatepost, name='updatepost'),
    path('board1/detail/<int:post_id>/deletepost', views.deletepost, name='deletepost'),
    path('searchpost/', views.searchpost, name='searchpost'),
    path('board1/<str:category_name>/', views.board_category, name="board_category"),
    path('deleteComment/<int:comment_id>', views.deleteComment, name='deleteComment'),
    path('updateComment/<int:comment_id>', views.updateComment, name='updateComment'),
    path('board1/detail/updateComment/<int:comment_id>', views.updateComment, name='updateComment'),
    path('mypage/admin_member', views.admin_member, name='admin_member'),
    path('mypage/admin_board', views.admin_board, name='admin_board'),
    path('board1/detail/<int:post_id>/like', views.like, name='like'),
    path('updateCategory/<str:Cat_name>', views.updateCategory, name='updateCategory'),
    path('deleteCategory/<str:Cat_name>', views.deleteCategory, name='deleteCategory'),
    path('mypage/createBoard/', views.createBoard, name="createBoard"),
    
    path('mypage_likes/', views.mypage_likes, name='mypage_likes'), # 0302 진형추가

    ############################################# 수한 ###########
    path('login/login_ok',views.login_ok, name='login_ok'), #로그인페이지 로그인버튼
    path('signup/signup_ok', views.signup_ok, name='signup_ok'), #회원가입페이지 회원가입버튼
    path('logout/',views.logout,name='logout'), #인덱스페이지 로그아웃버튼
    path('editinfo/editinfo_ok', views.editinfo_ok, name='editinfo_ok'), #회원정보수정페이지 회원정보수정버튼
    path('deleteuser/<str:email>', views.deleteuser, name='deleteuser'), #회원정보수정페이지 회원탈퇴버튼
    path('searchid/', views.searchid, name='searchid'), #아이디(이메일)비밀번호 찾기페이지
    path('searchemail/', views.searchemail, name='searchemail'), #아이디(이메일)비밀번호 찾기페이지 아이디(이메일)찾기 탭에서 아이디(이메일)찾기 버튼
    path('searchpass/', views.searchpass, name='searchpass'),#아이디(이메일)비밀번호 찾기페이지 비밀번호 찾기 탭에서 비밀번호 찾기 버튼

    ############################################# 대원 ############
    path('event/new/', views.event, name='event_new'),
	path('event/edit/?<event_id>/', views.event, name='event_edit'),  

    path('postWrite/', views.post_write, name='post_write'), 
    path('download/<int:pk>', views.post_download, name='post_download'),  
]