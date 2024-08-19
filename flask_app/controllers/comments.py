from flask_app import app
from flask_app.models.comment import Comment
from flask import flash, render_template, redirect, request, session


@app.post("/comments/create")
def create_comment():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    user_id = session["user_id"]
    thread_id = request.args.get("thread_id")

    form_data = {
        "user_id": user_id,
        "thread_id": thread_id,
        "content": request.form["content"]
    }

    if not Comment.form_is_valid(request.form):
        return redirect(f"/threads/{thread_id}")

    Comment.create(form_data)
    return redirect(f"/threads/{thread_id}")


@app.post("/comments/<int:comment_id>/delete")
def comment_delete(comment_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    thread_id = request.args.get("thread_id")

    Comment.delete_comment(comment_id)

    return redirect(f"/threads/{thread_id}")