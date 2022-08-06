from flask import Flask, render_template, redirect, url_for, Blueprint, request, jsonify
from flask.globals import request  
from affairs.admin.forms import Admin, KategoriF, LoginA, ArtikelP, editArtikel, UploadCSv
from affairs import db, app,bcrypt
from affairs.models import admindb, Kategori, Artikel, CustomerPgAir
from flask_login import login_user, logout_user, current_user, login_required 
import os
import csv
import secrets
import json

admingam = Blueprint('admingam', __name__)

def gthumbnail(file_foto):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file_foto.filename)
    nama_gambar = random_hex + f_ext
    file_foto.save(os.path.join(app.root_path, 'affairs/static/img', nama_gambar))
    return nama_gambar
    
def savecsv(file_csv):
    data = []
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file_csv.filename)
    nama_csv = random_hex + f_ext
    file_csv.save(os.path.join(app.root_path, 'affairs/static/csv', nama_csv))
    
    with open('affairs/static/csv/' + nama_csv) as file:
        csvfile = csv.DictReader(file)
        for row in csvfile:
          data.append(row)
        return data
        
    

@admingam.route("/")
def home():
    halaman = request.args.get('halaman', 1, type=int)
    daf_ar = Artikel.query.order_by(Artikel.id.desc()).paginate(page=halaman, per_page=3)
    return render_template("index.html", daf_ar=daf_ar)

@admingam.route('/baca_ar/<int:id>')
def baca_ar(id):
    bca = Artikel.query.get_or_404(id)
    return render_template('baca_ar.html', bca=bca)

@admingam.route("/about")
def about():
    return render_template("about.html")

@admingam.route("/contact")
def contact():
    return render_template("contact.html")
 
@admingam.route("/post")
def post():
    return render_template("post.html")
#risno456
@admingam.route("/admin", methods=["GET","POST"])

def admin():
    form = Admin()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        kelu = admindb(username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(kelu)
        db.session.commit()
        return redirect(url_for("admingam.home"))
    return render_template("admin.html", form=form)

@admingam.route("/login_adm", methods=["GET","POST"])
def login_adm():
    form=LoginA()
    if form.validate_on_submit():
        cekmail = admindb.query.filter_by(email=form.email.data).first()
        if cekmail and bcrypt.check_password_hash(cekmail.password, form.password.data):
            login_user(cekmail)
            return redirect(url_for("admingam.admin_panel"))
        else:
            print("login salah harap periksa email dan password")
    return render_template("login.html", form=form)

@admingam.route('/logout_adm')
def logout_adm():
    logout_user()
    return redirect(url_for('admingam.home'))

@admingam.route("/tambahkat", methods=["GET","POST"])
@login_required
def tambah_kat():
    form = KategoriF()
    if form.validate_on_submit():
        nama = Kategori(nama=form.nama_kat.data)
        db.session.add(nama)
        db.session.commit()
        return redirect(url_for("admingam.admin"))
    return render_template("kategori.html", form=form)
    
@admingam.route("/tambah_artikel", methods=["GET","POST"])
@login_required
def tambah_artikel():
  form=ArtikelP()
  form.kategori_id.choices = [(str(kategori_id.id), kategori_id.nama) for kategori_id in Kategori.query.all()]
  if form.validate_on_submit():
    random_hex = secrets.token_hex(8)
    gambar = form.thumbnail.data
    _, f_ext = os.path.splitext(gambar.filename)
    nama_gambar = random_hex + f_ext
    gambar.save(os.path.join(app.root_path, 'affairs/static/img', nama_gambar))
    artl = Artikel(judul=form.judul.data, konten=form.konten.data, thumbnail=nama_gambar ,kategori_id=form.kategori_id.data)
    db.session.add(artl)
    db.session.commit()
    return redirect(url_for('admingam.admin_panel'))
  #form.kategori_.choices.insert(0, ('','===pilih kategori==='))
  return render_template("Artikel.html",form=form, title='Tambah Berita')

@admingam.route('/admin_panel')
@login_required
def admin_panel():
    artl = Artikel.query.all()
    return render_template('admin_panel.html', artl=artl, title='Admin Panel')

@admingam.route('/edit_artikel/<int:id>', methods=["GET","POST"])
def edit_artikel(id):
    form=editArtikel()
    ed_a = Artikel.query.get_or_404(id)
    form.kategori_id.choices = [(str(kategori_id.id), kategori_id.nama) for kategori_id in Kategori.query.all()]
    if request.method == "GET":
        form.judul.data = ed_a.judul
        form.konten.data = ed_a.konten
        form.thumbnail.data = ed_a.thumbnail
        form.kategori_id.data = ed_a.kategori_id
    elif form.validate_on_submit():
        if form.thumbnail.data:
            foto = gthumbnail(form.thumbnail.data)
            ed_a.thumbnail = foto
        ed_a.judul = form.judul.data
        ed_a.konten = form.konten.data
        ed_a.kategori_id = form.kategori_id.data
        db.session.commit()
        return redirect(url_for('admingam.admin_panel'))
    return render_template("edit_artikel.html", form=form, title='Edit Berita')

@admingam.route("/hapus_ar/<int:id>",  methods=["POST"])
@login_required
def hapus_ar(id):
    art = Artikel.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(art)
        db.session.commit()
        return redirect(url_for('admingam.admin_panel'))
    return redirect(url_for('admingam.admin_panel'))

@admingam.route('/csvupload', methods=["GET","POST"])
@login_required
def csvupload():
    return render_template('upload_csv.html')



@admingam.route("/displaycsv",  methods=["GET","POST"])
@login_required
def displaycsv():
    data = []
    form = UploadCSv()
    if form.validate_on_submit():
      fcsv = savecsv(form.csvField.data)
      cus = CustomerPgAir(csv_field=fcsv)
      db.session.add(cus)
      db.session.commit()
      return redirect(url_for('admingam.home'))
    return render_template('displayfile.html', form=form, title="upload file")
    
@admingam.route('/lamanrek')
def lamanrek():
    rek = CustomerPgAir.query.all()
    return render_template('lamanrek.html', rek=rek,title='Daftar Rekening Bulanan')
            
@admingam.route('/hapusrek/<int:id>')
@login_required
def hapusrek(id):
    hps = CustomerPgAir.query.get_or_404(id)
    db.session.delete(hps)
    db.session.commit()
    return redirect(url_for('admingam.home'))            

@admingam.route('/lihatrek/<int:id>')
def lihatrek(id):
    rek = CustomerPgAir.query.filter_by(id=id).all()

    return render_template('lihatrek.html', rek=rek, title="tabel daftar")  
