from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Folder to temporarily store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('base.html')

# ------------------- System Admin -------------------
@app.route('/system_admin', methods=['GET', 'POST'])
def system_admin():
    if request.method == 'POST':
        # Handle form submission
        master_node = request.form.get('master_node')
        job_name = request.form.get('job_name')
        forced_update = request.form.get('forced_update') == 'on'
        
        print("System Admin Form Submitted:")
        print(f"Master Node: {master_node}")
        print(f"Job Name: {job_name}")
        print(f"Forced Update: {forced_update}")
        
        return redirect(url_for('system_admin'))
    
    return render_template('system_admin.html')

# ------------------- Share Admin -------------------
@app.route('/share_admin', methods=['GET', 'POST'])
def share_admin():
    if request.method == 'POST':
        # Handle structured inputs
        compression = request.form.get('compression')
        retention = request.form.get('retention')
        cost = request.form.get('cost')
        ingress = request.form.get('ingress')
        egress = request.form.get('egress')
        
        # Handle file uploads
        uploaded_files = request.files.getlist('requirement_docs')
        for file in uploaded_files:
            if file.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                print(f"Uploaded file saved to: {filepath}")
        
        print("Share Admin Form Submitted:")
        print(f"Compression: {compression}, Retention: {retention}, Cost: {cost}, Ingress: {ingress}, Egress: {egress}")
        
        return redirect(url_for('share_admin'))
    
    return render_template('share_admin.html')

# ------------------- User -------------------
@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        filename = request.form.get('filename')
        print(f"User searched for file: {filename}")
        return redirect(url_for('user'))
    
    return render_template('user.html')

# ------------------- Run Flask -------------------
if __name__ == '__main__':
    app.run(debug=True)
