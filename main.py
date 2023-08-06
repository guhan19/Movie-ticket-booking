import cx_Oracle
from tkinter import *
import datetime
class App:
    def __init__(self,root,cursor,con):
        self.con=con
        self.root=root
        self.cursor=cursor
        self.loggedInUser = None
        self.theater_id=None
        self.ticket_id=None
        self.show_id=None
        self.login()
        self.log_frame.tkraise()
        self.error=Label(self.root,text="Invalid Username/password!",fg="white",bg="darkblue",font=16)        
    def login(self):
        self.log_frame = Frame(self.root, bd=2, bg='#CCCCCC',relief=SOLID, padx=10, pady=10)
        Label(self.log_frame, text="Enter Username", bg='#CCCCCC').grid(row=0, column=0, sticky=W, pady=10)
        Label(self.log_frame, text="Enter Password", bg='#CCCCCC').grid(row=1, column=0, sticky=W, pady=10)
        Label(self.log_frame, text="Not registered yet?", bg='#CCCCCC').grid(row=3, column=0, sticky=W, pady=10)

        self.log_name = Entry(self.log_frame)
        self.log_pwd = Entry(self.log_frame, show='*')
        self.log_btn = Button(self.log_frame, width=15, text='LOG-IN',relief=SOLID,cursor='hand2',command=self.verify)
        self.create = Button(self.log_frame, width=15, text='Create an account',activebackground="Darkblue",activeforeground="White",command=self.registerpage)

        self.log_name.grid(row=0, column=1, pady=10, padx=20)
        self.log_pwd.grid(row=1, column=1, pady=10, padx=20)
        self.log_btn.grid(row=2, column=1, pady=10, padx=20)
        self.create.grid(row=3, column=1, pady=10, padx=20)
        self.log_frame.pack(padx=100,pady=100)

    def register(self):
        self.register_frame = Frame(self.root, bd=2, bg='#CCCCCC',relief=SOLID, padx=10, pady=10)

        Label(self.register_frame, text="Username(Unique)", bg='#CCCCCC').grid(row=0, column=0, sticky=W, pady=10)
        Label(self.register_frame, text="Enter Name", bg='#CCCCCC').grid(row=1, column=0, sticky=W, pady=10)
        Label(self.register_frame, text="Enter Email", bg='#CCCCCC').grid(row=2, column=0, sticky=W, pady=10)
        Label(self.register_frame, text="Contact Number", bg='#CCCCCC').grid(row=3, column=0, sticky=W, pady=10)
        Label(self.register_frame, text="Enter Password", bg='#CCCCCC').grid(row=4, column=0, sticky=W, pady=10)
        self.register_uname=Entry(self.register_frame)
        self.register_name = Entry(self.register_frame)
        self.register_email = Entry(self.register_frame)
        self.register_mobile = Entry(self.register_frame)
        self.register_pwd = Entry(self.register_frame, show='*')
        self.register_btn = Button(self.register_frame, width=15, text='Register',  relief=SOLID,cursor='hand2',command=self.cus_insert)

        self.register_uname.grid(row=0, column=1, pady=10, padx=20)
        self.register_name.grid(row=1, column=1, pady=10, padx=20)
        self.register_email.grid(row=2, column=1, pady=10, padx=20) 
        self.register_mobile.grid(row=3, column=1, pady=10, padx=20)
        self.register_pwd.grid(row=4, column=1, pady=10, padx=20)
        self.register_btn.grid(row=5, column=1, pady=10, padx=20)
        self.register_frame.pack(padx=100,pady=100)
    
    def theater_movies(self,th_id):
        self.tl_frame.pack_forget()
        self.theater_id=th_id
        self.show_frame = Frame(self.root, bd=3, bg="#CCCCCC", relief=SOLID)
        self.show_frame.config(width=1000, height=1000)
        self.dates_list = [""] * 7
        date = datetime.datetime.now()
        for i in range(7):
            self.dates_list[i] = date.strftime("%d-%b-%y")
            date += datetime.timedelta(days=1)
        switch_date = [None] * 7
        self.print_shows(0)
        for i in range(7):
            switch_date[i] = Button(self.show_frame,text=self.dates_list[i],width=15,activebackground="blue",padx=5,pady=5,command=lambda i=i: self.print_shows(i))
            switch_date[i].grid(column=i,row=0)
        self.show_frame.pack(padx=100, pady=100)
    def print_shows(self,date_pos):
        sid_list=[]
        current_date = self.dates_list[date_pos]
        self.cursor.execute(f"select show_id,movie_name,show_time,available_seats from movie natural join show where th_id=%s and show_date='%s'"%(self.theater_id,current_date))
        records = self.cursor.fetchall()
        details = [""] * len(records)
        for i in range(len(records)):
            for j in range(len(records[i])):
                if(j==0):
                    sid_list.append(records[i][j])
                elif(j==len(records[i])-1):
                    details[i] +="Available Seats:"+str(records[i][j]) + "|"
                else:     
                    details[i] += str(records[i][j]) + "|"
            details[i]+=current_date
        Label(self.show_frame,text="Select movie and show_time :",width=50,bg="Gray").grid(row=2, column=3,columnspan=1,padx=10,pady=10)
        for i in range(len(details)):
            movies = Button( self.show_frame,text=details[i],width=50,activebackground="blue",padx=5,pady=5,command=lambda i=i:self.seat_selection(sid_list[i]))
            movies.grid(row=3 + i, column=3,columnspan=1,padx=10,pady=10)
    def ticket_information(self):
        self.seats_frame.pack_forget()
        self.booking_frame.pack_forget()
        self.tInformation_frame=LabelFrame(self.root,text="Ticket Successfully booked:", bd=3, bg="#CCCCCC", relief=SOLID)
        Label(self.tInformation_frame,text="Theatre-id:",width=10).grid(row=0,column=0,padx=10,pady=10)
        Label(self.tInformation_frame,text="Ticket-id:",width=10).grid(row=1,column=0,padx=10,pady=10)
        Label(self.tInformation_frame,text="show_id:",width=10).grid(row=2,column=0,padx=10,pady=10)
        Label(self.tInformation_frame,text=self.theater_id,width=10).grid(row=0,column=1,padx=10,pady=10)
        Label(self.tInformation_frame,text=self.ticket_id,width=10).grid(row=1,column=1,padx=10,pady=10)
        Label(self.tInformation_frame,text=self.show_id,width=10).grid(row=2,column=1,padx=10,pady=10)
        self.tInformation_frame.pack(padx=100,pady=100)
    def booking(self):
        self.cursor.execute("select max(ticket_id) from tickets")
        self.con.commit()
        records=self.cursor.fetchall()
        seats=self.seatno.get()
        seats=seats.split(',')
        if records[0][0] is None:
            self.ticket_id=1
        else:
            self.ticket_id=int(records[0][0])+1
        print(self.ticket_id)
        self.cursor.execute(f"Insert into tickets values(ticket_id.nextval,:show_id,:c_id)",{'show_id':self.show_id,'c_id':self.loggedInUser})
        self.con.commit()

        for i in range(len(seats)):
            self.cursor.execute(f"Insert into booked_seats values(b_id.nextval,:ticket_id,:seat_no)",{'ticket_id':self.ticket_id,'seat_no':int(seats[i])}) 
        self.cursor.execute("Update show set available_seats=available_seats-%d where show_id=%s"%(len(seats),self.show_id))
        self.con.commit() 
        self.ticket_information()
    def seat_selection(self,show_id):
        self.show_frame.pack_forget()
        self.seats_frame=Frame(self.root, bd=3, bg="#CCCCCC", relief=SOLID)
        self.show_id=show_id
        self.cursor.execute(f"select no_of_seats from  theater where t_id=%d"%(self.theater_id))
        records=self.cursor.fetchall()
        total_seats=records[0][0]
        self.cursor.execute(f"select seat_no from booked_seats  b,tickets  t where b.ticket_id=t.ticket_id and t.show_id=%d"%(self.show_id))
        records=self.cursor.fetchall()
        print("show_id::",show_id,"booked_seats::",records)
        print(f"select seat_no from booked_seats  b,tickets  t where b.ticket_id=t.ticket_id and t.show_id=%d"%(self.show_id))
        records = [record[0] for record in records]
        print(records)
        row=1
        col=0
        for i in range(1,total_seats+1):
            if i in records:
                seats=Button(self.seats_frame,text=i,fg="white",bg="red",padx=10,pady=10)
                seats.grid(row=row,column=col,padx=10,pady=10)
            else:
                seats=Button(self.seats_frame,text=i,fg="white",bg="Green",padx=10,pady=10)
                seats.grid(row=row,column=col,padx=10,pady=10)
            col+=1
            if(i%10==0):     
                row+=1
                col=0
        self.seats_frame.pack(padx=50, pady=50)
        self.booking_frame=Frame(self.root, bd=3, bg="#CCCCCC", relief=SOLID)
        Label(self.booking_frame,text="Enter seat number:").grid(row=1,column=0)
        self.seatno=Entry(self.booking_frame)
        self.Book = Button(self.booking_frame, width=15, text='Book-Ticket',relief=SOLID,cursor='hand2',command=self.booking)
        Label(self.booking_frame,text="Available",bg="Green",fg="black").grid(row=0, column=0, pady=10, padx=20)
        Label(self.booking_frame,text="Booked",bg="Red",fg="black").grid(row=0, column=1, pady=10, padx=20)
        self.seatno.grid(row=1, column=1, pady=10, padx=20)
        self.Book.grid(row=2, column=1, pady=10, padx=20)
        self.booking_frame.pack(padx=50, pady=50)

    def Theater_selection(self):
        self.cursor.execute(f"select * from theater")
        records=self.cursor.fetchall()
        t_id=[]
        details=[""]*len(records)
        for i in range(len(records)):
            for j in range(len(records[i])):
                if(j==0):
                    t_id.append(records[i][j])
                details[i]+=str(records[i][j])+"|"
            
        self.tl_frame=LabelFrame(self.root,text="Click to select theater:",font=20,bd=3,bg='#CCCCCC',relief=SOLID,padx=20,pady=20)
        Theater1=Button(self.tl_frame,text=details[0],fg="white",bg="Black",command=lambda:self.theater_movies(t_id[0]))
        Theater2=Button(self.tl_frame,text=details[1],fg="white",bg="Black",command=lambda:self.theater_movies(t_id[1]))
        Theater3=Button(self.tl_frame,text=details[2],fg="white",bg="Black",command=lambda:self.theater_movies(t_id[2]))
        Theater1.grid(row=0,column=0,padx=10,pady=10)
        Theater2.grid(row=1,column=0,padx=10,pady=10)
        Theater3.grid(row=2,column=0,padx=10,pady=10)
        self.tl_frame.pack(padx=200,pady=200)
    def cus_insert(self):
        self.loggedInUser=self.register_uname.get()
        uname=self.register_uname.get()
        name=self.register_name.get()
        pwd=self.register_pwd.get()
        phoneno=self.register_mobile.get()
        emailid=self.register_email.get()
        self.cursor.execute(f"insert into customer values(:name,:c_id,:pwd,:phoneno,:emailid)",{'name':name,'c_id':uname,'pwd':pwd,'phoneno':phoneno,'emailid':emailid})
        self.con.commit()
        self.cursor.execute(f'select * from customer where c_id=:uname and c_password=:pwd',{'uname':uname,'pwd':pwd})
        self.con.commit()
        record =self.cursor.fetchall()
        print(record)
        if record:
            self.register_success()
        else:
            self.incorrect_user()
    def registerpage(self):
        self.log_frame.pack_forget()
        self.register()
        self.register_frame.tkraise()
    def register_success(self):
        self.error.destroy()
        self.register_frame.pack_forget()
        self.Theater_selection()
        self.self.tl_frame.tkraise()
    def login_success(self):
        self.error.destroy()
        self.log_frame.pack_forget()
        self.Theater_selection()
        self.tl_frame.tkraise()
    def incorrect_user(self):
        self.error.destroy()
        self.error=Label(self.root,text="Invalid Username/password!",fg="white",bg="darkblue",font=16)
        self.error.pack()
    def verify(self):
        uname=self.log_name.get()
        pwd=self.log_pwd.get()
        self.cursor.execute(f'select * from customer where c_id=:uname and c_password=:pwd',{'uname':uname,'pwd':pwd})
        record =self.cursor.fetchall()
        print(record)
        if record:
            self.loggedInUser = uname
            self.login_success()
        else:
            self.incorrect_user()
        self.con.commit()
if __name__ == "__main__":
    try:
        con = cx_Oracle.connect('scott/orcl@//localhost:1521/orcl')
        cursor=con.cursor()
        root = Tk()
        root.title('Movie reservation')
        root.config(bg='gray')
        webname=Label(root,text="Movie Ticket Reservation",fg="white",bg="darkblue",font=24)
        webname.pack()
        m=App(root,cursor,con)
    except cx_Oracle.DatabaseError as e:
        print("Problem connecting to Oracle", e)
        # Close the all database operation
    finally:
        if root:
            root.mainloop()
        if cursor:
            cursor.close()
        if con:
            con.close()
