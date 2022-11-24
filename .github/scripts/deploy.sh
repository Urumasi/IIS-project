eval $(ssh-agent -s)
echo "$1" | tr -d '\r' | ssh-add -
mkdir -p ~/.ssh
chmod 700 ~/.ssh
ssh-keyscan -p2200 urumasi.xyz >> ~/.ssh/known_hosts
chmod 644 ~/.ssh/known_hosts
ssh -p2200 iis@urumasi.xyz "cd /var/www/iis.urumasi.xyz/ && git stash && git checkout master && git pull origin master && git stash pop"
ssh -p2200 root@urumasi.xyz "systemctl restart gunicorn-iis"
