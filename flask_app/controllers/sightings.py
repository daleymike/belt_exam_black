from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.sighting import Sighting
from flask_app.models.user import User
from datetime import datetime

@app.route('/new/sighting')
def new_sighting():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id':session['user_id']
        }
    this_user = User.get_all_by_id(data)
    return render_template("create.html", this_user = this_user)

@app.route('/create/sighting', methods=['POST'])
def create_sighting():
    if 'user_id' not in session:
        return redirect('/')

    if not Sighting.validate_sighting(request.form):
        return redirect('/new/sighting')

    data = {
        'location':request.form['location'],
        'what_happened':request.form['what_happened'],
        'date':request.form['date'],
        'num_of_sasquatch':request.form['num_of_sasquatch'],
        'user_id':session['user_id']
    }

    Sighting.save(data)
    return redirect('/dashboard')

@app.route('/view/sighting/<int:id>')
def view_sighting(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'id' : session['user_id']}
    this_user = User.get_all_by_id(data)
    sighting_data = {'id':id}
    sighting_info = Sighting.get_all_with_skeptics(sighting_data)
    sighting_info.date = sighting_info.date.strftime("%B %d %Y")
    return render_template("show.html", this_user = this_user, sighting_info = sighting_info)

@app.route('/edit/sighting/<int:id>')
def edit_sighting(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'id' : session['user_id']}
    this_user = User.get_all_by_id(data)

    sighting_data = {'id':id}
    sighting_info = Sighting.get_sighting_by_id(sighting_data)

    return render_template("edit.html", this_user = this_user, sighting_info = sighting_info)

@app.route('/update/sighting', methods=['POST'])
def update_sighting():
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id': request.form['id'],
        'location': request.form['location'],
        'what_happened':request.form['what_happened'],
        'date':request.form['date'],
        'num_of_sasquatch':request.form['num_of_sasquatch']
    }

    if not Sighting.validate_sighting(request.form):
        return redirect('/edit/sighting/' + request.form['id'])

    Sighting.update(data)
    return redirect('/dashboard')

@app.route('/destroy/sighting/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : id
    }
    Sighting.destroy(data)
    return redirect('/dashboard')

@app.route('/skeptical/<int:id>')
def add_skeptic(id):
    data = {
        'user_id' : session['user_id'],
        'sighting_id': id
        }
    Sighting.add_skeptic(data)
    return redirect('/view/sighting/' + str(id))

@app.route('/destroy/skeptic/<int:id>')
def remove_skeptic(id):
    data = {
        'user_id' : session['user_id'],
        'sighting_id': id
        }
    Sighting.remove_skeptic(data)
    return redirect('/view/sighting/' + str(id))








    
