git init
git add .
git commit -m "Initial commit"

gh repo create <repo-name> --public --source=. --remote=origin --push
