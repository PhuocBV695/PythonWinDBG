import subprocess
def recvuntil(process, marker):
    data = b''
    while marker not in data:
        line = process.stdout.readline()
        if not line:
            break
        data += line
        #print(line, end='')  
    #print('xong')
    return data

def start(process):
    (recvuntil(process, b'Executable search path is:'))
    aa=(process.stdout.readline())
    (aa)
    startpoint=(int(aa.split()[1].replace(b'`', b''),16))#startpoint
    (recvuntil(process,b'int     3'))
    return startpoint
def break_point(bp,startpoint,process):
    try:
        #bp=0x2437#nhap breakpoint
        bp=hex(bp+startpoint).encode()#breakpoint+startpoint
        
        (process.stdout.read(7))#day la 0:000> 
        nhap=b"bp "+bp
        (nhap)
        process.stdin.write(nhap + b'\n')
        process.stdin.flush()
        return bp
    except:
        print("Dat breakpoint khong thanh cong")
        return False
    


def run(nhap,bp,process):
    (process.stdout.read(7))
    g=b'g'
    (nhap)
    process.stdin.write(g+b'\n')
    process.stdin.flush()
    #nhap=b'abcd'#nhap input o day
    process.stdin.write(nhap + b'\n')
    process.stdin.flush()
    (recvuntil(process, bp[-8:]))#
    return True

def getregval(thanhghi,process):
    (process.stdout.read(7))
    nhap=b'r '+thanhghi
    (nhap)
    process.stdin.write(nhap + b'\n')
    process.stdin.flush()
    aa=(process.stdout.readline())
    (aa)
    return aa[4:-1]

def getaddrval(kieudulieu, address, soluong,process):#new - bug fixxed
    soluong=str(soluong).encode()
    (process.stdout.read(7))
    nhap=kieudulieu+b' '+address+ b' L'+soluong
    (nhap)
    process.stdin.write(nhap + b'\n')
    process.stdin.flush()
    #aa=b''
    bb=[]
    n=int(soluong)
    for i in range(int(soluong)//16+1):
        aa=(process.stdout.readline()[17:])
        aa=aa.replace(b'-', b' ')
        #print(aa)
        aa=aa.split()
        #print(aa)
        for i in range(16):
            try:
                bb.append(int(aa[i],16))
            except:
                break
            #n=n-16
    return bb[:n]
def process(file):
    try:
        process = subprocess.Popen(
            [
                'C:/Program Files (x86)/Windows Kits/10/Debuggers/x64/cdb.exe','-a',
                file
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
            #,text=True
            #,bufsize=1
            ,creationflags=subprocess.CREATE_NO_WINDOW  
        )
        return process
    except:
        print("Chi chay duoc file 64bit hoac can cai dat WinDBG")
        return 0
        
def count_ins(process):#thêm chế độ đếm số lệnh đã thực thi
    t=0
    while True:
        (process.stdout.read(7))#,end='')
        nhap=b'p'
        #print(nhap)
        process.stdin.write(nhap+b'\n')
        process.stdin.flush()
        #print(process.stdout.read(20))

        aa=((recvuntil(process, b'0000')))
        #print(aa)
        t=t+1
        if b'ret' in aa:
            #print('instructions= ',t)
            break
    return t
def go(process):
    (process.stdout.read(7))
    g=b'g'
    (g)
    process.stdin.write(g+b'\n')
    process.stdin.flush()
    #(process.stdout.read(350)
    (recvuntil(process, b'eax='))
    for i in range(4):
        (process.stdout.readline())
def lm(name,process):# lấy address đầu và cuối của file exe
    name=name.encode()
    name=(name.strip().replace(b'.exe',b'')).split(b'(')[0]
    (process.stdout.read(7))#,end='')
    nhap=b'lm m'+name
    (nhap)
    process.stdin.write(nhap+b'\n')
    process.stdin.flush()
    (process.stdout.readline())
    aa=process.stdout.readline()
    aa=aa.split()
    #print(aa)
    aa0=aa[0].replace(b'`',b'')
    aa1=aa[1].replace(b'`',b'')
    return aa0,aa1

def in_func(addr,process):#lấy tên hàm chứa address 
    (process.stdout.read(7))#,end='')
    nhap=b'uf '+addr
    print(nhap)
    process.stdin.write(nhap+b'\n')
    process.stdin.flush()    
    aa=recvuntil(process,b'ret')
    if aa[0]==10:
        aa=aa[1:]
    aa=aa.split(b'\n')[0]
    bb=b'sub_'+(aa.split(b'x')[1]).split()[0]
    return bb
def bc(process):
    (process.stdout.read(7))
    g=b'bc 0'
    (g)
    process.stdin.write(g+b'\n')
    process.stdin.flush()
    #(process.stdout.read(350)    
    return True
def help():
    return ('''
made by Bui Phuoc AT20 KMA

cach su dung cac ham trong lib:

process(<file>=str) -> tao process va return process

start(<process>) -> return startpoint

break_point(<address>=int,<startpoint>=int,<process>) -> set breakpoint va return process breakpoint 

run(<input>=bytes,<process breakpoint>=bytes/None,<process>) -> day vao input va run den breakpoint

getregval(<register>=bytes,<process>) ->return gia tri tai thanh ghi

getaddrval(<kieudulieu>=bytes,<diachi>=str,<soluong>=int,<process>) ->lay n gia tri tu dia chi(kieu db/dw/dd/dq)

lm(<tên file>=str,<process>) -> lấy vùng address đầu và cuối của file

in_func(<địa chỉ>=bytes,<process>) -> lấy tên hàm chứa địa chỉ đó
''')
