
install:
	pip install -r requirements.txt

test:
	@printf "Starting tests \n"
	pytest tests/test_*.py
	@printf "\n Finished tests \n"

build:
	@printf "Creating image"
	docker image build -f Dockerfile -t "chess" .

start:
	@printf "Starting service"
	python index.py

stop-container:
	@printf "Stopping service"
	docker-compose -f docker-compose.yml stop