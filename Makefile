
PROJECT_NAME = cie-backend
JENKINS_IMAGE = jenkins_server
JENKINS_CONTAINER = jenkins_server
BACKEND_IMAGE = backend_img
BACKEND_CONTAINER = cie-backend
BACKEND_DOCKERFILE = dockerfile
JENKINS_DOCKERFILE = jenkins_service/dockerfile


.PHONY: help
help:
	@echo "Usage:"
	@echo "  make backend        - Build and run the Django backend"
	@echo "  make jenkins        - Build and run the Jenkins service"
	@echo "  make stop           - Stop all running containers"
	@echo "  make clean          - Remove all containers and images"

.PHONY: backend
backend:
	docker build -t $(BACKEND_IMAGE) -f $(BACKEND_DOCKERFILE) .
	docker run -d --name $(BACKEND_CONTAINER) -p 8000:8000 $(BACKEND_IMAGE)

.PHONY: jenkins
jenkins:
	docker build -t $(JENKINS_IMAGE) -f $(JENKINS_DOCKERFILE) jenkins_service
	docker run -d --name $(JENKINS_CONTAINER) -p 8080:8080 -p 50000:50000 $(JENKINS_IMAGE)

.PHONY: stop
stop:
	-docker stop $(BACKEND_CONTAINER) $(JENKINS_CONTAINER)
	-docker rm $(BACKEND_CONTAINER) $(JENKINS_CONTAINER)

.PHONY: clean
clean: stop
	-docker rmi $(BACKEND_IMAGE) $(JENKINS_IMAGE)

