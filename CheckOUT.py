#!/usr/bin/env python
# http://stackoverflow.com/questions/2957116/make-2-functions-run-at-the-same-time
VERSION="v2.3"
BUILD=13
appver=13
APPID="ictman1076/checkout"
"""
def checkUpdate(urlaa):
    exit=False
    print("Checking for updates..."),
    try:
        data=json.loads(url.urlopen(urlaa).read())['v1']
        update=data['updatedata']
        if update['ver']!=appver:
            print("Update found!")
            print(data['appdata']['name']+" version "+update['vername']+" is available NOW!\n\nHere are the update notes:")
            print(update['notes'])
            if raw_input("Update now (y/N)? ")=="y":
                urla = update['updateurl']

                file_name = urla.split('/')[-1]
                u = url.urlopen(urla)
                f = open(file_name, 'wb')
                meta = u.info()
                file_size = int(meta.getheaders("Content-Length")[0])
                fszkb=file_size/1024
                print "Downloading: %s File size: %s KB" % (file_name, fszkb)

                file_size_dl = 0
                block_sz = 8192
                while True:
                    buffer = u.read(block_sz)
                    if not buffer:
                        break

                    file_size_dl += len(buffer)
                    f.write(buffer)
                    status = r"%10d KB [%3.2f%%]" % (file_size_dl/1024, file_size_dl * 100. / file_size)
                    status = status + chr(8)*(len(status)+1)
                    print status,

                f.close()
                os.startfile(file_name)
                print("\n\nWe've started the installer. Just go through the steps to install the app.")
                print("Then, restart "+data['appdata']['name']+" and enjoy!")
                t.sleep(5)
                exit=True
            else:print("No worries! We'll remind you next time. :)");t.sleep(1)
        else:print("All up to date!")
    except:print("Failed. Are you connected to the internet?")
    if exit:exit()
"""
print("CheckOUT "+VERSION+" by ICTman1076")
print("\n(c) Sorcerertech 2018. All rights reserved.")
print("Loading modules..."),
import os
import urllib, json
import urllib2 as url
import time as t
from datetime import datetime
print("OK")
def isValid(filepath,requiredtext):
    toret=True
    if os.path.exists(filepath):
        f=open(filepath,"r")
        if f.read()==requiredtext:
            toret=True
            print("Dev mode active")
        else:
            toret=False
        f.close()
    return toret
dev=isValid("devmode.txt","enable developer mode")
ev3addon=isValid("ev3.checkoutaddon","ev3dev")
if ev3addon:
    import ev3dev.ev3 as ev3
    import termios,tty,sys
def ev3do(dowhat):
    if ev3addon:
        eval("ev3."+dowhat)
def ev3led(lr,color):
    ev3do("Leds.set_color(ev3.Leds."+lr.upper()+", ev3.Leds."+color.upper()+")")

def getch():
    fd=sys.stdin.fileno()
    old_settings=termios.tcgetaddr(fd)
    try:
        tty.setraw(fd)
        ch=sys.stdin.read(1)
    finally:
        termios.tcsetaddr(fd,termios.TCSADRAIN, old_settings)
    return ch
def einput(prompt):
    if True:
	print(prompt)
        ch=""
        toret=""
        while ch!="\n":
            toret=toret+ch
            ch=getch()
        return toret
    else:
        return raw_input(prompt)
ev3do("Leds.all_off()")

for i in ['5','4','3','2','1']:
    t.sleep(1)
    print(i+"...")
t.sleep(1)
def cls():
    for i in range(50):
        print("\n")
    print("         -= CheckOUT =-         ")
    print("By Sorcerertech - http://stch.tk")

def input2(prompt):
    ev3led("right","green")
    a=raw_input(prompt.upper()+" >>> ").lower()
    ev3led("right","amber")
    if a=="help":
        print("Area        | Command              | Description")
        print("HOME        | new item/ni          | Start the new item wizard")
        print("HOME        | delete item/del i    | Delete an item")
        print("HOME        | delete voucher/del v | Delete an item")
        print("HOME        | new voucher/nv       | Start the new voucher wizard")
        print("HOME        | new transaction/nt   | Start a new transaction")
        print("HOME        | exit                 | Close CheckOUT")
        print("HOME        | refund               | Start the refund wizard")
        print("HOME        | earnings/earn        | See this session's total earnings")
        print("TRANSACTION | add item/ai          | Add a new item to the transaction")
        print("TRANSACTION | add voucher/av       | Add a voucher to the transaction")
        print("TRANSACTION | cancel               | Cancel the transaction")
        print("TRANSACTION | finish/ff            | Finish the transaction")
        raw_input("Press [ENTER] to continue...")
        return False
    else:
        if dev:
            if a=="appdat":
                print("Version: "+VERSION)
                print("Build: "+str(BUILD))
                print("AppID: "+APPID)
                raw_input("Press [ENTER] to continue...")
        return a
earnings=0.0
while True:
    cls()
    #ev3do("Leds.set(ev3.Leds.RIGHT, brightness_pct=0.5, trigger='timer')")
    #ev3do("Leds.set(ev3.Leds.RIGHT, delay_on=3000, delay_off=500)")
    ev3do("Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)")
    cmd=input2("home")
    
    if cmd=="new item" or cmd=="ni":
        with open(raw_input("Type in the barcode: ")+".checkoutitem","w") as f:
            f.write(raw_input("Type in the item name: ")+"\n"+raw_input("Type in the price: "))
        print("Done!")
        t.sleep(1)
    elif cmd=="new voucher" or cmd=="nv":
        with open(raw_input("Type in the code: ")+".checkoutvoucher","w") as f:
            f.write(raw_input("Type in the voucher name: ")+"\n"+raw_input("Type in the discount: -"))
        print("Done!")
        t.sleep(1)
    elif cmd=="new transaction" or cmd=="nt":
        print("Loading...")
        if cmd!="nt":
            print("Did you know you can use \"nt\" to quickly access a new transaction?")
            t.sleep(1)
        items=[]
        prices=[]
        total=0
        vouchertotal=0
        transaction=True
        datestr=datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        filename=datestr+" transaction log.txt"
        log="Sorcerertech CheckOUT\nhttp://sorcerertech.pcriot.com\n\nName                          | Price\n"
        while transaction:
            cls()
            print("Name                          | Price")
            for i in range(len(items)):
                ii=i-1
                z=items[ii]
                whitespace=""
                for i in range(30-len(z)):
                    whitespace=whitespace+" "
                print(z+whitespace+"| "+str(prices[ii]))
            print("TOTAL                         | "+str(total)) 
            cmd2=input2("Transaction")
            if cmd2=="add item" or cmd2=="ai":
                filep=raw_input("Type in the barcode: ")+".checkoutitem"
                if os.path.exists(filep):
                    with open(filep,"r") as f:
                        itemdat=f.read()
                    dat=itemdat.split("\n")
                    print("Item name: "+dat[0])
                    q=input('Quantity ("0" to cancel): ')
                    if q!=0:
                        items.append(dat[0]+" x "+str(q))
                        prices.append(float(dat[1])*q)
                        total=total+float(dat[1])*q
                        whitespace=""
                        for i in range(30-len(dat[0]+" x "+str(q))):
                            whitespace=whitespace+" "
                        log=log+dat[0]+" x "+str(q)+whitespace+"| "+str(float(dat[1])*q)
                        log=log+"\n"
                else:
                    ev3led("right","red")
                    raw_input("Unknown item code! Have you made a typo?\nPress [ENTER] to continue...")
            if cmd2=="add voucher" or cmd2=="av":
                print("Make sure the customer meets the requirements of the Terms and Conditions!")
                filep=raw_input("Type in the code: ")+".checkoutvoucher"
                if os.path.exists(filep):
                    with open(filep,"r") as f:
                        itemdat=f.read()
                    dat=itemdat.split("\n")
                    items.append("Voucher: "+dat[0])
                    total=total-float(dat[1])
                    prices.append("-"+dat[1])
                    whitespace=""
                    for i in range(30-len("Voucher: "+dat[0])):
                        whitespace=whitespace+" "
                    log=log+"Voucher: "+dat[0]+whitespace+"| "+str("-"+dat[1])
                    log=log+"\n"
                else:
                    ev3led("right","red")
                    raw_input("Unknown voucher code! Have you made a typo?\nPress [ENTER] to continue...")
            if cmd2=="cancel":
                ev3led("right","red")
                ev3led("left","red")
                if raw_input("Cancel (y/N)? ").lower()=="y":
                    transaction=False
                ev3do("Leds.all_off()")
            if cmd2=="finish" or cmd2=="ff":
                cls()
                print("\nTOTAL: "+str(total))
                print("Logged date/time: "+datestr)
                cash=input("How much money did the customer give you (0 to cancel)? ")
                if cash!=0 and cash>=total:
                    print("Return "+str(cash-total)+" to the customer.")
                    log=log+"TOTAL                         | "+str(total)
                    with open(filename,"w") as f:
                        f.write(log)
                    transaction=False
                    earnings=earnings+total
                    raw_input("Press [ENTER] to continue.")
                elif cash<total:
                    ev3led("right","red")
                    ev3led("left","amber")
                    raw_input("Not enough money - "+str(total-cash)+" more needed. Press [ENTER] to go back.")
                    ev3do("Leds.all_off()")
    elif cmd=="exit":
        print("You have earned "+str(earnings)+" today!")
        if raw_input("Close CheckOUT (y/N)? ").lower()=="y":
            print("Bye bye!")
            t.sleep(1)
            exit()
    elif cmd=="earnings" or cmd=="earn":
        print("You have earned "+str(earnings)+" today!")
        raw_input("Press [ENTER] to finish...")
    elif cmd=="delete item" or cmd=="del i":
        filee=raw_input("Enter item code you want to remove: ")+".checkoutitem"
        with open(filee,"r") as f:
            itemdat=f.read()
        dat=itemdat.split("\n")
        if raw_input("Delete item "+dat[0]+" (y/N)? ").lower()=="y":
            os.remove(filee)
            print("Deleted.")
        t.sleep(1)
    elif cmd=="delete voucher" or cmd=="del v":
        filee=raw_input("Enter voucher code you want to remove: ")+".checkoutvoucher"
        with open(filee,"r") as f:
            itemdat=f.read()
        dat=itemdat.split("\n")
        if raw_input("Delete voucher "+dat[0]+" (y/N)? ").lower()=="y":
            os.remove(filee)
            print("Deleted.")
        t.sleep(1)
    elif cmd=="refund":
        filee=raw_input("Enter item code: ")+".checkoutitem"
        with open(filee,"r") as f:
            itemdat=f.read()
        dat=itemdat.split("\n")
        q=input("Quantity of "+dat[0]+" worth "+str(dat[1])+" to refund (\"0\" to cancel)? ")
        if q!=0:
            earnings=earnings-(float(dat[1])*q)
            with open("_refund log.txt","a") as f:
                f.write(str(q)+' x "'+dat[0]+'" Refunded for '+str(float(dat[1])*q)+", Time: "+datetime.now().strftime('%Y-%m-%d %H-%M-%S')+"\n")
            print("Return "+str(float(dat[1])*q)+" to the customer. The refund has been logged.")
            raw_input("Press [ENTER] to continue")
            

