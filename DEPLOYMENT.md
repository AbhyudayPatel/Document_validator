# 🚀 Deployment Guide

## Issues Fixed

### 1. **Exit Status 128 Error** ✅
- **Root Cause**: Multiple deployment configuration issues
- **Solutions Applied**:
  - Fixed PORT environment variable binding (Render requires dynamic PORT)
  - Standardized Gemini AI model to `gemini-2.0-flash` (was using inconsistent models)
  - Added proper entrypoint script with startup validation
  - Ensured proper line endings for shell scripts (LF, not CRLF)

### 2. **Model Inconsistency** ✅
- Changed both async and sync methods to use `gemini-2.0-flash`
- Removed references to `gemini-2.0-flash-exp` and `gemini-2.5-flash`

### 3. **Environment Variable Handling** ✅
- Added `render.yaml` for proper Render configuration
- Updated Dockerfile to use dynamic PORT with fallback
- Added startup script to validate configuration before launch

## Deployment Steps

### Prerequisites
1. **Render Account**: Sign up at [render.com](https://render.com)
2. **Gemini API Key**: Get from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Deploy to Render

#### Option 1: Using render.yaml (Recommended)
1. Push all changes to your GitHub repository:
   ```bash
   git add .
   git commit -m "Fix deployment issues - exit 128"
   git push origin master
   ```

2. In Render Dashboard:
   - Click **"New +"** → **"Blueprint"**
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`
   - Set the `GEMINI_API_KEY` environment variable
   - Click **"Apply"**

#### Option 2: Manual Setup
1. Push changes to GitHub
2. In Render Dashboard:
   - Click **"New +"** → **"Web Service"**
   - Connect your GitHub repository
   - Configure:
     - **Name**: insurance-document-validator
     - **Runtime**: Docker
     - **Branch**: master
     - **Region**: Oregon (or nearest)
     - **Plan**: Free
   - Add Environment Variable:
     - **Key**: `GEMINI_API_KEY`
     - **Value**: Your actual API key
   - Click **"Create Web Service"**

### Verify Deployment
Once deployed, test your API:
```bash
# Health check
curl https://your-app.onrender.com/

# Test validation
curl -X POST https://your-app.onrender.com/validate \
  -H "Content-Type: application/json" \
  -d '{"document_text": "Policy HM-2025-10-A4B for vessel MV Neptune..."}'
```

## Configuration Files

### Files Created/Modified:
1. **`Dockerfile`** - Updated for Render compatibility
2. **`entrypoint.sh`** - New startup script with validation
3. **`render.yaml`** - Render deployment configuration
4. **`.gitattributes`** - Ensures proper line endings
5. **`ai_extractor.py`** - Fixed model inconsistency

### Key Changes in Dockerfile:
```dockerfile
# Added entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Updated command to use entrypoint
ENTRYPOINT ["./entrypoint.sh"]
```

### entrypoint.sh Features:
- ✅ Checks if GEMINI_API_KEY is configured
- ✅ Validates required files exist
- ✅ Uses dynamic PORT environment variable
- ✅ Provides clear startup logging
- ✅ Proper error handling

## Troubleshooting

### Error: "Exit status 128"
**Causes**:
1. Missing or incorrect environment variables
2. File permission issues
3. Invalid line endings in shell scripts

**Solutions**:
- Ensure `GEMINI_API_KEY` is set in Render dashboard
- Verify `entrypoint.sh` has LF line endings (not CRLF)
- Check Render logs for specific error messages

### Error: "AI service not available"
**Cause**: Missing GEMINI_API_KEY

**Solution**:
1. Go to Render Dashboard → Your Service → Environment
2. Add/Update `GEMINI_API_KEY` environment variable
3. Trigger redeploy

### Error: "Validation service not available"
**Cause**: Missing `valid_vessels.json` file

**Solution**:
- Ensure `provided_assets/valid_vessels.json` is committed to Git
- Verify `.dockerignore` doesn't exclude this file

### Build Fails
**Check**:
1. All files are committed and pushed to GitHub
2. `pyproject.toml` and `uv.lock` are present
3. Docker builds locally: `docker build -t test .`

### Logs
View real-time logs in Render:
- Dashboard → Your Service → Logs
- Look for startup messages from entrypoint.sh

## Local Testing

### Test Docker Build:
```bash
docker build -t insurance-validator .
```

### Test Docker Run:
```bash
docker run -p 8000:8000 \
  -e GEMINI_API_KEY="your-key-here" \
  insurance-validator
```

### Test Entrypoint Script:
```bash
# On Linux/Mac
bash entrypoint.sh

# Or use Docker
docker run -it --entrypoint=/bin/sh insurance-validator
```

## Environment Variables

Required:
- `GEMINI_API_KEY`: Your Google Gemini API key

Optional:
- `PORT`: Port to run on (defaults to 8000, Render sets this automatically)

## Performance

- **Cold Start**: ~5-10 seconds on Render free tier
- **Response Time**: ~1-3 seconds for validation (depends on document size)
- **Scaling**: Automatic with Render paid plans

## Security Notes

- ✅ Runs as non-root user (`appuser`)
- ✅ API key loaded from environment (not hardcoded)
- ✅ Minimal attack surface with slim Python image
- ✅ Dependencies locked with `uv.lock`

## Next Steps

1. **Monitor**: Check Render dashboard for metrics
2. **Test**: Send sample documents to your API
3. **Scale**: Upgrade to paid plan if needed
4. **Custom Domain**: Add in Render settings (optional)

## Support

If issues persist:
1. Check Render logs for detailed error messages
2. Verify all environment variables are set
3. Test locally with Docker first
4. Review [Render Troubleshooting Guide](https://render.com/docs/troubleshooting-deploys)
