# Build production image
docker build -t fastapi-cicd-demo .

# Run container
docker run -p 8000:8000 -e ENVIRONMENT=production fastapi-cicd-demo