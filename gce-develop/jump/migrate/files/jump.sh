cd sources
wget https://golang.org/dl/go1.20.1.linux-armv6l.tar.gz -O go.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> /etc/profile
source /etc/profile
if cd jump 2> /dev/null; then git pull origin main; else git clone https://github.com/practable/jump && cd jump; fi
( cd scripts/build; ./build.sh)
cd ../ #back to sources
cp jump/cmd/jump/jump /usr/local/bin
export FILES=https://assets.practable.io/84aa5631-7337-433e-bbf9-94f5feb26f0d/
wget $FILES/getid.sh -O getid.sh
chmod +x ./getid.sh
export PRACTABLE_ID=$(./getid.sh)
cd /etc/practable
wget $FILES/jump.env.$PRACTABLE_ID -O jump.env
cd /etc/systemd/system
wget $FILES/jump.service -O jump.service
systemctl enable jump.service
systemctl start jump.service
