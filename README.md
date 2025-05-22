# Lib  
```
!đã hỗ trợ PE file x86
  autodebug lấy giá trị thanh ghi tại 1 địa chỉ, giá trị n phần tử tại địa chỉ và các chức năng khác
```
## x64: 
```python
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
```
  
## x86(chưa hỗ trợ hoàn toàn)  
```python
import subprocess
def recvuntil(process, marker):
    data = b''
    while marker not in data:
        line = process.stdout.readline()
        if not line:
            break
        data += line
        #(line, end='')  
    #('xong')
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
        ("Dat breakpoint khong thanh cong")
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
    #(aa)
    return aa[4:-1]

def getaddrval(kieudulieu, address, soluong,process):
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
        aa=(process.stdout.readline()[9:])
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
                'C:/Program Files (x86)/Windows Kits/10/Debuggers/x86/cdb.exe','-a',
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
        ("Chi chay duoc file 32bit hoac can cai dat WinDBG")
        return 0
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
    #print(recvuntil(process, bp[-6:]))#
    #print(recvuntil(process, bp[-6:]))
    return True
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
    #(aa)
    aa0=aa[0].replace(b'`',b'')
    aa1=aa[1].replace(b'`',b'')
    return aa0,aa1

def in_func(addr,process):#lấy tên hàm chứa address 
    (process.stdout.read(7))#,end='')
    nhap=b'uf '+addr
    (nhap)
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
```
`print(help()) để đọc hướng dẫn`  

   
# Ví dụ sử dụng:  
## lấy giá trị tại thanh ghi/địa chỉ  
```python
from windbg_autodebug import*
proces=process('lmao3.exe')
startpoint=start(proces)
bp=break_point(0x2437,startpoint,proces)
run(b'abc',bp,proces)
rsi=getregval(b'rsi',proces)
data=getaddrval(b'db',rsi,3,proces)
print(data)
proces.terminate()
#[97, 98, 99]
```
## Bruteforce flag bằng cách đếm số lệnh đã thực thi  
bài `Just not a s1mple flag checker - 13r_ə_Rɪst` - KCSC Recruitment 2024):  
```python
from windbg_autodebug import*
brepoi=0x14b2
wordlists= b'''_{}0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'''
flag=''
maxx=20
length=53
for i in range(length):
    for sym in wordlists:
        print(chr(sym),end='')
        inputt=(flag+chr(sym)+(length-i-1)*'-').encode()
        proces=process('chall.exe')
        startpoint=start(proces)
        bp=break_point(brepoi,startpoint,proces)
        run(inputt,bp,proces)
        ins=count_ins(proces)
        proces.terminate()#đừng quên terminate process
        if ins>maxx:
            maxx=ins
            print(' ',maxx)
            flag=flag+chr(sym)
            print('flag=',flag)
            break
#flag= 3CSC{3V3rY_r3v3R53_En91n33r_kN0w_H0W_TH3_5t4ck_w0Rk3}
```  
**nhược điểm:**  
-tốn rất nhiều thời gian bruteforce (cần đặt breakpoint càng gần chỗ `cmp` càng tốt và có thể điều chỉnh wordlists hợp lý để rút ngắn thời gian bruteforce)  
-cần xử lý antidebug bằng cách patch trước khi đưa file vào bruteforce  
**ưu điểm:**  
-không cần phân tích đề, chỉ cần bỏ vào là ra flag  
-hữu dụng khi gặp mấy bài obfuscate/VM chỉ sử dụng mã hóa dòng, check hash,...  
-tương tác cấp assembly nên sử dụng được cho nhiều ngôn ngữ khác nhau  
## EzMath - KMACTF2024  
Bruteforce bằng cách đọc trực tiếp `v17` thay vì dựng lại script bằng python hay bruteforce chay bằng tay.  
![image](https://hackmd.io/_uploads/HkXX8RVxxg.png)  

```python
from windbg_autodebug import*
chuoi=b'-'
for dem in range(400//21):
    proces=process('Chall(1).exe')
    startpoint=start(proces)
    bp=break_point(0x2C19,startpoint,proces)
    run(b'S'+chuoi,bp,proces)
    ll=[]
    for i in range(dem+1):
        go(bp,proces)
        rdx=getregval(b'rdx',proces)
        rdx=int(rdx,16)

        ll.append(rdx)
    chuoi=b''.join(c.to_bytes(1, 'big') for c in ll)
    print(b'S'+chuoi)    
    proces.terminate()
#b'SUper_e3sy_Md4_CR3CJ'
```
output:  
```
b'SU'
b'SUo'
b'SUpd'
b'SUpeq'
b'SUper^'
b'SUper_d'
b'SUper_e3'
b'SUper_e3r'
b'SUper_e3sx'
b'SUper_e3sy^'
b'SUper_e3sy_L'
b'SUper_e3sy_Mc'
b'SUper_e3sy_Md4'
b'SUper_e3sy_Md4^'
b'SUper_e3sy_Md4_B'
b'SUper_e3sy_Md4_CQ'
b'SUper_e3sy_Md4_CR3'
b'SUper_e3sy_Md4_CR3B'
b'SUper_e3sy_Md4_CR3CJ'
```
Tuy nhiên flag chuẩn là `SUper_e4sy_Md5_CR4CK`  
## OldGame.exe (pwnablevn)  
auto dump toàn bộ shellcode đã bị mã hóa(đã được gọi):  
```python
from windbg_autodebug_x86 import*
import hashlib
import time
ops = ''
ha = []
proces = process('OldGame.exe')
startpoint = start(proces)
# print(startpoint)
bp = break_point(0x13B6, startpoint, proces)
# print(bp)

ecx = b'0000'
eax = b'0000'
listt = []
ops = ''

for i in range(32782 - 1):
    try:
        op = ''
        go(bp, proces)
        time.sleep(0.1)
        # ecx = getregval(b'ecx', proces)
        # print(ecx[-4:].decode(), end=' ')

        eax = getregval(b'eax', proces)

        op = ''
        ebx = getregval(b'ebx', proces)
        esi = getregval(b'esi', proces)
        addrr = hex(int(esi, 16) + int(ebx, 16) * 4 + 0x30).encode()
        addrr2 = str(hex(getaddrval(b'dd', addrr, 1, proces)[0])).encode()
        opcodes = getaddrval(b'db', addrr2, int(eax, 16), proces)

        for o in opcodes:
            op = op + hex(o)[2:].zfill(2) + ' '

        has = hashlib.md5(op.encode()).hexdigest()
        if has in ha:
            continue
        else:
            listt.append(eax)
            ha.append(has)
            print(f'{i}:', eax[-4:].decode(), end=' ')
            ops += op

    except:
        print('loi')
        break

proces.terminate()

with open('opcodesloo2.txt', "w") as f:
    f.write(ops)

```
có thể áp dụng nguyên lý trên để unpack các bài gọi shellcode  
tuy không phải là cách hay và đây chỉ là ý tưởng nảy ra nhưng hi vọng sẽ giúp ích được gì đấy  

## VM nezziRz  
Sử dụng debug động để extract opcode từ VM theo tuần tự 1 cách tự dộng  
```python
from windbg_autodebug_x86 import*
import numpy as np
ops = ''
ha = []
proces = process('chal.exe')
startpoint = start(proces)
b=break_point(0x16b8, startpoint, proces)
bp = break_point(0x15bf, startpoint, proces)
go(proces)
bc(proces)
b=break_point(0x1506, startpoint, proces)

ecx = b'0000'
eax = b'0000'
listt = []
ops = ''
i=1
y=''
flag=''
a=''
k=0
flag=''
for i in range(32//4):
    if k==0:
        l=19
        a=[7]
    else:
        l=20
        a=[]
    b=[]
    for i in range(l):
        k=k+1
        go(proces)
        eip = getregval(b'eip', proces)
        if eip[-4:]==b'15bf':
            edi = getregval(b'edi', proces)
            print(int(edi,16),end=' ')
            a.append(int(edi,16))
        if eip[-4:]==b'1506':
            ecx = getregval(b'ecx', proces)
            print(ecx[-4:],end=' ')
            b.append(int(ecx,16))
            eax = getregval(b'eax', proces)
            print(eax[-4:].decode()+' ')
        if i==l-1:
            a=np.array(a).reshape(-1, 4)
            print(a)
            b=np.array(b)
            print(b)
            c=(np.linalg.solve(a, b))
            print(c)
            c=''.join(chr(int(round(val))) for val in c)
            print(c)
            flag=flag+c
            
print(flag)      
proces.terminate()
#sh33r_d3d1c4ti0n_4lw4y5_p4ys_0ff
```
