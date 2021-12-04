# EvilRedirect
Automation redirect detector tool

## Installation
```
git clone https://github.com/Aseel577/EvilRedirect.git
cd EvilRedirect
```
## Usage & Example
![alt text](Image%26Gifs/options.png)
##### Attacking single host:
```
python3 EvilRedirect.py --host 127.0.0.1?redirect=FUZZ
```
![alt text](Image%26Gifs/single_host.png)

#### Attacking multiple host:
First lets creat a file that has multiple hosts for example:
```
cat hosts.txt
http://127.0.0.1?redirect=FUZZ
http://myfakesite.com/redirect.php?redirect=FUZZ
```
```
python3 EvilRedirect.py -f hosts.txt
```
![alt text](Image%26Gifs/multiple_host.png)
