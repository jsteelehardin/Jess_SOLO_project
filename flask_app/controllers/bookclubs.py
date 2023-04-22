# Import app
from flask_app import app
# Import modules from flask
from flask_app import Flask, render_template, request, redirect, session, url_for, flash, bcrypt

# Import models class
from flask_app.models import user, bookclub

# CRUD CREATE ROUTES
@app.route('/bookclub/create', methods=['POST'])
def create_new_bookclub():
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Call staticmethod to validate form
    if not bookclub.Bookclub.validate_form(request.form):
        # Redirect back to new bookclub page/dashboard
        return redirect('/dashboard')
    # Create data dict based on request form
    # the keys must match exactly to the var in the query set
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'user_id': session['id']
    }
    bookclub.Bookclub.create_bookclub(data)
    return redirect('/dashboard')

@app.route('/bookclub/favsubscribe', methods=['POST'])
def add_favsubscribe_bookclub():
    bookclub.Bookclub.favsubscribe(request.form)
    return redirect('/dashboard')


# CRUD READ ROUTES
@app.route('/bookclub/show/<int:bookclub_id>')
def bookclub_show_one(bookclub_id):
    """Show the bookclub on a page"""
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Create data dict based on bookclub_id
    # The keys must match exactly to the var in the query set
    data = { 'id': bookclub_id }
    # Create additonal data dict for user
    data_user = { 'id': session['id'] }
    # Call classmethods and render_template edit template with data filled in
    return render_template('show.html', one_bookclub=bookclub.Bookclub.get_one_bookclub(data), user=user.User.get_user_by_id(data_user))


# CRUD UPDATE ROUTES
@app.route('/bookclub/edit/<int:bookclub_id>')
def edit_bookclub(bookclub_id):
    """Edit the bookclub"""
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Create data dict based on bookclub_id
    # The keys must match exactly to the var in the query set
    data = { 'id': bookclub_id }
    # Create additonal data dict for user
    data_user = { 'id': session['id'] }
    # Call classmethods and render_template edit template with data filled in
    return render_template('edit.html', one_bookclub=bookclub.Bookclub.get_one_bookclub(data), user=user.User.get_user_by_id(data_user))

@app.route('/bookclub/update', methods=['POST'])
def update_bookclub():
    """Update bookclub after editing"""
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Call staticmethod to validate form
    if not bookclub.Bookclub.validate_form(request.form):
        # Redirect back to new bookclub page
        id = int(request.form['id'])
        return redirect(f'/bookclub/edit/{id}')
    # Create data dict based on bookclub_id
    # The keys must match exactly to the var in the query set
    data = {
        'id': int(request.form['id']),
        'user_id': session['id'],
        'title': request.form['title'],
        'description': request.form['description'],
    }
    # Call classmethod in models
    bookclub.Bookclub.update_bookclub(data)
    # Redirect to dashboard after update
    flash("Success! Your info has changed.", "success")
    return redirect('/dashboard')

# @app.route('/bookclub/update<int:id>', methods=['POST'])
# def update_bookclub(id):
#     """Update bookclub after editing"""
#     if 'id' not in session:
#         flash("Please register or login to continue", "danger")
#         return redirect('/')
#     if not bookclub.Bookclub.validate_form(request.form):
#         id = int(request.form['id'])
#         return redirect(f'/bookclub/edit/{id}')
#     data = {
#         'id': int(request.form['id']),
#         'user_id': session['user_id'],
#         'title': request.form['title'],
#         'description': request.form['description'],
#     }
#     bookclub.Bookclub.update_bookclub(data)
#     flash("Success! Your info has changed.", "success")
#     return redirect('/dashboard')

# CRUD DELETE ROUTES
@app.route('/bookclub/delete/<int:bookclub_id>', methods=['POST'])
def delete_bookclub(bookclub_id):
    """Delete bookclub if session user created"""
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Create data dict based on bookclub_id
    # The keys must match exactly to the var in the query set
    data = { 'id': bookclub_id }
    # Call classmethod in models
    bookclub.Bookclub.delete_bookclub(data)
    # Redirect back to dashboard after deletion
    flash("Success! Your info has been deleted.", "success")
    return redirect('/dashboard')

@app.route('/bookclub/unfavsubscribe', methods=['POST'])
def un_favsubscribe_bookclub():
    bookclub.Bookclub.unfavsubscribe(request.form)
    return redirect('/dashboard')


