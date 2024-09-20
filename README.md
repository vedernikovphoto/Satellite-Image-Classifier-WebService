# Planet Classification Web Service

This project provides a FastAPI-based web service that performs planet classification using a pre-trained computer vision model. The model is implemented with PyTorch and saved with TorchScript for efficient inference. The service offers an easy-to-use API for image classification tasks, enabling users to send images and receive predictions on planet classes.


## Installation

1. **Clone the repository:**
   ```sh
   git clone https://gitlab.deepschool.ru/cvr8/a.vedernikov/hw-01-service.git
   cd hw-01-service
   ```

2. **Install the required packages and set up the environment:**
   ```sh
   make install
   ```

3. **Setup Configuration**:
Ensure that the configuration file `config/config.yml` is correctly set up with the paths to your model weights and other necessary configurations.


## Model Versioning
We use DVC for model versioning. The model weights are stored in a private remote storage configured through DVC. If you have access to this storage, follow the steps below to retrieve the weights:

1. **Install DVC (if not already installed)**:
   Run the following command to install the required dependencies, including DVC:
   ```sh
   make install_dvc
   ```

2. **Configure DVC and pull the latest weights:** 
   Run the following command to configure the DVC remote and pull the latest model weights:
   ```bash
   make pull_weights USERNAME=<username> KEY_FILE=<path_to_private_key>
   ```

3. **Verify the downloaded files:** 
   After pulling the files, verify them using:
   ```bash
   ls weights
   ```

This process ensures that you have the necessary files in your local setup for inference or further training. For inference, place the downloaded file into the `weights` folder.

If you do not have access to the mentioned private remote storage, you can request the model weights by sending an email to [alexander.vedernikov.edu@gmail.com](mailto:alexander.vedernikov.edu@gmail.com). Once you receive the weights, place them in the `weights` directory.


## Running the Service

You can run the web service locally or using Docker. Below are the instructions for both methods:

### 1. Running FastAPI service Locally:
   ```sh
  make run_app
   ```

Once the service is running, you can access it at `http://127.0.0.1:5007`. The API documentation can be found at `http://127.0.0.1:5007/docs`.

### 2. Running with Docker:

- Build the Docker image:
   ```sh
   make build_image
   ```

- Run Docker Container:
   ```sh
   make run_container
   ```

  Once the container is running, you can visit `http://127.0.0.1:5007/docs` to explore the API documentation.

- Stop and Remove Docker Container:
   ```sh
   make stop_container
   ```


## Testing

This project includes both unit and integration tests to ensure the functionality of the web service and its components.

### Running Tests

1. **Run All Tests**:
   ```sh
   make run_all_tests
   ```

2. **Run Unit Tests Only**:
   ```sh
   make run_unit_tests
   ```

3. **Run Integration Tests Only**:
   ```sh
   make run_integration_tests
   ```

4. **Generate Coverage Report**:
   ```sh
   make generate_coverage_report
   ```

The report will be generated in an HTML format and can be viewed by opening the `htmlcov/index.html` file in your browser.

### Running Specific Tests
You can run specific test files or individual tests directly using pytest commands. For example, to run the integration tests for the API endpoints:

```sh
pytest tests/integration/test_planets_endpoints.py
```

## Linting
We use `wemake-python-styleguide` for linting to ensure code quality and maintain consistent style. The linter configurations are specified in the `setup.cfg` file.
   ```sh
   make lint
   ```


## Continuous Integration and Deployment (CI/CD)

This project uses GitLab CI/CD for automating the testing, building, and deployment process. The GitLab pipeline consists of the following stages:

1. **Prepare**: Model weights are pulled from the DVC remote storage using SSH authentication.

2. **Build**: The Docker image is built and pushed to the GitLab container registry.

3. **Lint**: Code quality is checked using `wemake-python-styleguide`.

4. **Tests**: Unit and integration tests are run inside a Docker container to ensure functionality.

5. **Deploy**: Ansible is used to deploy the service to a remote host. Deployment can be manually triggered when required.

To view the complete pipeline configuration, refer to the `.gitlab-ci.yml` file.


## Deployment Automation with Ansible

This project uses Ansible for automating deployment, container management, and cleanup tasks. The Ansible playbooks (`deploy.yml` and `destroy.yml`) are configured to:

1. **Deploy**: Pull the latest Docker image, stop and remove any existing containers, and run the service in a new container.
   ```sh
   make deploy
   ```

2. **Destroy**: Stop and remove the running container and clean up Docker images and containers.
   ```sh
   make destroy
   ```

The deployment process uses an inventory file (`inventory.ini`) to define the target host and environment variables, while the templates for automation scripts (e.g., `pull.sh`, `run.sh`, `clean.sh`, `destroy.sh`) ensure a streamlined process for managing the service lifecycle.
