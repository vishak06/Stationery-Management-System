import mysql.connector as sql
conn= sql.connect(host='localhost', user = 'root', password ='vishak06',database ='sales')
c1=conn.cursor()
chpasswd='d'
print('''+--------------------------+
///////////////////////// 
/////////////////////////
STATIONERY MANAGEMENT
////////////////////////
///////////////////////
+--------------------------+''')
c1.execute('select product_no,product_name,stock from stock;')
peee=c1.fetchall()
peee1=list(peee)
print('''PRODUCT PRODUCT NAME NO''') 
for i in range(0,int(len(peee))):
    print(peee[i] )
it=0
bill=0
while True:
    print("===========================================================================================")
    print("1. CUSTOMER")
    print("2. ADMIN")
    print("3. EXIT")
    loggin=int(input('enter the choice:'))
    if loggin==1:
        while True:
            print("===========================================================================================")
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
            print("product name :",dt1[1])
            print("cost per product:",dt1[2])
            print("stock available:",dt1[3])
            print(" Number items purchased :",dt1[4])
        elif ch==2:
            for i in range(0,int(len(peee))):
                print(peee[i] )
            prdno=input("Enter the product number of the product for which the stock is going to be updated:")
            upd_value=int(input("enter the number of new stocks came:"))
            c1.execute("update stock set stock=stock+" + str(upd_value) + " where product_no="+prdno)
            conn.commit()
        elif ch==3:
            pno1=input('Enter the product number of new product:')
            pna=input('Enter the product name of the new product:')
            cst=input('Enter the cost of the product:')
            stock12=input('Enter the number of stocks of the new product arrived:')
            pch='0'
            c1.execute("insert into stock values(" + pno1 +','+'"'+pna+'"'+','+cst+','+stock12+','+pch+')')
            print("Added sucessfully!!!!!!!")
            conn.commit()
        else:
            print('####INVALID OPTION ####')
    elif loggin== 3:
        print("...QUITING... ")
        break 
    else:
        print("###INVALID OPTION####")
