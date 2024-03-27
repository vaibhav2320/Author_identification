from flask import Flask, render_template, request, redirect, url_for, flash
from flask.globals import session
import os
import os.path
import author_model as a_model
app = Flask(__name__,template_folder='template')
app.secret_key = '1F4453C6EA2C5B454D221285FFFFC'

@app.route('/')  
def index():
    if 'username' in session and session['username'] != 'admin':
        return redirect(url_for('user'))
    elif 'username' in session and session['username'] == 'admin':
        return redirect(url_for('admin'))
    else:
        return render_template('login.html')
    
@app.route('/login_nav', methods=['GET','POST'])
def login_nav(): 
    msg='Fill details..'
    return render_template('login.html', msg = msg)

@app.route('/login', methods=['GET','POST'])
def login(): 
    username=request.form['username']
    password = request.form['password']
    if username=="admin" and password=="admin":
        session['username'] = username
        return redirect(url_for('admin'))
    
    else:
            msg='login Failed'
            return redirect(url_for('login_nav'))

@app.route('/admin')
def admin():
    if 'username' in session:
        user = session['username']
        return render_template('admin_home.html')
    else:
        return redirect(url_for('login_nav'))
    
@app.route('/train_model')
def train_model():
    myarray=[]
    if 'username' in session:
        return render_template('author_predict_train.html', DataOut= myarray)
    else:
        return redirect(url_for('login_nav'))

@app.route('/train_model_save',methods=["GET","POST"])
def train_model_save():
    
    file_exist_status=os.path.exists('authorship_model.joblib')
    if file_exist_status==True:
        return render_template('author_predict_train.html', DataOut= "Model Already Trained!!")
    else:
        a_model.train_authorship_model()
        if 'username' in session:
            return render_template('author_predict_train.html', DataOut= "Model Successfully Trained!!")
        else:
            return redirect(url_for('login_nav'))


@app.route('/authorPredict_nav')
def authorPredict_nav():
        return render_template('authorpredict.html', DataOut= "")

@app.route('/predictAuthor',methods=["GET","POST"])
def predictAuthor():
    input_paragraph=request.form['para']
    file_exist_status=os.path.exists('authorship_model.joblib')
    if file_exist_status==False:
        return render_template('authorpredict.html', DataOut= "Please train model first!")
    else:
        if 'username' in session:
            author=a_model.predict_author(input_paragraph)
            return render_template('authorpredict.html',text_ = input_paragraph, DataOut= author)
        else:
            return redirect(url_for('login_nav'))



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_nav')) 

        
if __name__ == '__main__':  
    app.run(debug=True)
