from django.urls import path
from .views import pollslist, profileView, loginView, poll_suggestion,  vote, delete, register_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('home/<str:filter_button_pressed>', pollslist.as_view(), name="home"), 
    path('poll/<int:pk>', vote, name="poll_vote"),
    path('delete/<int:pk>/<str:filter_button_pressed>', delete, name="poll_delete"),
    path('profile/<str:name>', profileView.as_view(), name="profile"),
    path('login', loginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(next_page='login'), name="logout"),
    path('register', register_view, name="register"),
    path("poll_suggestion", poll_suggestion.as_view(), name="poll_suggestion"),
]
