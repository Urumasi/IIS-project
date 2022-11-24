eval $(ssh-agent -s)
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "$1" | tr -d '\r' > ~/.ssh/action_key
chmod 700 ~/.ssh/action_key
ssh-keyscan -p2200 urumasi.xyz >> ~/.ssh/known_hosts
chmod 644 ~/.ssh/known_hosts
ssh -i ~/.ssh/action_key -p2200 iis@urumasi.xyz "cd /var/www/iis.urumasi.xyz/ && git stash && git checkout master && git pull origin master && git stash pop"
ssh -i ~/.ssh/action_key -p2200 root@urumasi.xyz "systemctl restart gunicorn-iis"
