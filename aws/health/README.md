# Health

## Disk usage

Servers can use up the disk space in a number of ways, including image dumps from amazon, logs and so forth.

One symptom is an error message when attempting to run a command, such as updating an ssl certificate

```
sudo certbot certonly --manual -d 'practable.io'
Traceback (most recent call last):
  File "/snap/certbot/2618/bin/certbot", line 8, in <module>
    sys.exit(main())
  File "/snap/certbot/2618/lib/python3.8/site-packages/certbot/main.py", line 19, in main
    return internal_main.main(cli_args)
  File "/snap/certbot/2618/lib/python3.8/site-packages/certbot/_internal/main.py", line 1700, in main
    log.pre_arg_parse_setup()
  File "/snap/certbot/2618/lib/python3.8/site-packages/certbot/_internal/log.py", line 71, in pre_arg_parse_setup
    temp_handler = TempHandler()
  File "/snap/certbot/2618/lib/python3.8/site-packages/certbot/_internal/log.py", line 267, in __init__
    self._workdir = tempfile.mkdtemp(prefix="certbot-log-")
  File "/snap/certbot/2618/usr/lib/python3.8/tempfile.py", line 486, in mkdtemp
    prefix, suffix, dir, output_type = _sanitize_params(prefix, suffix, dir)
  File "/snap/certbot/2618/usr/lib/python3.8/tempfile.py", line 256, in _sanitize_params
    dir = gettempdir()
  File "/snap/certbot/2618/usr/lib/python3.8/tempfile.py", line 425, in gettempdir
    tempdir = _get_default_tempdir()
  File "/snap/certbot/2618/usr/lib/python3.8/tempfile.py", line 357, in _get_default_tempdir
    raise FileNotFoundError(_errno.ENOENT,
FileNotFoundError: [Errno 2] No usable temporary directory found in ['/tmp', '/var/tmp', '/usr/tmp', '/home/ubuntu']
```

First step is to [identify which locations are using most disk](https://askubuntu.com/questions/266825/what-do-i-do-when-my-root-filesystem-is-full) using this command

```
sudo du -hsx /* | sort -rh | head -n 40
```

An example for a full disk is:

```
du: cannot access '/proc/2535453/task/2535453/fd/4': No such file or directory
du: cannot access '/proc/2535453/task/2535453/fdinfo/4': No such file or directory
du: cannot access '/proc/2535453/fd/3': No such file or directory
du: cannot access '/proc/2535453/fdinfo/3': No such file or directory
4.4G	/usr
2.8G	/var
229M	/home
228M	/boot
21M	/run
6.5M	/etc
92K	/root
72K	/tmp
44K	/snap
16K	/lost+found
4.0K	/srv
4.0K	/opt
4.0K	/mnt
4.0K	/media
0	/sys
0	/sbin
0	/proc
0	/libx32
0	/lib64
0	/lib32
0	/lib
0	/dev
0	/bin
```

Then run again in the folders with the largest usage, e.g. 
```
$ sudo du -hsx /usr/* | sort -rh | head -n 35
2.6G	/usr/share
924M	/usr/lib
583M	/usr/src
237M	/usr/bin
55M	/usr/sbin
17M	/usr/local
648K	/usr/libexec
112K	/usr/include
4.0K	/usr/libx32
4.0K	/usr/lib64
4.0K	/usr/lib32
4.0K	/usr/games
```

```
$ sudo du -hsx /usr/share/* | sort -rh | head -n 35
2.4G	/usr/share/nginx
34M	/usr/share/vim
28M	/usr/share/locale
28M	/usr/share/doc
20M	/usr/share/perl
18M	/usr/share/man
17M	/usr/share/i18n
7.0M	/usr/share/terminfo
5.9M	/usr/share/X11
5.7M	/usr/share/mime
4.9M	/usr/share/mysql
4.7M	/usr/share/zoneinfo
2.9M	/usr/share/bash-completion
2.8M	/usr/share/fonts
2.5M	/usr/share/grub
2.2M	/usr/share/consolefonts
2.1M	/usr/share/perl5
1.8M	/usr/share/groff
1.5M	/usr/share/xml
1.5M	/usr/share/iso-codes
1.5M	/usr/share/alsa
1.4M	/usr/share/fwupd
1.2M	/usr/share/misc
1.2M	/usr/share/info
668K	/usr/share/polkit-1
636K	/usr/share/lintian
584K	/usr/share/ufw
536K	/usr/share/sounds
528K	/usr/share/ca-certificates
500K	/usr/share/initramfs-tools
488K	/usr/share/zoneinfo-icu
460K	/usr/share/calendar
428K	/usr/share/dbus-1
384K	/usr/share/bug
372K	/usr/share/apport
```

```
$ sudo du -hsx /usr/share/nginx/* | sort -rh | head -n 35
2.2G	/usr/share/nginx/pdf.gradex.io
140M	/usr/share/nginx/practable.io
58M	/usr/share/nginx/wordpress.generic
20K	/usr/share/nginx/modules-available
8.0K	/usr/share/nginx/html
0	/usr/share/nginx/modules
```

```
$ sudo du -hsx /usr/share/nginx/pdf.gradex.io/* | sort -rh | head -n 35
2.2G	/usr/share/nginx/pdf.gradex.io/wp-content
40M	/usr/share/nginx/pdf.gradex.io/wp-includes
9.6M	/usr/share/nginx/pdf.gradex.io/wp-admin
48K	/usr/share/nginx/pdf.gradex.io/wp-login.php
32K	/usr/share/nginx/pdf.gradex.io/wp-signup.php
24K	/usr/share/nginx/pdf.gradex.io/wp-settings.php
20K	/usr/share/nginx/pdf.gradex.io/license.txt
12K	/usr/share/nginx/pdf.gradex.io/wp-mail.php
8.0K	/usr/share/nginx/pdf.gradex.io/wp-trackback.php
8.0K	/usr/share/nginx/pdf.gradex.io/wp-activate.php
8.0K	/usr/share/nginx/pdf.gradex.io/readme.html
4.0K	/usr/share/nginx/pdf.gradex.io/xmlrpc.php
4.0K	/usr/share/nginx/pdf.gradex.io/wp-load.php
4.0K	/usr/share/nginx/pdf.gradex.io/wp-links-opml.php
4.0K	/usr/share/nginx/pdf.gradex.io/wp-cron.php
4.0K	/usr/share/nginx/pdf.gradex.io/wp-config.php
4.0K	/usr/share/nginx/pdf.gradex.io/wp-config-sample.php
4.0K	/usr/share/nginx/pdf.gradex.io/wp-comments-post.php
4.0K	/usr/share/nginx/pdf.gradex.io/wp-blog-header.php
4.0K	/usr/share/nginx/pdf.gradex.io/index.php
```
```
$ sudo du -hsx /usr/share/nginx/pdf.gradex.io/wp-content/* | sort -rh | head -n 35
2.1G	/usr/share/nginx/pdf.gradex.io/wp-content/updraft
73M	/usr/share/nginx/pdf.gradex.io/wp-content/uploads
30M	/usr/share/nginx/pdf.gradex.io/wp-content/plugins
4.5M	/usr/share/nginx/pdf.gradex.io/wp-content/themes
3.1M	/usr/share/nginx/pdf.gradex.io/wp-content/languages
4.0K	/usr/share/nginx/pdf.gradex.io/wp-content/upgrade
4.0K	/usr/share/nginx/pdf.gradex.io/wp-content/index.php
```

Our backups have accummulated, so let's download and delete

```
# on admin machine, in some suitable dir
scp -i ~/practable-realm.pem 'ubuntu@practable.io:/usr/share/nginx/pdf.gradex.io/wp-content/updraft/backup_*' ./ 
```

```
on remote machine
cd /usr/share/nginx/pdf.gradex.io/wp-content/updraft
rm backup_*
```

Next we look in var, which has the most stuff in lib, so look there:

```
sudo du -hsx /var/lib/* | sort -rh | head -n 35
1.7G	/var/lib/snapd
171M	/var/lib/mysql
162M	/var/lib/apt
39M	/var/lib/dpkg
<snip>
```

```
1.1G	/var/lib/snapd/snaps
353M	/var/lib/snapd/cache
252M	/var/lib/snapd/seed
896K	/var/lib/snapd/assertions
536K	/var/lib/snapd/apparmor
356K	/var/lib/snapd/seccomp
88K	/var/lib/snapd/state.json
40K	/var/lib/snapd/sequence
36K	/var/lib/snapd/cookie
20K	/var/lib/snapd/lib
20K	/var/lib/snapd/desktop
12K	/var/lib/snapd/device
12K	/var/lib/snapd/dbus-1
8.0K	/var/lib/snapd/ssl
8.0K	/var/lib/snapd/mount
4.0K	/var/lib/snapd/void
4.0K	/var/lib/snapd/system-params
4.0K	/var/lib/snapd/system-key
4.0K	/var/lib/snapd/inhibit
4.0K	/var/lib/snapd/hostfs
4.0K	/var/lib/snapd/firstboot
4.0K	/var/lib/snapd/features
4.0K	/var/lib/snapd/environment
4.0K	/var/lib/snapd/auto-import
0	/var/lib/snapd/state.lock
```

We could [clean](https://www.debugpoint.com/clean-up-snap/) this, but we'd have to stop some snaps, so we'd need to know what snaps were being used...

```
Name              Version        Rev    Tracking         Publisher     Notes
amazon-ssm-agent  3.1.1188.0     5656   latest/stable/…  aws✓          disabled,classic
amazon-ssm-agent  3.1.1732.0     6312   latest/stable/…  aws✓          classic
certbot           1.32.2         2618   latest/stable    certbot-eff✓  classic
certbot           1.32.1         2582   latest/stable    certbot-eff✓  disabled,classic
core              16-2.57.6      14399  latest/stable    canonical✓    core,disabled
core              16-2.58        14447  latest/stable    canonical✓    core
core18            20221212       2667   latest/stable    canonical✓    base
core18            20221205       2654   latest/stable    canonical✓    base,disabled
core20            20221123       1738   latest/stable    canonical✓    base,disabled
core20            20221212       1778   latest/stable    canonical✓    base
go                1.19.5         10030  latest/stable    mwhudson      classic
go                1.19.4         10008  latest/stable    mwhudson      disabled,classic
lxd               4.0.9-eb5e237  23991  4.0/stable/…     canonical✓    disabled
lxd               4.0.9-a29c6f1  24061  4.0/stable/…     canonical✓    -
snapd             2.58           17950  latest/stable    canonical✓    snapd
snapd             2.57.6         17883  latest/stable    canonical✓    snapd,disabled
```

Since the default is three revisions, it looks like we already issued this command in the past:
```
sudo snap set system refresh.retain=2
```

`clean_snap.sh`:
```
#!/bin/bash
 #Removes old revisions of snaps
 #CLOSE ALL SNAPS BEFORE RUNNING THIS
 set -eu
 LANG=en_US.UTF-8 snap list --all | awk '/disabled/{print $1, $3}' |
     while read snapname revision; do
         snap remove "$snapname" --revision="$revision"
     done
```


It's not obvious how to stop core, so let's bash on....
```
$ sudo ./clean_snap.sh 
amazon-ssm-agent (revision 5656) removed
certbot (revision 2582) removed
core (revision 14399) removed
core18 (revision 2654) removed
core20 (revision 1738) removed
go (revision 10008) removed
lxd (revision 23991) removed
snapd (revision 17883) removed
```
```
$ sudo du -hsx /var/lib/* | sort -rh | head -n 35
1.2G	/var/lib/snapd
171M	/var/lib/mysql
162M	/var/lib/apt
39M	/var/lib/dpkg
```

That's saved another 0.5GB. We're back to 70% usage. 

```
$ df
Filesystem     1K-blocks    Used Available Use% Mounted on
/dev/root        8065444 5605224   2443836  70% /
devtmpfs          989876       0    989876   0% /dev
tmpfs             996480       0    996480   0% /dev/shm
tmpfs             199296    3420    195876   2% /run
tmpfs               5120       0      5120   0% /run/lock
tmpfs             996480       0    996480   0% /sys/fs/cgroup
tmpfs             199296       0    199296   0% /run/user/1000
/dev/loop10        25088   25088         0 100% /snap/amazon-ssm-agent/6312
/dev/loop0         94080   94080         0 100% /snap/lxd/24061
/dev/loop2         45824   45824         0 100% /snap/certbot/2618
/dev/loop8         56960   56960         0 100% /snap/core18/2667
/dev/loop11        64896   64896         0 100% /snap/core20/1778
/dev/loop13        51072   51072         0 100% /snap/snapd/17950
/dev/loop15       119552  119552         0 100% /snap/core/14447
/dev/loop17       107776  107776         0 100% /snap/go/10030
```

We could consider increasing the size of this disk.
