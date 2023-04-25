from flask import(
    Flask,
    request,
    render_template,
    redirect,
    session,
    url_for,

)
from service import WebService
import os 
app = Flask(__name__)
app.secret_key='1234'


@app.route('/')
def login():
    if 'username' in session:
        return redirect("/home")
    return render_template("login.html")

@app.route("/log",methods=['POST'])
def connect():
    username = request.form["user"]
    password = str(request.form["pass"])
    good=services.loggin(username,password)
    if good == True:
        session['username'] = username
        return redirect("/home")
    else:
        return render_template("login.html",error=good)

@app.route('/home')
def homepage():
    username = session.get('username')
    test=services.homepage(username)
    admin= services.getuser(username)
    files=services.file_nbr(username)
    dirs=services.dir_nbr(username)
    space=services.stockage(username)
    return render_template("home.html", home_dir=admin, files=test, os=os,nbrfiles=files,nbrdirs=dirs,nbrspace=space)
@app.route("/view_file")
def view_file():
    filename = request.args.get("filename")
    username = session.get('username')
    path=f"/home/{username}/{filename}"
    try:
        with open(path) as f :
            contents = f.read()
    except FileNotFoundError:
        return "File not found " + os.getlogin()
    return render_template("view_file.html", fielname=filename,contents=contents)

@app.route('/logout')
def logout():
  if 'username' in session:
    session.pop('username')
    return redirect('/')
@app.route("/download_zip", methods=["POST"])
def download_zip():
    username = session.get('username')
    services.create_zip_archive(username)
    return "Archive created and downloaded!"

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query")

        username = session.get('username')
        home_dir=f"/home/{username}"
        matching_files = []
        for root, dirs, files in os.walk(home_dir):
            for file in files:
                if query in file:
                    matching_files.append(os.path.join(root, file))
        return render_template("search.html", matching_files=matching_files)
    else:
        return render_template("search_form.html")
if __name__=='__main__':
    services=WebService()
    app.run(host="0.0.0.0",port=9595,debug=True)