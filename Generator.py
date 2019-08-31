import random, string, requests, threading, os, sys, time
from time import sleep
import os.path
from requests.exceptions import ProxyError, SSLError, ConnectionError, InvalidProxyURL

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print("8qBIT's Nitro Code Generator v1.8a\n")

print("Amount of workers to use at once?")
_THREADS = int(input("Threads: "))

os.environ["_THREADS"] = "0"
generation = 0
banned = 0
nitro_codes = 0
start_time = time.time()

def clearterminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def codeGenerator():
    codeLen = 16
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(letters) for i in range(codeLen))

proxies = [line.rstrip('\n') for line in open("proxy.txt")]
def getProxy():
    global proxies
    return random.choice(proxies)

def banProxy(pxy):
    global proxies, banned
    if proxies.__contains__(pxy):
        proxies.remove(pxy)
        banned = banned + 1
    else:
        pass

def saveCode(code):
    file = open("nitro_codes.txt","a")
    file.write(code + "\n")
    nitro_codes = nitro_codes + 1

def getRuntime():
    elapsed_time = time.time() - start_time
    return str(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

class masterThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.tasks = []
    def run(self):
        global generation, banned, nitro_codes
        raw_proxy = ""
        while True:
            try:
                current_code = codeGenerator()

                url = 'https://discordapp.com/api/v6/entitlements/gift-codes/' + current_code + '?with_application=false&with_subscription_plan=true'
                raw_proxy = getProxy()
                proxy = {'https': 'https://' + raw_proxy}

                s = requests.session()
                response = s.get(url, proxies=proxy)
                if 'subscription_plan' in response.text:
                    saveCode(current_code)
                elif 'Access denied' in response.text:
                    banProxy(raw_proxy)
                else:
                    generation = generation + 1
                    sleep(random.randrange(1,10))
            except ProxyError:
                pass
            except SSLError:
                banProxy(raw_proxy)
                pass
            except ConnectionError:
                banProxy(raw_proxy)
                pass
            except InvalidProxyURL:
                banProxy(raw_proxy)
                pass
            else:
                pass

class monitorThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.tasks = []
    def run(self):
        global generation, banned, nitro_codes, proxies
        while True:
            try:
                clearterminal()
                window = " <---------> GENERATOR MONITOR <--------->\n\n" + " Gen/s: " + bcolors.WARNING + str(generation) + bcolors.ENDC + " | Active Threads: " + bcolors.OKGREEN + os.environ["_THREADS"] + bcolors.ENDC + "\n Bad Proxies: " + bcolors.FAIL + str(banned) + bcolors.ENDC + " | Active Proxies: " + bcolors.OKGREEN + str(len(proxies)) + bcolors.ENDC + "\n Nitro Codes Found: " + bcolors.OKGREEN + str(nitro_codes) + bcolors.ENDC + " | Runtime: " + bcolors.OKBLUE + getRuntime() + bcolors.ENDC +"\n\n <--------------------------------------->"
                print(window)
                generation = 0
                sleep(1)
            except:
                pass

threads = []
for x in range(_THREADS):
    threads.append(masterThread())

for thread in threads:
    thread.daemon = True
    thread.start()
    thr = int(os.environ["_THREADS"])
    os.environ["_THREADS"] = str(thr + 1)

monitor = monitorThread()
monitor.daemon = True
monitor.start()

while True:
    try:
        sleep(1)
    except KeyboardInterrupt:
        print("\n Quitting...")
        exit(0)