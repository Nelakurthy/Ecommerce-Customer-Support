
from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "chat/",
        views.chatbot_response,
        name="chatbot_response"
    ),

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "login/",
        views.user_login,
        name="login"
    ),

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),

    path(
        "history/",
        views.chat_history,
        name="chat_history"
    ),

    path(
        "ticket/",
        views.create_ticket,
        name="create_ticket"
    ),

    path(
        "tickets/",
        views.ticket_history,
        name="ticket_history"
    ),

]
