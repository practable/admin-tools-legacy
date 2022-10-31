# SSL

For the case where your domain registry / DNS are not supported by automatic SSL updates, then manual updates are needed.

## Practable v0.2.x

There are four separate instances that server the practable v0.2.x system, that each need a new wildcard certificate (`relay`,`static`,`book`, `shell`), and one that needs a non-wildcard (the blog site at the root domain). You can check and update the certificates using let's encrypts certbot (or whatever you use to manage your certificates manually). It's even better to have an automatic update but some domain registries such as namecheap are not supported by the certbot for wildcard ssl at this time.

### Checking your SSL certificate expiration dates

You can check the dates on the servers using openssl

```
echo  | openssl s_client -servername relay.practable.io -connect relay.practable.io:443 | openssl x509 -noout -dates
echo  | openssl s_client -servername static.practable.io -connect static.practable.io:443 | openssl x509 -noout -dates
echo  | openssl s_client -servername shell.practable.io -connect shell.practable.io:443 | openssl x509 -noout -dates
echo  | openssl s_client -servername book.practable.io -connect book.practable.io:443 | openssl x509 -noout -dates
echo  | openssl s_client -servername practable.io -connect practable.io:443 | openssl x509 -noout -dates
```

### Update your SSL certificates

Typically you will need an authentication certificate in `pem` format to log into your servers (this is not what we are updating, just what we use to log in to the servers)

```
export admin_cert=~/practable-realm.pem
```


#### relay.practable.io

```
ssh -i $admin_cert ubuntu@relay.practable.io
sudo certbot certonly --manual -d '*.practable.io'
```
Follow the instructions for the challenge. For namecheap, go to manage domains, Advanced DNS tab. A 1min TTL helps refresh rates on future cert updates.

Once the certificate has been updated, restart `nginx` so that it is using the new certificate (else it continues to use the old one)
```
sudo nginx -t
sudo systemctl restart nginx
echo  | openssl s_client -servername relay.practable.io -connect relay.practable.io:443 | openssl x509 -noout -dates
```

Since we know where the cert is saved
```
Certificate is saved at: /etc/letsencrypt/live/practable.io/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/practable.io/privkey.pem
```
We can copy the cert to the other two wildcard servers, rather than going through the verification process again

```
ansible-playbook download-ssl-cert-key-from-session-relay.yml
```

#### book.practable.io, shell.practable.io, static.practable.io

```
ansible-playbook upload-ssl-cert-key-to-book.yml
ansible-playbook upload-ssl-cert-key-to-shell.yml
ansible-playbook upload-ssl-cert-key-to-static.yml
```

#### practable.io

The blog is hosted at the root domain, using a non-wildcard cert, so we update manually, rather than copying the wildcard cert.

```
ssh -i $admin_cert ubuntu@practable.io
sudo certbot certonly --manual -d 'practable.io'
```
Then log in again from another terminal (keeping certbot one alive), so you can make the file for the authentication

```
ssh -i $admin_cert ubuntu@practable.io
cd /usr/share/nginx/practable.io/.well-known/acme-challenge/
sudo nano <filename> # edit contents to contain the challenge secret
```
Then go back to the original terminal running certbot, press Enter to verify.
```
sudo nginx -t
sudo systemctl restart nginx
```
Note - you can use `tmux` here if you like to avoid opening two separate connections.

### check the dates again

You should now see dates three months into the future, e.g.

```
$ ./check-dates
practable.io        Jan 29 11:04:33 2023 GMT
book.practable.io   Jan 29 09:49:00 2023 GMT
relay.practable.io  Jan 29 09:49:00 2023 GMT
shell.practable.io  Jan 29 09:49:00 2023 GMT
static.practable.io Jan 29 09:49:00 2023 GMT
```

 
