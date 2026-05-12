from django.shortcuts import redirect, render

questions = [
    {"country": "France", "capital": "Paris"},
    {"country": "Canada", "capital": "Ottawa"},
    {"country": "Brazil", "capital": "Brasilia"},
    {"country": "Monaco", "capital": "Monaco"},
    {"country": "Spain", "capital": "Madrid"},
    {"country": "Singapore", "capital": "Singapore"},
    {"country": "Japan", "capital": "Tokyo"},
    {"country": "Israel", "capital": "Jerusalem"},
    {"country": "China", "capital": "Beijing"},
    {"country": "Australia", "capital": "Canberra"},
]


def _get_image_path(country):
    return f"images/{country.lower()}.png"


def homepage(request):
    if request.method == "GET":
        request.session["quiz_questions"] = questions
        request.session["current_index"] = 0
        request.session["score"] = 0
        return render(
            request,
            "index.html",
            {
                "question": questions[0],
                "score": 0,
                "image_path": _get_image_path(questions[0]["country"]),
            },
        )

    return redirect("submit")


def submit_answer(request):
    if request.method != "POST":
        return redirect("index")

    question_list = request.session.get("quiz_questions", questions)
    current_index = request.session.get("current_index", 0)
    score = request.session.get("score", 0)
    user_answer = request.POST.get("answer", "").strip().lower()
    current_question = question_list[current_index]
    correct_answer = current_question["capital"].strip().lower()

    result = "correct" if user_answer == correct_answer else "incorrect"
    if result == "correct":
        score += 1
        request.session["score"] = score

    current_index += 1
    request.session["current_index"] = current_index

    if current_index < len(question_list):
        next_question = question_list[current_index]
        return render(
            request,
            "index.html",
            {
                "question": next_question,
                "score": score,
                "result": result,
                "previous_answer": user_answer,
                "correct_answer": current_question["capital"],
                "image_path": _get_image_path(next_question["country"]),
            },
        )

    return render(request, "results.html", {"final_score": score, "total": len(question_list)})
