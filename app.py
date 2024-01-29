from flask import Flask, render_template,request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'contactslist'
mysql = MySQL(app)


#settings
app.secret_key = 'mysecretkey'
# get contacts list 
@app.route("/")
def index():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts')
    data = cursor.fetchall()

    return render_template('index.html', contacts = data)

# add contact to database
@app.route("/add_contact", methods=['POST'])
def add_contact():
    if request.method == 'POST':
      fullname =  request.form['fullname']
      phone =  request.form['phone']
      email =  request.form['email']
      cursor = mysql.connection.cursor()
      
      cursor.execute('INSERT INTO contacts(fullname, phone, email) VALUES(%s, %s, %s)', 
                     (fullname, phone, email))
      mysql.connection.commit()
      flash('Contact Added successfully')
      return redirect(url_for('index'))
    
# get contact to edit by id
@app.route("/edit/<id>")
def get_contact(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id = %s',(id))
    data = cursor.fetchall()
    
    return render_template('edit_contact.html', contact = data[0])

# update contact by id
@app.route("/update/<id>", methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
     fullname = request.form['fullname']
     phone = request.form['phone']
     email = request.form['email']
     cursor = mysql.connection.cursor()
     cursor.execute("""
        UPDATE contacts SET 
        fullname = %s,
        phone = %s,
        email = %s
        WHERE id = %s
    """,(fullname,phone,email,id))
     mysql.connection.commit()
    flash('Contact Updated Successfully')
    return redirect(url_for('index'))

# delete contact by id
@app.route('/delete/<string:id>')
def delete_contact(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(port=3000, debug=True)