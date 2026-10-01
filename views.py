
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

import json

from .models import FAQ, Conversation, Order, SupportTicket


# =========================
# HOME
# =========================

def home(request):
    return render(request, "chatbot/home.html")


# =========================
# REGISTER
# =========================

def register(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if not username or not email or not password:
            return JsonResponse(
                {"error": "All fields are required"},
                status=400
            )

        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"error": "Username already exists"},
                status=400
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect("home")

    return render(request, "chatbot/register.html")


# =========================
# LOGIN
# =========================

def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("home")

        return JsonResponse(
            {"error": "Invalid username or password"},
            status=401
        )

    return render(request, "chatbot/login.html")


# =========================
# LOGOUT
# =========================

def user_logout(request):

    logout(request)

    return redirect("home")


# =========================
# CHATBOT
# =========================

@csrf_exempt
def chatbot_response(request):

    if request.method != "POST":

        return JsonResponse(
            {"error": "Only POST requests are allowed"},
            status=405
        )

    if not request.user.is_authenticated:

        return JsonResponse(
            {"error": "Please login to use the chatbot"},
            status=401
        )

    try:

        data = json.loads(request.body)

        message = data.get("message", "").strip().lower()

        if not message:

            return JsonResponse(
                {"error": "Message is required"},
                status=400
            )


        # =========================
        # FIND ORDER ID
        # =========================

        words = message.upper().split()

        order_id = None

        for word in words:

            cleaned_word = word.strip(".,!?;:")

            if cleaned_word.startswith("ORD"):

                order_id = cleaned_word

                break


        # =========================
        # ORDER TRACKING
        # =========================

        if (
            "track" in message
            or "order status" in message
            or "where is my order" in message
            or "delivery status" in message
        ):

            if order_id:

                order = Order.objects.filter(
                    user=request.user,
                    order_id=order_id
                ).first()

                if order:

                    response = (
                        f"Order {order.order_id} is currently "
                        f"{order.status}. "
                        f"Product: {order.product.name}. "
                        f"Quantity: {order.quantity}. "
                        f"Total amount: ₹{order.total_amount}."
                    )

                else:

                    response = (
                        f"I couldn't find order {order_id} "
                        f"under your account. "
                        f"Please check the order ID."
                    )

            else:

                response = (
                    "Sure! Please provide your order ID. "
                    "For example: Track order ORD1001"
                )


        # =========================
        # RETURN
        # =========================

        elif (
            "return" in message
            or "return product" in message
            or "return order" in message
        ):

            if order_id:

                order = Order.objects.filter(
                    user=request.user,
                    order_id=order_id
                ).first()

                if not order:

                    response = (
                        f"I couldn't find order {order_id} "
                        f"under your account."
                    )

                elif order.status == "Delivered":

                    response = (
                        f"Order {order.order_id} was delivered. "
                        f"Eligible products can be returned within "
                        f"7 days of delivery. "
                        f"Please create a support ticket with "
                        f"your order ID to start the return."
                    )

                elif order.status == "Cancelled":

                    response = (
                        f"Order {order.order_id} is already cancelled. "
                        f"A return request is not required."
                    )

                else:

                    response = (
                        f"Order {order.order_id} has not been delivered yet. "
                        f"You can request a return after delivery."
                    )

            else:

                response = (
                    "Please provide your order ID to check return "
                    "eligibility. For example: Return order ORD1001"
                )


        # =========================
        # REFUND
        # =========================

        elif (
            "refund" in message
            or "money back" in message
            or "refund status" in message
        ):

            if order_id:

                order = Order.objects.filter(
                    user=request.user,
                    order_id=order_id
                ).first()

                if not order:

                    response = (
                        f"I couldn't find order {order_id} "
                        f"under your account."
                    )

                elif order.status == "Cancelled":

                    response = (
                        f"Order {order.order_id} is cancelled. "
                        f"If the payment was completed, the refund "
                        f"will be processed to the original payment method."
                    )

                else:

                    response = (
                        f"For order {order.order_id}, a refund can "
                        f"be processed after an eligible return is approved. "
                        f"The refund will be sent to the original "
                        f"payment method."
                    )

            else:

                response = (
                    "Please provide your order ID to check refund "
                    "information. For example: Refund ORD1001"
                )


        # =========================
        # FAQ SEARCH
        # =========================

        else:

            faqs = FAQ.objects.all()

            best_answer = None

            best_score = 0

            for faq in faqs:

                keywords = [
                    keyword.strip().lower()
                    for keyword in faq.keywords.split(",")
                    if keyword.strip()
                ]

                score = 0

                for keyword in keywords:

                    if keyword in message:

                        score += 1

                if score > best_score:

                    best_score = score

                    best_answer = faq.answer


            if best_answer:

                response = best_answer

            else:

                response = (
                    "I'm sorry, I couldn't find a suitable answer. "
                    "Please create a support ticket so our customer "
                    "support team can assist you."
                )


        # =========================
        # SAVE CONVERSATION
        # =========================

        Conversation.objects.create(
            user=request.user,
            message=message,
            response=response
        )


        return JsonResponse(
            {
                "message": message,
                "response": response
            }
        )


    except json.JSONDecodeError:

        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )


    except Exception as e:

        return JsonResponse(
            {
                "error": "Something went wrong",
                "details": str(e)
            },
            status=500
        )


# =========================
# CHAT HISTORY
# =========================

def chat_history(request):

    if not request.user.is_authenticated:

        return redirect("login")

    conversations = Conversation.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "chatbot/history.html",
        {
            "conversations": conversations
        }
    )


# =========================
# CREATE SUPPORT TICKET
# =========================

def create_ticket(request):

    if not request.user.is_authenticated:

        return redirect("login")


    if request.method == "POST":

        subject = request.POST.get(
            "subject",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()


        if not subject or not description:

            return JsonResponse(
                {
                    "error": "Subject and description are required"
                },
                status=400
            )


        ticket = SupportTicket.objects.create(
            user=request.user,
            subject=subject,
            description=description
        )


        return JsonResponse(
            {
                "message": "Support ticket created successfully",
                "ticket_id": ticket.id
            }
        )


    return render(
        request,
        "chatbot/ticket.html"
    )


# =========================
# TICKET HISTORY
# =========================

def ticket_history(request):

    if not request.user.is_authenticated:

        return redirect("login")


    tickets = SupportTicket.objects.filter(
        user=request.user
    ).order_by("-created_at")


    return render(
        request,
        "chatbot/ticket_history.html",
        {
            "tickets": tickets
        }
    )
