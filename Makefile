down:
	docker-compose rm -f

start:
	docker-compose -f docker-compose.yml up

build:
	docker build -t app_api -f api/Dockerfile .
	docker build -t celery_worker -f celery/Dockerfile .

run: down build start
