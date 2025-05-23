git init
git add .
git commit -m "Initial commit"

gh repo create my-proxy-app --public --source=. --remote=origin --push
