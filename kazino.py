from flask import Flask, render_template, url_for, request
from werkzeug.utils import redirect
from dotenv import load_dotenv
from mail_sender import send_email
import mail_sender
import sqlite3
import random

app = Flask(__name__)
load_dotenv()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('kazi_log.html')


@app.route('/tosubscribe', methods=['GET'])
def reg():
    return render_template('kazi_reg.html')


@app.route('/tosubscribe_t', methods=['GET'])
def reg_false():
    return render_template('kazi_reg_false.html')


@app.route('/register', methods=['POST'])
def register():
    global a, user_pas
    x = request.form['username']
    a = x
    print(x)
    x = request.form['password']
    print(x)
    z = request.form['pass']
    if z == x:
        print('Успешно')
        user_pas = request.form['password']
        return redirect(url_for('post_form'))
    else:
        return redirect(url_for('reg_false'))


@app.route('/post_form', methods=['GET'])
def post_form():
    email = a
    if send_email(email):
        return(redirect('reg_info'))
    else:
        print('Произошла ошибка')

@app.route('/reg_info', methods=['GET'])
def reg_info():
    return render_template('login.html')


@app.route('/reg_status', methods=['POST'])
def reg_status():
    input_token = request.form['token']
    out_token = mail_sender.ttt
    print(input_token, out_token)
    if input_token == out_token[0]:
        conn = sqlite3.connect("reg_info.db")
        cursor = conn.cursor()
        sqlite_connection = sqlite3.connect('reg_info.db')
        cursor.execute(f"""INSERT INTO profile (name, passw, money)
                        VALUES ('{a}', '{user_pas}', '5000')
                       """)
        conn.commit()
        return(redirect('login_success'))
    else:
        return(redirect('token_error'))


@app.route('/token_error', methods=['GET'])
def token_error():
    return render_template('token_error.html')


@app.route('/login_success', methods=['GET'])
def login_success():
    return render_template('login_success.html')


@app.route('/authorization', methods=['POST'])
def authorization():
    global mail_check, pass_check, lss
    lss = []
    mail_check = request.form['name_check']
    pass_check = request.form['pass_check']
    print(mail_check, pass_check)
    conn = sqlite3.connect("reg_info.db")
    cursor = conn.cursor()
    sql = "SELECT * FROM profile WHERE name=?"
    cursor.execute(sql, [(mail_check)])
    if cursor.fetchone() is None:
        conn.commit()
        return redirect('login_not_found')
    else:
        sql = "SELECT * FROM profile WHERE name=?"
        cursor.execute(sql, [(mail_check)])
        if cursor.fetchone()[2] == str(pass_check):
            conn.commit()
            return redirect('Russian Рулетка')
        else:
            mail_check = ''
            pass_check = ''
            conn.commit()
            return redirect('login_f')


@app.route('/login_f', methods=['GET'])
def login_f():
    return render_template('kazi_log_false.html')


@app.route('/login_not_found', methods=['GET'])
def login_not_found():
    return render_template('kazi_email_false.html')


@app.route('/set_password', methods=['POST'])
def set_password():
    global input_mail
    email = request.form['in_ema']
    input_mail = email
    send_email(email)
    return(redirect('give_token'))


@app.route('/give_token', methods=['GET'])
def give_token():
    return render_template('password_reset.html')


@app.route('/set_pass_toke', methods=['POST'])
def set_pass_toke():
    out_token = mail_sender.ttt
    input_token = request.form['token']
    if input_token == out_token[0]:
        print(12345)
        return(redirect('password_reset_success'))
    else:
        return(redirect('password_reset_false'))


@app.route('/password_reset_false', methods=['GET'])
def password_reset_false():
    return render_template('password_reset_false.html')


@app.route('/password_reset_success', methods=['GET'])
def password_reset_success():
    return render_template('pass_reset_success.html')


@app.route('/pass_change', methods=['POST'])
def pass_change():
    x = request.form['miran']
    y = request.form['danila']
    if x == y:
        conn = sqlite3.connect("reg_info.db")
        cursor = conn.cursor()
        print(1233)
        print(input_mail)
        do = f"""UPDATE profile SET passw = '{y}' WHERE name = '{input_mail}'"""
        cursor.execute(do)
        conn.commit()
        return render_template('good_change.html')
    else:
        return render_template('password_repeat.html')


@app.route('/input_email', methods=['GET'])
def input_email():
    return render_template('input_email.html')


@app.route('/Russian Рулетка', methods=['POST', 'GET'])
def Russian_Roulette():
    global mon_lis
    mon_lis = []
    if mail_check != '' and pass_check != '':
        lss.append(mail_check)
        lss.append(pass_check)
        param = {}
        param['uname'] = mail_check
        param['pass_n'] = pass_check
        print(param['uname'])
        conn = sqlite3.connect("reg_info.db")
        cursor = conn.cursor()
        sql = "SELECT * FROM profile WHERE name=?"
        cursor.execute(sql, [(mail_check)])
        param['mon'] = cursor.fetchone()[3]
    else:
        param = {}
        param['uname'] = lss[-2]
        param['pass_n'] = lss[-1]
        print(param['uname'])
        conn = sqlite3.connect("reg_info.db")
        cursor = conn.cursor()
        sql = "SELECT * FROM profile WHERE name=?"
        cursor.execute(sql, [(mail_check)])
        param['mon'] = cursor.fetchone()[3]
    mon_lis.append(param['mon'])
    return render_template('Russian_Roulette.html', **param)

@app.route('/Башня', methods=['POST', 'GET'])
def bash():
    return(render_template('slot.html'))
    
@app.route('/Слоты', methods=['POST', 'GET'])
def slot():
    print(mon_lis)
    return(render_template('slot.html'))

@app.route('/Рулетка', methods=['POST', 'GET'])
def ryletka():
    return(render_template('slot.html'))

@app.route('/slot_up', methods=['POST'])
def move_slot():
    money = request.form['stavka']
    money = int(money)
    a = ["банан", "банан", "банан", "арбуз", "арбуз", "арбуз", "вишня", "вишня", "клубника", "клубника", "7"]
    s = random.choice(a)
    d = random.choice(a)
    q = random.choice(a)
    if s == "банан" and s == d == q or s == "арбуз" and s == d == q:
        money = 20 * money
        print(s, d, q, money)
    elif s == "вишня" and s == d == q or s == "клубника" and s == d == q:
        money = money * 50
        print(s, d, q, money)
    elif s == "7" and s == d == q:
        money = money * 250
        print(s, d, q, money)
    else:
        money += 5
    print('asdsad')
    return redirect('Слоты')



if __name__ == '__main__':
    app.run()
