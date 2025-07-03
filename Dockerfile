# Build production image
docker build -t cicd-demo .

# Run container
docker run -p 8000:8000 -e ENVIRONMENT=production cicd-demo