git init
git add .
git commit -m "Initial commit"

git remote add origin https://github.com/aidensacharski/gradeschool.git
git branch -M main
git push -u origin main

pip install requests

sudo apt install cloudflared
cloudflared login
cloudflared tunnel create my-tunnel
tunnel: my-tunnel
credentials-file: /home/youruser/.cloudflared/my-tunnel.json

ingress:
  - hostname: sacharski.cc
    service: http://localhost:3000
  - service: http_status:404
cloudflared tunnel route dns my-tunnel sacharski.cc
cloudflared tunnel run my-tunnel
