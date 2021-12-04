import requests
import argparse
from time import sleep
from ascci import ascc

redirectCode = ["301", "302", "303", "307", "308"]
parser = argparse.ArgumentParser(description="Redirection check")
parser.add_argument("--host", type=str, help="Insert victim host")
parser.add_argument("-p", "--payload", metavar='', help="Set payload list file", default=False)
parser.add_argument("-pr", "--parameter", metavar='', help="Insert file that contain common parameter,"
                                                           " for common parameter [-pr default]", default=False)
parser.add_argument("-T", "--time", type=int, metavar='', help="Time delay between each request (default is 3 [-T 3])"
                                                               " bigger is faster, maximum is 5", default=3)
parser.add_argument("-v", "--verbose", action='store_true', help="Set to verbose mode")
parser.add_argument("-f", "--file", help="Insert file that contain list of hosts. (Must contain FUZZ in suspicious parameter)")
args = parser.parse_args()
host = args.host
time = args.time
if time == 5:
    second = 0.1
elif time == 4:
    second = 0.2
elif time == 2:
    second = 0.4
elif time == 1:
    second = 0.5
else:
    second = 0.3

try:
    if host[-1] == "/":
        host = host[:-1]
    if "http" not in host:
        print("Please type a valid host!!")
        exit()
except TypeError:
    pass

def prRed(skk):
    print("\033[91m {}\033[00m" .format(skk)) # This function will print red color

def prGreen(skk):
    print("\033[92m {}\033[00m" .format(skk)) # This function will print green color

prGreen(ascc[0])

def suspect_or_not():
    if args.verbose:
        pass
    else:
        prRed(f"\n[Suspicious Redirect]\n")

if args.payload:
    with open(f"{args.payload}", "r", encoding='utf-8') as payload_file:
        payloads = [p.rstrip() for p in payload_file]
else:
    with open("payload_files/payloads.txt", "r", encoding='utf-8') as payload_file:
        payloads = [p.rstrip() for p in payload_file]

def fuzzing(host):
    suspect_or_not()
    # host_filter(host)
    for payload in payloads:
        fuzz_par = host.replace('FUZZ', payload)
        response = requests.get(f"{fuzz_par}", allow_redirects=False)
        if str(response.status_code) in redirectCode:
            prRed(f"{fuzz_par} [{response.status_code}]")
            sleep(second)
        else:
            if args.verbose:
                prGreen(f"The {fuzz_par} is not vulnerable")
                sleep(second)

if args.parameter:
    suspect_or_not()
    if args.parameter == "default":
        with open("payload_files/parameter.txt", "r") as parameter_list:
            parameters = [parm.rstrip() for parm in parameter_list]
    elif args.parameter:
        with open(f"{args.parameter}", "r", encoding='utf-8') as parameter_list:
            parameters = [parm.rstrip() for parm in parameter_list]

    for parameter in parameters:
        for payload in payloads:
            response = requests.get(f"{host}?{parameter}={payload}", allow_redirects=False)
            if str(response.status_code) in redirectCode:
                prRed(f"{host}?{parameter}={payload} [{response.status_code}]")
                sleep(second)
            else:
                if args.verbose:
                    prGreen(f"The {host}?{parameter}={payload} is not vulnerable")
                    sleep(second)
elif host:
    if "FUZZ" in host:
        fuzzing(host)
    else:
        parser.print_help()
elif args.file:
    with open(f"{args.file}", "r", encoding='utf-8') as file_hosts:
        hosts = [fh.rstrip() for fh in file_hosts]
    for h in hosts:
        if "FUZZ" in h:
            fuzzing(h)
        else:
            parser.print_help()
else:
    parser.print_help()
