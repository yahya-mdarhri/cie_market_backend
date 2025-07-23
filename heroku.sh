docker build --platform=linux/amd64 -t registry.heroku.com/backendciemarket/web . --provenance=false
docker push registry.heroku.com/backendciemarket/web
heroku container:release web --app backendciemarket
heroku open --app backendciemarket

