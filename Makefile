APP_PORT := 5000
IMAGE_NAME := my-planet-app
CONTAINER_NAME := my-planet-container

DEPLOY_HOST := demo_host
DVC_REMOTE_NAME := alexander_vedernikov_remote
STAGING_USERNAME := a.vedernikov
KEY_FILE := ~/.ssh/id_rsa

install:
	@bash setup.sh

.PHONY: run_app
run_app:
	PYTHONPATH=. python3 -m uvicorn app:app --host='127.0.0.1' --port=$(APP_PORT)

.PHONY: build_image
build_image:
	docker build -t $(IMAGE_NAME) .

.PHONY: run_container
run_container:
	docker run -d -p $(APP_PORT):$(APP_PORT) --name $(CONTAINER_NAME) $(IMAGE_NAME)

.PHONY: stop_container
stop_container:
	docker stop $(CONTAINER_NAME) && docker rm $(CONTAINER_NAME)

.PHONY: lint
lint:
	PYTHONPATH=. flake8 .

.PHONY: run_unit_tests
run_unit_tests:
	PYTHONPATH=. pytest tests/unit/

.PHONY: run_integration_tests
run_integration_tests:
	PYTHONPATH=. pytest tests/integration/

.PHONY: run_all_tests
run_all_tests:
	make run_unit_tests
	make run_integration_tests

.PHONY: generate_coverage_report
generate_coverage_report:
	PYTHONPATH=. pytest --cov=src --cov-report html  tests/

.PHONY: install_dvc
install_dvc:
	pip install pygit2==1.10.1 pathspec==0.9.0
	pip install dvc[ssh]==2.5.4

.PHONY: pull_weights
pull_weights: configure_dvc_remote
	dvc pull -R weights

.PHONY: configure_dvc_remote
configure_dvc_remote:
	dvc remote add --default $(DVC_REMOTE_NAME) ssh://91.206.15.25/home/$(STAGING_USERNAME)/dvc_files || true
	dvc remote modify $(DVC_REMOTE_NAME) user $(STAGING_USERNAME)
	dvc remote modify $(DVC_REMOTE_NAME) keyfile $(KEY_FILE)
	dvc config cache.type hardlink,symlink

.PHONY: deploy
deploy:
	ansible-playbook -i deploy/ansible/inventory.ini deploy/ansible/deploy.yml \
		-e host=$(DEPLOY_HOST) \
		-e docker_image=$(IMAGE_NAME) \
		-e docker_tag=$(DOCKER_TAG) \
		-e docker_registry_user=$(CI_REGISTRY_USER) \
		-e docker_registry_password=$(CI_REGISTRY_PASSWORD) \
		-e docker_registry=$(CI_REGISTRY)

.PHONY: destroy
destroy:
	ansible-playbook -i deploy/ansible/inventory.ini deploy/ansible/destroy.yml \
		-e host=$(DEPLOY_HOST)
