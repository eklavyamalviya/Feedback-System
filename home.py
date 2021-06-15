from flask import Flask,render_template,redirect,url_for,session,request,make_response,Response
from flask_mysqldb import MySQL
from flask import jsonify
from flask import json

app=Flask(__name__)
  

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'system'
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)
app.secret_key = "abc"





@app.route('/')
def form():
	return render_template('index2.html')

@app.route('/home')
def home():
   return render_template('index2.html')	

@app.route('/adhome')
def adhome():
   uname=session['uname']
   if uname==None:
   		print('session expired')
   return render_template('adhome.html',name=uname.capitalize())

@app.route('/shome')
def shome():
   uname=session['uname']
   return render_template('home.html',name=uname.capitalize())

@app.route('/feed' , methods=['GET', 'POST'])
def feed():
	if request.method=='POST' or request.method=='GET':
		sem1=request.form.get('sel')
		eid=session['eid']
		cur=mysql.connection.cursor()
		cur.execute("select sem,eid from sprofile")
		data=cur.fetchall()
		a=list(data)
		k,c=0,[]
		for i in data:
			a=list(data)
			if eid==a[k][1]:
				sem=a[k][0]
			k+=1
		sem1=int(sem1)
		print(sem1)	
		if sem1==1 or sem1==2:	
			e=sem-int(sem1)
			d="use sem"+str(e)
			print(d)
			cur.execute(d)
			cur.execute("select * from cse_stu")
			data=cur.fetchall()
			data=dict(data)
			return render_template('feed.html',last=int(sem)-1,last2=int(sem)-2,result=data)
		else:
			print('youououou')
			return redirect(url_for('feedback'))	

@app.route('/feedback')
def feedback():	
		eid=session['eid']
		cur=mysql.connection.cursor()
		cur.execute("select sem,eid from sprofile")
		data=cur.fetchall()
		a=list(data)
		k,c=0,[]
		for i in data:
			a=list(data)
			if eid==a[k][1]:
				sem=a[k][0]
			k+=1
		return render_template('feedback.html',last=int(sem)-1,last2=int(sem)-2)


@app.route('/add',methods=['POST','GET'])
def editadd():
	if request.method == 'POST':
		sem=request.form["sem"]
		branch=request.form["branch"]
		sid=request.form["sid"]
		name=request.form["sname"]
		d="use sem"+str(sem)
		e="INSERT INTO "+branch+"_stu(sid,sname) VALUES(%s,%s)"
		print(e)
		cur=mysql.connection.cursor()
		cur.execute(d)
		cur.execute(e,(sid,name))
		mysql.connection.commit()
		cur.close()
		return render_template('add.html')
	return render_template('add.html')		

@app.route('/del',methods=['POST','GET'])
def editdel():
	if request.method=="POST":
		branch=request.form['branch']
		session['sem']=request.form['sem']
		sem=session['sem']
		h="select sub_name from "+(str(branch))+"_stu"
		print(h)
		e,c="use sem"+str(sem),[]
		cur=mysql.connection.cursor()
		cur.execute(e)
		cur.execute(h)
		d=cur.fetchall()
		for i in range(len(d)):
			c.append(str(d[i][0]))
		return render_template('del.html',data=c)
	return render_template('del.html')

@app.route('/del1',methods=['POST','GET'])
def editdel1():
	if request.method=="POST":
		sub=request.form["sub"]
		sem=session['sem']
		e="use sem"+str(sem)
		cur=mysql.connection.cursor()
		cur.execute(e)
		cur.execute("delete from cse_stu where sub_name='%s'"%(str(sub)))
		mysql.connection.commit()
		cur.close()
		return render_template('del.html')
	return render_template('del.html')

@app.route('/asi',methods=['POST','GET'])
def editasi():
	if request.method=="POST":
		branch=request.form['branch']
		session['sem']=request.form['sem']
		sem=session['sem']
		h="select sub_name from "+(str(branch))+"_stu where sub_name not in(select sname from assign)"
		j="select name from "+(str(branch))+"_sign"
		e,c,l="use sem"+str(sem),[],[]
		cur=mysql.connection.cursor()
		cur.execute(e)
		cur.execute(h)
		d=cur.fetchall()
		for i in range(len(d)):
			c.append(str(d[i][0]))
		cur.execute('use faculty')
		cur.execute(j)
		d=cur.fetchall()
		for i in range(len(d)):
			l.append(str(d[i][0]))
		return render_template('asi.html',sdata=c,fdata=l)
	return render_template('asi.html')

@app.route('/asi1',methods=['POST','GET'])
def editasi1():
	if request.method=="POST":
		sname=request.form['sname']
		fname=request.form['fname']
		sem=session['sem']
		e="use sem"+str(sem)
		cur=mysql.connection.cursor()
		cur.execute(e)
		cur.execute("INSERT INTO assign(sname,fname) VALUES(%s , %s)",(sname,fname))
		mysql.connection.commit()
		cur.close()
		return redirect(url_for('asin'))
	return redirect(url_for('asin'))


@app.route('/asin')
def asin():
	return render_template('asi.html')


@app.route('/report1',methods=['POST','GET'])
def report1():
	if request.method=="POST":
		sem=request.form['sem']
		e="use sem"+str(sem)
		cur=mysql.connection.cursor()
		cur.execute(e)
		cur.execute("SELECT * FROM assign")
		d=cur.fetchall()
		mysql.connection.commit()
		cur.close()
		return render_template('rep.html',result=dict(d))
	return redirect(url_for('report'))

@app.route('/report')
def report():
	return render_template('report.html')

@app.route('/logout')
def logout():
   session.pop('uname', None)
   session.pop('eid', None)
   return redirect(url_for('home'))


def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        blob=file.write(data)
    print(blob)    
    return blob
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData



@app.route('/pro')
def spro():
	k=0
	cur = mysql.connection.cursor()
	cur.execute("select name,branch,sem,eid from sprofile")
	data=cur.fetchall()
	eid=session['eid']
	for i in data:
		a=data[k][3]
		if a==eid:
			c=list(data[k])
			for i in range(len(c)):
				name=c[0]
				branch=c[1]
				sem=c[2]
				eid=c[3]
		k+=1		
	mysql.connection.commit()
	cur.close()
	return render_template("pro.html",fname=name.capitalize(),lname=branch,sem=sem,eid=eid)

@app.route('/spro', methods=['POST','GET'])
def srpro():
	if request.method =='POST':
		photu = request.form['photu']
		print(photu)
		if photu:
			photu = convertToBinaryData(photu)
		name=request.form['fname']
		branch = request.form['lname']
		sem = request.form['sem']
		Eid = request.form['eid']
		cur = mysql.connection.cursor()
		if session['eid']==Eid:
			cur.execute("INSERT INTO sprofile(name,branch,sem,eid,photu) VALUES( %s , %s, %s, %s, %s)",(name,branch,sem,Eid,photu))
			mysql.connection.commit()
			cur.close()
			return redirect(url_for('shome'))
		else:
			flash("please enter the same enrollment number")
			return redirect(url_for('spro'))		
"""
@app.route('/demo')
def display_image():
    sql1="select * from sprofile"
    cur = mysql.connection.cursor()
    cur.execute(sql1)
    mysql.connection.commit()
    #db.commit()
    data=cur.fetchall()
   # a= writeTofile(data,'C:\\Users\\admin\\Desktop\\Django\\flask\\Scripts\\fac.jpg')
    name="fac"
    photoPath = "C:\\Users\\admin\\Desktop\\Django\\flask\\Scripts\\fac.jpg"
    #image = base64.b64decode(str(base64String))
    b = convertToBinaryData(photoPath)
    a = base64.b64encode(b)
    a = a.decode("UTF-8")
    for row in data:
            name = row[0]
            photo = row[4]
    photoPath = "C:\\Users\\admin\\Desktop\\Django\\flask\\Scripts\\fac.jpg"
    img=writeTofile(photo, photoPath)
    cur.close()
    #print(img)
    writeTofile(photo, photoPath)
    return render_template("demo1.html",data=a) """



@app.route('/sign', methods=['POST','GET'])
def sign():
	if request.method =='POST':
		user=request.form
		session['uname']=request.form['uname']
		session['eid']=request.form['eid']
		name=request.form['uname']
		eid=request.form['eid']
		psw=request.form['psw']
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO sign(name,eid,pass) VALUES( %s , %s, %s)",(name,eid,psw))
		mysql.connection.commit()
		cur.close()
		return render_template('FREG.html')



@app.route('/login', methods=['POST','GET'])
def login():
	if request.method =='POST':
		k=0
		session['uname']=request.form['uname']
		session['eid']=request.form['eid']
		sta=request.form['sta']
		eid=session['eid']
		uname=session['uname']
		psw = request.form['psw']

		if sta=="student":
			cur = mysql.connection.cursor()
			cur.execute("SELECT * FROM sign")
			for i in cur:
				c=list(i)
				if uname== c[0] and psw==c[2] and eid==c[1]:
					k+=1
			if k>0:
				resp = make_response(render_template('home.html',name=uname))
				resp.set_cookie('userID',uname)
				return redirect(url_for('shome'))
			else:
				return render_template('index2.html')
		elif sta=="admin":
			cur = mysql.connection.cursor()
			cur.execute("use admin")
			cur.execute("SELECT * FROM signad")	
			for i in cur:
				c=list(i)
				if uname== c[0] and psw==c[2] and eid==c[1]:
					k+=1
			if k>0:
				resp = make_response(render_template('adhome.html',name=uname))
				resp.set_cookie('userID',uname)
				return redirect(url_for('adhome'))
			else:
				abort(401)
				return render_template('index2.html')
	return render_template('index2.html')

if __name__ == "__main__" :
	app.run(debug=True)