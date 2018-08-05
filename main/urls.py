from django.urls import path
from main import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('generate_new_dataset/', views.generate_new_dataset,name='generate_new_dataset'),
    path('', views.HomePageView.as_view(), name='home'),

    path('dashboard', views.DashboardView.as_view(), name='dashboard'),

    path('sms_response/', views.sms_response,name='inbound_view'),

    path('user/transtaction/',views.new_transtaction, name='new_transtaction'),
    path('transtaction/list', views.TransactionListView.as_view(), name='transtaction-list'),
    path('user/list', views.UserListView.as_view(), name='user-list'),
    path('user/signup/', views.SignUp.as_view(), name='signup'),
    path('user/update/<int:pk>/', views.UserUpdateView.as_view(), name='user-update'),
    path('user/detail/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
    # login and logout
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # change password urls
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # reset password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

#accounts/login/ [name='login'] registration/login.html.
#accounts/logout/ [name='logout'] registration/logged_out.html
#accounts/password_change/ [name='password_change'] registration/password_change_form.html
#accounts/password_change/done/ [name='password_change_done'] registration/password_change_done.html
#accounts/password_reset/ [name='password_reset'] registration/password_reset_form.html
#accounts/password_reset/done/ [name='password_reset_done'] registration/password_reset_done.html
#accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm'] registration/password_reset_confirm.html.
#accounts/reset/done/ [name='password_reset_complete'] registration/password_reset_complete.html

handler404 = 'main.views.html_404'
