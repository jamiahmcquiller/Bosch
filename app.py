from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/system_admin', methods=['GET', 'POST'])
def system_admin():
    if request.method == 'POST':
        # handle form submission
        print(request.form)
        return redirect(url_for('system_admin'))
    return render_template('system_admin.html')

@app.route('/share_admin', methods=['GET', 'POST'])
def share_admin():
    if request.method == 'POST':
        print(request.form)
        return redirect(url_for('share_admin'))
    return render_template('share_admin.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        print(request.form)
        return redirect(url_for('user'))
    return render_template('user.html')

if __name__ == '__main__':
    app.run(debug=True)
