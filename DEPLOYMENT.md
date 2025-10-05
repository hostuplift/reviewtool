# Deployment Guide for ReviewTool

## Streamlit Cloud Deployment (Recommended)

### Prerequisites
- GitHub repository with your code
- Apify API token
- OpenAI API key

### Step 1: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `hostuplift/reviewtool`
5. Set main file path: `app.py`
6. App URL: Choose a unique name (e.g., `reviewtool-app`)

### Step 2: Configure Secrets

In the Streamlit Cloud dashboard:

1. Go to "Settings" → "Secrets"
2. Add the following secrets:

```toml
APIFY_API_TOKEN = "your_actual_apify_token_here"
OPENAI_API_KEY = "your_actual_openai_key_here"
```

### Step 3: Deploy

1. Click "Deploy"
2. Wait for deployment to complete
3. Your app will be live at: `https://reviewtool-app.streamlit.app`

## Alternative Deployment Options

### Heroku

1. Create a `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.headless=true
```

2. Deploy using Heroku CLI:
```bash
heroku create your-app-name
heroku config:set APIFY_API_TOKEN=your_token
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

### Docker

1. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"]
```

2. Build and run:
```bash
docker build -t reviewtool .
docker run -p 8501:8501 -e APIFY_API_TOKEN=your_token -e OPENAI_API_KEY=your_key reviewtool
```

## Environment Variables

For local development, create a `.env` file:
```
APIFY_API_TOKEN=your_apify_token_here
OPENAI_API_KEY=your_openai_key_here
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are in `requirements.txt`
2. **API Key Issues**: Check that secrets are properly configured
3. **Memory Issues**: Streamlit Cloud has memory limits; consider data caching
4. **Timeout Issues**: Large datasets may timeout; implement pagination

### Performance Tips

1. Cache expensive operations with `@st.cache_data`
2. Limit the number of reviews processed at once
3. Use pagination for large datasets
4. Implement lazy loading for better performance

## Security Considerations

- Never commit API keys to version control
- Use environment variables or secrets management
- Implement rate limiting for API calls
- Add input validation for user data
- Consider adding authentication for production use
