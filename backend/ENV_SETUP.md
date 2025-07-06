# Environment Setup Guide

## Quick Setup

1. **Copy the example file** (already done):
   ```bash
   cp .env.example .env
   ```

2. **Update required variables in .env**:

### Essential Variables to Update:

#### AI Provider Configuration
```bash
AI_PROVIDER=HUGGINGFACE
HUGGINGFACE_API_KEY=your-actual-huggingface-key-here
```

#### Database Configuration
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name
```

#### Security
```bash
SECRET_KEY=generate-a-strong-secret-key-at-least-64-characters-long
```

### Optional Variables:

#### Redis (if using caching)
```bash
REDIS_URL=redis://localhost:6379/0
```

#### Alternative AI Providers
```bash
# OpenAI (backup)
OPENAI_API_KEY=your-openai-key-here

# DeepSeek (backup)
DEEPSEEK_API_KEY=your-deepseek-key-here
```

## Getting API Keys

### HuggingFace API Key
1. Go to https://huggingface.co/
2. Sign up/Login
3. Go to Settings → Access Tokens
4. Create a new token
5. Copy the token to `HUGGINGFACE_API_KEY`

### Database Setup
If using PostgreSQL:
```bash
# Create database
createdb htmlpagegen_dev

# Update DATABASE_URL with your credentials
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/htmlpagegen_dev
```

## Verification

After setup, verify your configuration:
```bash
# Check if all required variables are set
grep -E "^(AI_PROVIDER|HUGGINGFACE_API_KEY|DATABASE_URL)" .env

# Test the application
python -m app.main
```

## Security Notes

- Never commit the actual `.env` file to version control
- Use different keys for development and production
- Keep your API keys secure and rotate them regularly
- Use environment-specific database names

## Troubleshooting

If you encounter issues:
1. Check that all required variables are set
2. Verify API key validity
3. Ensure database connection is working
4. Check logs for specific error messages
