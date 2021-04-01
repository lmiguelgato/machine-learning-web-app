down:
	docker-compose rm -f

start:
	docker-compose -f docker-compose.yml up

build:
	docker build -t app_api -f docker/api/Dockerfile .
	docker build -t celery_worker -f docker/celery/Dockerfile .

run: down build start
