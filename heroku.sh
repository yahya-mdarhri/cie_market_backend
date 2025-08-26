docker build --platform=linux/amd64 -t registry.heroku.com/backendciemarketplace/web . --provenance=false
docker push registry.heroku.com/backendciemarketplace/web
heroku container:release web --app backendciemarketplace
heroku open --app backendciemarketplace

