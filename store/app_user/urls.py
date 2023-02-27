from django.urls import path
from .views import UserLoginView, UserLogoutView, UserRegisterView, UserDetailView, UserUpdateView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('signup/', UserRegisterView.as_view(), name='signup'),

    path('<int:pk>/', UserDetailView.as_view(), name="account"),  # TODO получать данные в шаблон
    path('<int:pk>/', UserUpdateView.as_view(), name="account_update"),  # TODO получать данные в шаблон
]
