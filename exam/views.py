from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Exam, Question, Result


# ---------------- REGISTER ----------------
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {
                "error": "Username already exists"
            })

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect("/login/")

    return render(request, "register.html")



# ---------------- GUEST LOGIN ----------------
# def guest_login(request):
#     return redirect("/exams/")


def guest_login(request):
    # Check if guest user already exists
    guest_user, created = User.objects.get_or_create(username="guest")

    if created:
        guest_user.set_password("guest123")
        guest_user.save()

    login(request, guest_user)
    return redirect("/exams/")

# ---------------- LOGIN ----------------
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/exams/")
        else:
            return render(request, "login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "login.html")


# ---------------- LOGOUT ----------------
@login_required
def user_logout(request):
    logout(request)
    return redirect("/login/")


# ---------------- EXAM LIST ----------------
@login_required(login_url="/login/")
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, "exam_list.html", {"exams": exams})


# ---------------- EXAM PAGE ----------------
@login_required(login_url="/login/")
def exam_page(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = Question.objects.filter(exam=exam)

    if request.method == "POST":
        score = 0

        for q in questions:
            selected = request.POST.get(str(q.id))
            if selected == q.correct_answer:
                score += 1

        percentage = (score / questions.count()) * 100

        # Save result
        Result.objects.create(
            user=request.user,
            exam=exam,
            score=score,
            percentage=percentage
        )

        # Get previous and next exams
        previous_exam = Exam.objects.filter(id__lt=exam.id).order_by('-id').first()
        next_exam = Exam.objects.filter(id__gt=exam.id).order_by('id').first()

        return render(request, "result.html", {
            "exam": exam,
            "score": score,
            "percentage": percentage,
            "previous_exam": previous_exam,
            "next_exam": next_exam
        })

    return render(request, "exam.html", {
        "exam": exam,
        "questions": questions
    })
