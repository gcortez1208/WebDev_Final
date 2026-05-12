from django.shortcuts import redirect, render
import random

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
        # Initialize session for new quiz
        request.session["used_indices"] = []
        request.session["score"] = 0
        # Generate number to use as index to select a random question
        random_index = _generate_random_index(request.session["used_indices"])
        if random_index is None:
            # No more questions, but shouldn't happen on start
            return render(request, "results.html", {"final_score": 0, "total": len(questions)})
        # Retrieve a random question
        selected_question = questions[random_index]
        request.session["current_question_index"] = random_index
        # Pass the selected question to the template to be displayed to the user
        return render(
            request,
            "index.html",
            {
                "question": selected_question,
                "score": 0,
                "image_path": _get_image_path(selected_question["country"]),
            },
        )

    return redirect("process_form")


def _generate_random_index(used_indices):
    available_indices = [i for i in range(len(questions)) if i not in used_indices]
    if not available_indices:
        return None
    return random.choice(available_indices)


def process_form(request):
    if request.method != "POST":
        return redirect("index")

    # Retrieve the index, score, and answer from the session
    used_indices = request.session.get("used_indices", [])
    score = request.session.get("score", 0)
    current_question_index = request.session.get("current_question_index")
    user_answer = request.POST.get("answer", "").strip().lower()

    if current_question_index is None:
        return redirect("index")

    current_question = questions[current_question_index]
    correct_answer = current_question["capital"].strip().lower()

    # Compare the user answer to the correct answer and update the score accordingly
    result = "correct" if user_answer == correct_answer else "incorrect"
    if result == "correct":
        score += 1
        request.session["score"] = score

    # Increment the index to move to the next question and update the session
    used_indices.append(current_question_index)
    request.session["used_indices"] = used_indices

    # If there are more questions, render the next question template with the updated score and index, otherwise render the results template with the final score
    random_index = _generate_random_index(request.session["used_indices"])
    if random_index is not None:
        next_question = questions[random_index]
        request.session["current_question_index"] = random_index
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
    else:
        return render(request, "results.html", {"final_score": score, "total": len(questions)})
