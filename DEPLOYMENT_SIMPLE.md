# Deployment Guide

## Quick Start

### Prerequisites
- **Gemini API Key**: Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
- **Docker** (for local testing)

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `PORT`: Server port (default: 8000, auto-configured by most platforms)

## Deploy with Docker

### Local Deployment

```bash
# Build
docker build -t document-validator .

# Run
docker run -d \
  -p 8000:8000 \
  -e GEMINI_API_KEY=your_api_key_here \
  --name document-validator \
  document-validator
```

### Docker Compose

```bash
export GEMINI_API_KEY=your_api_key_here
docker-compose up -d
```

## Cloud Platforms

Works with any Docker-compatible platform:

### Render.com
1. Connect your GitHub repository
2. Create new Web Service (Docker environment)
3. Set environment variable: `GEMINI_API_KEY`
4. Deploy

### Other Platforms
- **AWS ECS/Fargate**: Push to ECR → Create task
- **Google Cloud Run**: Push to GCR → Deploy
- **Azure Container Instances**: Push to ACR → Deploy
- **Heroku**: Use Docker deployment
- **DigitalOcean**: Use App Platform with Docker

All platforms: Just set `GEMINI_API_KEY` environment variable.

## Testing

```bash
# Health check
curl https://your-url/

# Validate document
curl -X POST https://your-url/validate \
  -H "Content-Type: application/json" \
  -d '{
    "document_text": "Your document content",
    "valid_vessels_path": "provided_assets/valid_vessels.json"
  }'
```

## Troubleshooting

**Exit Status 128**: Missing `GEMINI_API_KEY` environment variable
- Solution: Set the variable in your deployment platform

**Build Failures**: Missing files
- Ensure all .py files and provided_assets/ are committed

**Port Issues**: None! Dockerfile uses `${PORT:-8000}` for automatic configuration

**Logs**:
```bash
docker logs document-validator  # Docker
docker-compose logs -f          # Docker Compose
```

## Security
- Never commit API keys
- Container runs as non-root user (uid 1000)
- Use HTTPS in production

## Performance
- Cold start: ~2-3 seconds
- Response time: 5-10 seconds (depends on document length)
- Multi-stage Docker build for optimization
