from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField 
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField

class Admin(FlaskForm):
    username =  StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
    email =  StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    konf_pass = PasswordField('Konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Daftar")

class LoginA(FlaskForm):
    email =  StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")

class ArtikelP(FlaskForm):
    judul = StringField('Judul', validators=[DataRequired()])
    konten = CKEditorField('Konten', validators=[DataRequired()])
    thumbnail = FileField('Foto', validators=[DataRequired(),FileAllowed(['jpg','jpeg','png','gif'])])
    kategori_id = SelectField('Kategori Berita', validators=[DataRequired()])
    submit = SubmitField("Post")

class KategoriF(FlaskForm):
    nama_kat = StringField('Tambah Kategori', validators=[DataRequired()])
    submit = SubmitField("Tambah Kategori")

class editArtikel(FlaskForm):
    judul = StringField('Judul', validators=[DataRequired()])
    konten = CKEditorField('Konten', validators=[DataRequired()])
    thumbnail = FileField('Foto', validators=[DataRequired()])
    kategori_id = SelectField('Kategori Berita', validators=[DataRequired()])
    submit = SubmitField("Edit")

class UploadCSv(FlaskForm):
    csvField = FileField('CSV', validators=[DataRequired(), FileAllowed(['csv'])])
   # catatan  = TextAreaField("Catatan", validators=[DataRequired()])
    submit = SubmitField("Sv Fl")
    