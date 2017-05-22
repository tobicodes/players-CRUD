from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators

class Addnewplayer (FlaskForm):
	first_name =StringField('First Name', [validators.Length(min=1)])
	last_name = StringField('Last Name', [validators.Length(min=1)])
	position = StringField('Position', [validators.Length(min=1)])

class Editplayer(FlaskForm):
	first_name =StringField('First Name', [validators.Length(min=1)])
	last_name = StringField('Last Name', [validators.Length(min=1)])
	position = StringField('Position', [validators.Length(min=1)])

class Addnewtrait(FlaskForm):
	trait = StringField("What is unique about this player?",[validators.Length(min=1)])

class Edittrait(FlaskForm):
	trait = StringField("Edit his trait",[validators.Length(min=1)])

