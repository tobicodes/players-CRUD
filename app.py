from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from forms import Addnewplayer, Editplayer, Addnewtrait, Edittrait
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
modus = Modus(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/Players-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Player (db.Model):
	__tablename__ = "players"

	## define columns and tell database what to expect in these columns 

	id = db.Column(db.Integer, primary_key = True)
	first_name = db.Column(db.Text, nullable = False)
	last_name = db.Column(db.Text, nullable = False)
	position = db.Column(db.Text, nullable = False)
	traits = db.relationship('Trait', backref ='player', lazy ='dynamic')

	## define rows
	def __init__(self, first_name, last_name, position):
		self.first_name = first_name
		self.last_name = last_name
		self.position = position 

	## repr is human-readable text that gets printed when we print instances of Player class

	def __repr__(self):
		return "Player is {} {}".format(self.first_name, self.last_name)

@app.route("/players", methods = ["GET", "POST"])
def index():
	form = Addnewplayer(request.form)
	if request.method == "POST":
		if form.validate():
			player = Player(first_name = request.form['first_name'],
						last_name = request.form['last_name'],
						position = request.form['position'])
			db.session.add(player)
			db.session.commit()
			flash("Successfully created a new player")
			return redirect(url_for('index'))
		else:
			return render_template("new.html", form=form)


	all_players =Player.query.all()

	return render_template("index.html", all_players=all_players)


@app.route("/players/new")
def new():
	form = Addnewplayer(request.form)
	return render_template('new.html', form=form)

@app.route("/players/<int:id>", methods =["GET", "PATCH", "DELETE"])
def show(id):
	player = Player.query.get(id)

	if request.method == b"PATCH":
	
		player.first_name = request.form['first_name']
		player.last_name = request.form['last_name']
		player.position = request.form['position']
		db.session.add(player)
		db.session.commit()
		return redirect(url_for('index'))
		
	if request.method == b"DELETE":
		db.session.delete(player)
		db.session.commit()
		return redirect(url_for('index'))
	
	return render_template("show.html", player = player)

@app.route("/players/<int:id>/edit")
def edit(id):
	player = Player.query.get(id)
	return render_template("edit.html", player = player)


class Trait(db.Model):
	__tablename__ = "traits"

	id = db.Column(db.Integer, primary_key = True) 
	content = db.Column(db.Text, nullable = False)
	player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
	
	def __init__(self,content, player_id):
		self.content = content
		self.player_id = player_id

	def __repr__(self):
		return self.content

@app.route("/players/<int:id>/traits", methods = ["GET", "POST"])
def traits_index(id):
	player = Player.query.get(id)
	if request.method == "POST":
		new_trait = Trait(request.form['new_trait'], id)
		db.session.add(new_trait)
		db.session.commit()
		return redirect(url_for('traits_index', id = id))

	return render_template('traits.html', player = player)

@app.route("/players/<int:id>/traits/new")
def new_trait(id):
	player = Player.query.get(id)
	return render_template('new_trait.html', player = player)


@app.route("/players/<int:player_id>/traits/<int:id>", methods = ["GET", "PATCH", "DELETE"])
def show_trait(player_id, id):
	trait = Trait.query.get(id)
	if request.method == b"PATCH":
		trait.content = request.form['edited_trait']
		db.session.add(trait)
		db.session.commit()
		return redirect(url_for('traits_index', id = player_id))

	if request.method ==b"DELETE":
		db.session.delete(trait)
		db.session.commit()
		return redirect(url_for('traits_index', id = player_id))

	return render_template('show_trait.html', trait = trait)


@app.route("/players/<int:player_id>/traits/<int:id>/edit")
def edit_trait(player_id, id):
	trait = Trait.query.get(id)
	return render_template('edit_trait.html', trait = trait)


if __name__ == '__main__':
	app.run(debug=True, port=3001)
