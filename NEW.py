import mysql.connector as sql
conn= sql.connect(host='localhost', user = 'root', password ='vishak06',database ='sales')
c1=conn.cursor()
chpasswd='d'
print('''+--------------------------+
///////////////////////// 
/////////////////////////
//STATIONERY MANAGEMENT//
/////////////////////////
/////////////////////////
+--------------------------+''')
import datetime
d_day=datetime.date.today()
d_time=datetime.datetime.now()
print(d_day.day,"/",d_day.month,"/",d_day.year," ",d_time.hour,":",d_time.minute,)
print("============================================================================")
c1.execute('select product_no,product_name from stock;')
peee=c1.fetchall()
peee1=list(peee)
it=0
bill=0
while True:
    print("\n\n\n")
    print("============================================================================")
    print("1. CUSTOMER")
    print("2. ADMIN")
    print("3. EXIT")
    loggin=int(input('enter the choice:'))
    if loggin==1:
        while True:
            print("\n\n\n")
            print("===========================================================================================")
            print('''PRODUCT PRODUCT NAME''') 
            for i in range(0,int(len(peee))):
                print(peee[i] )
            b=input('product number: ')
            c1.execute('select product_name,cost_per_product from stock where product_no =' + b)
            data= c1.fetchall()
            data1=list(data[0])
            print('product name :', data1[0])
            print('cost of the product :', data1[1] )
            appr= input('do you want to buy it (Y/N) :')
            if appr == 'y' or appr =='Y' :
                c1.execute("update stock set stock = stock-1 where product_no= " + b )
                c1.execute("update stock set purchased = purchased+1 where product_no=" + b )
                bill+=int(data1[1]) 
                it+=1
                conn.commit()
                print("bought successfully!!!!")
                opn = input("Do you want buy any other thing (Y/N) : ")
                if opn == 'y' or opn == 'Y':
                    continue
                elif opn=='n' or opn=='N':
                    print('BILL')
                    print('''NUMBER OF ITEMS PURCHASED:''',it)
                    print('''TOTAL AMOUNT:''',bill)
                    print('''*******THANK YOU**************PLEASE VIST AGAIN*******''')
                    break
            elif appr =='n' or appr =='N':
                opn = input(" Do you want buy any other thing (Y/N) : ")
                if opn == 'y' or opn == 'Y':
                    continue
                elif opn == 'n' or opn =='N':
                    print(' BILL')
                    print('''NUMBER OF ITEMS PURCHASED:''',it)
                    print('''TOTAL AMOUNT:''',bill)
                    print('''*******THANK YOU**************PLEASE VIST AGAIN*******''')
                    break
            else:
                print('####invalid command####')
                break
                conn.commit()
    elif loggin==2:
        print("\n\n\n")
        print("*"*100)
        print("\t\t\t***WELCOME TO STATIONERY MANAGEMENT SYSTEM***")
        print("*"*100)
        print("STATIONERY MANAGEMENT SYSTEM")
        print(d_day.day,"/",d_day.month,"/",d_day.year," ",d_time.hour,":",d_time.minute,)
        chpasswd='d'
        while True:
            print("1.LOGIN")
            print("2.REGISTER")
            print("3.VIEW ALL USERS")
            print("4.EXIT")
            choice=int(input('ENTER THE CHOICE:'))
            print("============================================================================")
            print("\n\n\n")
            if choice == 1:
                us=input('USERNAME:')
                ps=input('PASSWORD:')
                c1.execute("select * from user where username = '{}' and passwd = '{}'".format(us , ps))
                data = c1.fetchall()
                if any(data) :
                    print("LOGIN SUCCESSFULL")
                    print("1. view stock")
                    print("2. add stock")
                    print("3. Adding a new product")
                    ch=int(input("Enter your choice :"))
                    if ch==1:
                        for i in range(0,int(len(peee))):
                            print(peee[i] )
                        a=input('Enter the product number :')
                        c1.execute("select * from stock where product_no="+a)
                        dt=c1.fetchall()
                        dt1=list(dt[0])
                        print("Product name :",dt1[1])
                        print("Cost per product:",dt1[2])
                        print("Stock available:",dt1[3])
                        print("Number items purchased :",dt1[4])
                        break
                    elif ch==2:
                        for i in range(0,int(len(peee))):
                            print(peee[i] )
                        prdno=input("Enter the product number of the product for which the stock is going to be updated:")
                        upd_value=int(input("enter the number of new stocks came:"))
                        c1.execute("update stock set stock=stock+" + str(upd_value) + " where product_no="+prdno)
                        conn.commit()
                        print("The stocks have been added")
                        break
                    elif ch==3:
                        pno1=input('Enter the product number of new product:')
                        pna=input('Enter the product name of the new product:')
                        cst=input('Enter the cost of the product:')
                        stock12=input('Enter the number of stocks of the new product arrived:')
                        pch='0'
                        c1.execute("insert into stock values(" + pno1 +','+'"'+pna+'"'+','+cst+','+stock12+','+pch+')')
                        print("Added sucessfully!!!!!!!")
                        conn.commit()
                        break
                    else:
                        print('####INVALID OPTION ####')
                        break
                else:
                    print('''..SORRY..WRONG.......USERNAME OR PASSWORD''')
            elif choice == 2:
                print("===========================================================================================")
                li=input('ENTER THE NEW USER ID:')
                while True:
                    li2=input('ENTER YOUR PASSWORD:')
                    li3=input('ENTER YOUR PASSWORD AGAIN(to confirm):')
                    if li2== li3:
                        c1.execute("insert into user values("+'"'+li+'",'+'"'+li3+'")')
                        print("ID has been successfully created:")
                        conn.commit()
                        break
                break
            elif choice ==3:
                c1.execute("select username from user")
                data = c1.fetchall()
                for row in data :
                    print(row)
                break    
            elif choice == 4:
                print(".......................LOGGING...........OUT................")
                break
            else:
                print('please enter the right option')
    elif loggin== 3:
        print("...QUITING... ")
        break 
    else:
        print("###INVALID OPTION####")
