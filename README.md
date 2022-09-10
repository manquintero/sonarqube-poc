# sonarqube-poc
Testing the sonarqube api on Python


# Spin a local server for testing the API

docker run -d --name sonarqube -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true -p 9000:9000 sonarqube:latest


# Kubernetes

helm repo add sonarqube https://SonarSource.github.io/helm-chart-sonarqube
helm repo update
kubectl create namespace sonarqube
helm upgrade --install -n sonarqube sonarqube sonarqube/sonarqube --atomic --debug


# Expose
export POD_NAME=$(kubectl get pods --namespace sonarqube -l "app=sonarqube,release=sonarqube" -o jsonpath="{.items[0].metadata.name}")
kubectl port-forward $POD_NAME 8080:9000 -n sonarqube &

# Update admin password

# Run analysis
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=hello-world \
  -Dsonar.host.url=http://127.0.0.1:8080 \
  -Dsonar.login=TOKEN