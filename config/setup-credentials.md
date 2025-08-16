# 🔐 SWE-AGENT Credentials Setup Guide

This guide walks you through setting up all the required API credentials and configurations for the SWE-AGENT system.

## 📋 Prerequisites

- Python 3.11+ installed
- Node.js 18+ installed
- Git installed
- Access to JIRA, GitHub, and Google Cloud Platform

## 🚀 Quick Setup

1. **Copy the environment file:**
   ```bash
   cp config/env.example .env
   ```

2. **Edit the `.env` file with your credentials** (see detailed instructions below)

3. **Run the setup script:**
   ```bash
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

## 🔧 Detailed Configuration

### 1. 🎫 JIRA Setup

#### Generate JIRA API Token:
1. Go to [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Give it a name like "SWE-Agent"
4. Copy the token

#### Configure JIRA:
```bash
# In your .env file:
JIRA_URL=https://your-company.atlassian.net
JIRA_TOKEN=ATATT3xFfGF0_your_token_here
JIRA_USER_EMAIL=your-email@company.com
JIRA_PROJECT_KEY=PROJ
```

#### Test JIRA Connection:
```bash
curl -H "Authorization: Bearer $JIRA_TOKEN" \
     "$JIRA_URL/rest/api/3/search?jql=assignee=AI-Agent"
```

### 2. 🐙 GitHub Setup

#### Generate GitHub Personal Access Token:
1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
   - ✅ `write:packages` (Upload packages to GitHub Package Registry)
   - ✅ `delete:packages` (Delete packages from GitHub Package Registry)
4. Generate and copy the token

#### Configure GitHub:
```bash
# In your .env file:
GH_TOKEN=ghp_your_github_token_here
GH_REPO=your-username/your-repository
GH_USERNAME=your-username
GH_DEFAULT_BRANCH=main
```

#### Test GitHub Connection:
```bash
curl -H "Authorization: token $GH_TOKEN" \
     "https://api.github.com/repos/$GH_REPO"
```

### 3. ☁️ Google Cloud Platform Setup

#### Option A: Service Account (Recommended)

1. **Create a Service Account:**
   ```bash
   # Install gcloud CLI if not already installed
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   
   # Create service account
   gcloud iam service-accounts create swe-agent \
       --description="SWE Agent Service Account" \
       --display-name="SWE Agent"
   
   # Create and download key
   gcloud iam service-accounts keys create ~/swe-agent-key.json \
       --iam-account=swe-agent@YOUR_PROJECT_ID.iam.gserviceaccount.com
   ```

2. **Grant Required Permissions:**
   ```bash
   # Grant Vertex AI User role
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
       --member="serviceAccount:swe-agent@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
       --role="roles/aiplatform.user"
   
   # Grant additional roles if needed
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
       --member="serviceAccount:swe-agent@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
       --role="roles/storage.admin"
   ```

3. **Configure Environment:**
   ```bash
   # In your .env file:
   GCP_PROJECT=your-gcp-project-id
   GCP_REGION=us-central1
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/swe-agent-key.json
   ```

#### Option B: User Account (Development)

1. **Authenticate with gcloud:**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   gcloud auth application-default login
   ```

2. **Configure Environment:**
   ```bash
   # In your .env file:
   GCP_PROJECT=your-gcp-project-id
   GCP_REGION=us-central1
   # GOOGLE_APPLICATION_CREDENTIALS not needed for user auth
   ```

#### Test Google Cloud Connection:
```bash
# Test with gcloud
gcloud auth list
gcloud config get-value project

# Test Vertex AI access
python3 -c "
from google.cloud import aiplatform
aiplatform.init(project='$GCP_PROJECT', location='$GCP_REGION')
print('✅ Google Cloud connection successful')
"
```

### 4. 🔍 SonarQube Setup (Optional)

#### Using SonarCloud:
1. Go to [SonarCloud](https://sonarcloud.io/)
2. Sign up with GitHub account
3. Create a new project
4. Generate a token: Account > Security > Generate Token

#### Configure SonarQube:
```bash
# In your .env file:
SONAR_HOST_URL=https://sonarcloud.io
SONAR_TOKEN=your_sonar_token_here
SONAR_ORGANIZATION=your-organization
SONAR_PROJECT_KEY=your-project-key
```

### 5. 🔨 Maven Setup

#### Install Maven:

**macOS:**
```bash
brew install maven
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install maven
```

**Windows:**
Download from [Apache Maven](https://maven.apache.org/download.cgi)

#### Configure Maven:
```bash
# In your .env file (optional):
MAVEN_HOME=/usr/local/maven
MAVEN_SETTINGS=/path/to/settings.xml
```

#### Test Maven:
```bash
mvn --version
```

## 🧪 Testing Your Setup

### Run the Test Script:
```bash
python3 scripts/test-credentials.py
```

### Manual Testing:

1. **Test Backend:**
   ```bash
   cd backend
   source venv/bin/activate
   python app.py
   # Visit http://localhost:5050/api/issues
   ```

2. **Test Frontend:**
   ```bash
   cd frontend
   npm run dev
   # Visit http://localhost:5173
   ```

3. **Test Full Workflow:**
   ```bash
   npm run dev  # Runs all services
   ```

## 🚨 Security Best Practices

### 1. Environment File Security:
- ✅ Never commit `.env` files to version control
- ✅ Use different `.env` files for different environments
- ✅ Rotate tokens regularly
- ✅ Use least privilege access

### 2. Token Management:
```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo "*.key" >> .gitignore
echo "secrets/" >> .gitignore
```

### 3. Production Setup:
- Use environment variables instead of files
- Use secrets management systems (AWS Secrets Manager, Azure Key Vault, etc.)
- Enable audit logging
- Use service accounts with minimal permissions

## 🐛 Troubleshooting

### Common Issues:

#### JIRA Authentication Failed:
```bash
# Check token validity
curl -H "Authorization: Bearer $JIRA_TOKEN" \
     "$JIRA_URL/rest/api/3/myself"
```

#### GitHub API Rate Limit:
```bash
# Check rate limit status
curl -H "Authorization: token $GH_TOKEN" \
     "https://api.github.com/rate_limit"
```

#### Google Cloud Authentication:
```bash
# Clear and re-authenticate
gcloud auth revoke --all
gcloud auth login
gcloud auth application-default login
```

#### Port Conflicts:
```bash
# Kill processes on required ports
sudo lsof -ti:5050 | xargs kill -9  # Backend
sudo lsof -ti:5173 | xargs kill -9  # Frontend
```

## 📞 Support

If you encounter issues:
1. Check the logs in `/tmp/swe-agent.log`
2. Run tests: `python3 scripts/test-credentials.py`
3. Verify all environment variables are set correctly
4. Check firewall and network configurations

## 🔄 Environment Templates

### Development Environment:
```bash
cp config/env.example .env.development
# Edit for development settings
```

### Production Environment:
```bash
cp config/env.example .env.production
# Edit for production settings with secure values
```

### Docker Environment:
```bash
cp config/env.example .env.docker
# Edit for containerized deployment
```
