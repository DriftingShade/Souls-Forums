from flask_app import app
from flask_app.models.thread import Thread
from flask_app.models.user import User
from datetime import datetime
from flask_app.models.comment import Comment
from flask import flash, render_template, redirect, request, session


@app.route("/threads/all")
def threads():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    threads = Thread.find_all_with_users()
    user = User.find_by_id(session["user_id"])
    return render_template("all_threads.html", threads=threads, user=user)


@app.get("/threads/new")
def new_thread():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    user = User.find_by_id(session["user_id"])
    return render_template("new_thread.html", user=user)


@app.post("/threads/create")
def create_thread():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    if not Thread.form_is_valid(request.form):
        return redirect("/threads/new")

    form_data = {
        "title": request.form["title"],
        "content": request.form["content"],
        "user_id": session["user_id"],
    }

    Thread.create(form_data)

    return redirect("/threads/all")


@app.get("/threads/<int:thread_id>")
def thread_details(thread_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    comments = Comment.all_comments(thread_id)
    thread = Thread.find_by_id_with_user(thread_id)
    user = User.find_by_id(session["user_id"])

    return render_template("thread_details.html", user=user, thread=thread, comments=comments)


@app.get("/threads/<int:thread_id>/edit")
def edit_thread(thread_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    thread = Thread.find_by_id(thread_id)
    user = User.find_by_id(session["user_id"])
    return render_template("edit_thread.html", thread=thread, user=user)


@app.post("/threads/<int:thread_id>/update")
def update_thread(thread_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    if not Thread.form_is_valid(request.form):
        return redirect(f"/threads/{thread_id}/edit")

    form_data = {
        "title": request.form["title"],
        "content": request.form["content"],
        "user_id": session["user_id"],
        "thread_id": thread_id,
    }

    Thread.update(form_data)
    return redirect(f"/threads/{thread_id}")


@app.post("/threads/<int:thread_id>/delete")
def delete_thread(thread_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    Thread.delete_by_id(thread_id)
    return redirect("/threads/all")
