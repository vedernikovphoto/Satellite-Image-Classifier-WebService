# Planet Classification Web Service

This repository contains the web service for predicting planet classes from images using a deep learning model.

## Project Overview

This project is a FastAPI-based web service that utilizes a trained deep learning model to classify planet images into multiple categories. The model is trained using PyTorch and TorchScript is used to save the model for inference.

## Getting Started

### Clone the Repository

```bash
git clone https://gitlab.deepschool.ru/cvr8/a.vedernikov/hw-01-service.git
cd hw-01-service
```

## Setup Environment

1. **Install Dependencies**:
To set up the environment and install the required packages, run the following command
```sh
make install
```

2. **Setup Configuration**:
Ensure that the configuration file `config/config.yml` is correctly set up with the paths to your model weights and other necessary configurations.

3. **Run Linters (Optional)**:
To check for code quality and style, use wemake-python-styleguide. The linter configurations are specified in the `setup.cfg` file. To run the linter use the following command:

```sh
make lint
```
This will apply the linting rules defined in `setup.cfg` to the entire project.


## Model Versioning
We use DVC for model versioning. The latest and best model can be found in the DVC storage. To download the latest model weights from the remote storage, follow these steps:

1. **Install DVC (if not already installed)**:
Run the following command to install the required dependencies, including DVC:
```bash
make install_dvc
```

2. **Configure DVC and Pull the Latest Weights**:
Run the following command to configure the DVC remote and pull the latest model weights:
```bash
make pull_weights USERNAME=your_username KEY_FILE=/path/to/your/key_rsa
```

3. **Verify the Downloaded Files**:
To verify that the weights have been downloaded correctly, run:
```bash
ls weights
```

This will download the necessary files to your local setup, making it ready for inference or further training. For the inference, place the downloaded file into the `weights` folder.


## Running the Service

1. **Locally**:
Run the FastAPI service locally:
```sh
make run_app
```
- Visit the service at `http://127.0.0.1:5000`.
- Explore the API documentation at `http://127.0.0.1:5000/docs`.


2. **Using Docker**:
You can also run the service inside a Docker container using the provided `Makefile` commands:

   - **Build Docker Image**:
     To build the Docker image, use the following command:
     ```sh
     make build_image
     ```

   - **Run Docker Container**:
     To run the service inside a Docker container:
     ```sh
     make run_container
     ```

   After running the container, visit `http://127.0.0.1:5000/docs` to explore the API documentation.

   - **Stop Docker Container**:
     To stop and remove the Docker container:
     ```sh
     make stop_container
     ```


## Testing

This project includes both unit and integration tests to ensure the functionality of the web service and its components.

### Running Tests

1. **Run All Tests**:
To execute all tests, run the following command:
```sh
make run_all_tests
```
2. **Run Unit Tests Only**: 
To run only the unit tests, use:
```sh
make run_unit_tests
```
3. **Run Integration Tests Only**:
To run only the integration tests, use:
```sh
make run_integration_tests
```
4. **Generate Coverage Report**:
You can also run specific test files or individual tests. For example, to run the integration tests for the API endpoints:
```sh
make generate_coverage_report
```

The report will be generated in an HTML format and can be viewed by opening the `htmlcov/index.html` file in your browser.

### Running Specific Tests
If you still prefer to run specific test files or individual tests directly, you can use pytest commands as well. For example, to run the integration tests for the API endpoints:

```sh
pytest tests/integration/test_planets_endpoints.py
```