from flask import Flask,render_template,request,redirect,url_for
import pymssql

#创建flask实例
app=Flask(__name__)
app.secret_key="12345678"
#连接到数据库
DB_Config = {
    'server':'localhost',
    'database':'JY',
    'username':'sa',
    'password':'password'
}

def get_db_connection():
    return pymssql.connect(
        server=DB_Config['server'],
        database=DB_Config['database'],
        user=DB_Config['username'],
        password=DB_Config['password']
    )

#渲染html模板
@app.route('/')
def index():
    conn=get_db_connection()
    cursor=conn.cursor(as_dict=True)#以字典形式返回
    cursor.execute("select * from book")
    books=cursor.fetchall()
    conn.close()
    return render_template('index.html',books=books)

@app.route('/add',methods=['GET','POST'])
def add_book():
    if request.method=='POST':
        book_id=request.form['book_id']
        book_name=request.form['book_name']
        book_isbn=request.form['book_isbn']
        book_author=request.form['book_author']
        book_publisher=request.form['book_publisher']
        book_price=float(request.form['book_price'])
        interview_times=int(request.form['interview_times'])

        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(
            """
            insert into book(book_id,book_name,book_isbn,book_author,book_publisher,book_price,interview_times)
            values(%s,%s,%s,%s,%s,%s,%s)
            """,
            (book_id,book_name,book_isbn,book_author,book_publisher,book_price,interview_times)
        )
        conn.commit()
        conn.close()
        print("添加成功！")
        return redirect(url_for('index'))
    return render_template('form.html',action="添加")

@app.route('/edit/<string:book_id>',methods=['GET','POST'])
def edit_book(book_id):
    conn=get_db_connection()
    cursor=conn.cursor(as_dict=True)
    cursor.execute("select * from book where book_id=%s",(book_id,))
    book=cursor.fetchone()
    conn.close()

    if not book:
        return redirect(url_for('index'))
    
    if request.method=='POST':
        book_new_id=request.form['book_id']
        book_name=request.form['book_name']
        book_isbn=request.form['book_isbn']
        book_author=request.form['book_author']
        book_publisher=request.form['book_publisher']
        book_price=float(request.form['book_price'])
        interview_times=int(request.form['interview_times'])

        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(
            """
            update book
            set book_id=%s,book_name=%s,book_isbn=%s,book_author=%s,book_publisher=%s,book_price=%s,interview_times=%s
            where book_id=%s
            """,
            (book_new_id,book_name,book_isbn,book_author,book_publisher,book_price,interview_times,book_id)
        )
        conn.commit()
        conn.close()
        print("修改成功！")
        return redirect(url_for('index'))

    return render_template('form.html',book=book,action='编辑')


@app.route('/delete/<string:book_id>',methods=['GET','POST'])
def delete_book(book_id):
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute("delete from book where book_id=%s",(book_id,))
    conn.commit()
    conn.close()
    print("删除成功！")
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True)