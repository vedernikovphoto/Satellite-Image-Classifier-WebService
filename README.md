<<<<<<< HEAD
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


## API Endpoints

*Note*: The images `file_99.jpg` and `file_212.jpg` used in the examples can be found in the `inference_images` folder in the root directory.

1. `GET  /planet/classes`
   - **Description**: Endpoint to get the list of available classes for prediction.
   - **Example Request**:
     ```bash
     curl -X GET "http://localhost:5000/planet/classes" \
     -H "accept: application/json"
     ```
   - **Example Response**:
     ```json
     {
       "classes": [
         "haze",
         "primary",
         "agriculture",
         "clear",
         "water",
         "habitation",
         "road",
         "cultivation",
         "slash_burn",
         "cloudy",
         "partly_cloudy",
         "conventional_mine",
         "bare_ground",
         "artisinal_mine",
         "blooming",
         "selective_logging",
         "blow_down"
       ]
     }
     ```

2. `POST /planet/predict`
   - **Description**: Endpoint to predict the class of the uploaded image.
   - **Example Request**:
     ```bash
     curl -X POST "http://localhost:5000/planet/predict" \
     -H "accept: application/json" \
     -F "image=@file_99.jpg"
     ```
   - **Example Response**:
     ```json
     {
       "classes": [
         "habitation",
         "slash_burn",
         "bare_ground",
         "blow_down"
       ]
     }
     ```

3. `POST /planet/predict_proba`
   - **Description**: Endpoint to predict the class probabilities of the uploaded image.
   - **Example Request**:
     ```bash
     curl -X POST "http://localhost:5000/planet/predict_proba" \
     -H "accept: application/json" \
     -F "image=@file_212.jpg"
   - **Example Response**:
     ```json
     {
       "haze": 0.0314,
       "primary": 0.0,
       "agriculture": 0.0041,
       "clear": 0.0117,
       "water": 0.0015,
       "habitation": 0.9802,
       "road": 0.0002,
       "cultivation": 0.0,
       "slash_burn": 0.0032,
       "cloudy": 0.0115,
       "partly_cloudy": 0.0294,
       "conventional_mine": 0.003,
       "bare_ground": 0.9973,
       "artisinal_mine": 0.0141,
       "blooming": 0.0051,
       "selective_logging": 0.0002,
       "blow_down": 0.0062
     }
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
=======
# hw-01-service



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.deepschool.ru/cvr8/a.vedernikov/hw-01-service.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.deepschool.ru/cvr8/a.vedernikov/hw-01-service/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
>>>>>>> 2731630e0fc9d14e29a9285fe67d7719ae0cc5d5
