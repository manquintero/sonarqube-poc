<!-- start title -->

# GitHub Action: Sonar Project Generator

<!-- end title -->
<!-- start description -->

Generate or Configure a SonarQuebe or SonarCloud project

<!-- end description -->

<!-- start contents -->

A GitHub action that wraps [python-sonarqube-api](https://github.com/shijl0925/python-sonarqube-api)
library to generate and configure sonar projects in SonarQube and SonarCloud

# Prerequisites

To authenticate in Sonar, an environmental variable `SONAR_TOKEN` needs to be available during execution. Make sure the value is set, otherwise the program would just exist due to missing authentication.

# Usage

<!-- end contents >

<!-- start usage -->

```yaml
- uses: discoveryinc-dtc/sonarqube-poc@v0.0.0
  with:
    # Sonar Platform
    # Default: sonarcloud
    platform: ""

    # Sonar Organization
    # Default: ${{ github.repository_owner }}
    organization: ""

    # Whether the created project should be visible to everyone, or only specific
    # user/groups.
    # Default: private
    visibility: ""

    # Key of the project
    # Default: ${{ github.event.repository.name }}
    project: ""
```

<!-- end usage -->

# Inputs

<!-- start inputs -->

| **Input**          | **Description**                                                                          | **Default**                           | **Required** |
| ------------------ | ---------------------------------------------------------------------------------------- | ------------------------------------- | ------------ |
| **`platform`**     | Sonar Platform                                                                           | `sonarcloud`                          | **false**    |
| **`organization`** | Sonar Organization                                                                       | `${{ github.repository_owner }}`      | **false**    |
| **`visibility`**   | Whether the created project should be visible to everyone, or only specific user/groups. | `private`                             | **false**    |
| **`project`**      | Key of the project                                                                       | `${{ github.event.repository.name }}` | **false**    |

<!-- end inputs -->

# Outputs

<!-- start outputs -->
<!-- end outputs -->

<!-- start contents -->

# Local Testing

<!-- start contents -->

## Spin a local server for testing the API (Docker)

For local testing via Docker:

```sh
docker run -d --name sonarqube -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true -p 9000:9000 sonarqube:latest
```

## Split a local server for testing the API (Helm)

For local testing via Kubernetes:

```sh
helm repo add sonarqube https://SonarSource.github.io/helm-chart-sonarqube
helm repo update
kubectl create namespace sonarqube
helm upgrade --install -n sonarqube sonarqube sonarqube/sonarqube --atomic --debug
```

Then expose the service

```
export POD_NAME=$(kubectl get pods --namespace sonarqube -l "app=sonarqube,release=sonarqube" -o jsonpath="{.items[0].metadata.name}")
kubectl port-forward $POD_NAME 8080:9000 -n sonarqube &
```

## Finish setup

Make sure the first login as admin succeeds and the password is updated from the default value.

Once the service is up, you should be able to retrieve an authentication token via Browser.

## Executing the application

The entrypoint is simply a call to a python interpreter with the `main.py` scripts as objective, taking the next set of parameters:

```sh
$ python main.py --help

usage: main.py [-h] [--platform {sonarqube,sonarcloud}] [--project PROJECT]
               [--visibility {private,public}] [--organization ORGANIZATION]

Process Sonar Project information

optional arguments:
  -h, --help            show this help message and exit
  --platform {sonarqube,sonarcloud}
  --project PROJECT
  --visibility {private,public}
  --organization ORGANIZATION
```

<!-- end contents -->
