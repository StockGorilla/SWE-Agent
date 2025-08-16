#!/bin/bash

# =============================================================================
# SWE-AGENT Setup Script
# =============================================================================

set -e  # Exit on any error

echo "🚀 Setting up SWE-AGENT..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_step() {
    echo -e "${BLUE}📋 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if .env file exists
check_env_file() {
    if [ ! -f ".env" ]; then
        print_warning "No .env file found. Creating from template..."
        if [ -f "config/env.example" ]; then
            cp config/env.example .env
            print_success "Created .env file from template"
            print_warning "Please edit .env file with your credentials before continuing"
            echo "Run: nano .env or code .env"
            exit 1
        else
            print_error "config/env.example not found!"
            exit 1
        fi
    else
        print_success "Found .env file"
    fi
}

# Check required tools
check_prerequisites() {
    print_step "Checking prerequisites..."
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    # Check Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_success "Node.js $NODE_VERSION found"
    else
        print_error "Node.js is required but not installed"
        exit 1
    fi
    
    # Check npm
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        print_success "npm $NPM_VERSION found"
    else
        print_error "npm is required but not installed"
        exit 1
    fi
    
    # Check Git
    if command -v git &> /dev/null; then
        GIT_VERSION=$(git --version | cut -d' ' -f3)
        print_success "Git $GIT_VERSION found"
    else
        print_error "Git is required but not installed"
        exit 1
    fi
}

# Setup Python virtual environment
setup_python_env() {
    print_step "Setting up Python environment..."
    
    cd backend
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_step "Creating Python virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_success "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    print_step "Upgrading pip..."
    pip install --upgrade pip
    
    # Install dependencies
    print_step "Installing Python dependencies..."
    pip install -r requirements.txt
    print_success "Python dependencies installed"
    
    cd ..
}

# Setup Node.js environment
setup_node_env() {
    print_step "Setting up Node.js environment..."
    
    # Install root dependencies
    if [ -f "package.json" ]; then
        print_step "Installing root npm dependencies..."
        npm install
        print_success "Root dependencies installed"
    fi
    
    # Install frontend dependencies
    cd frontend
    print_step "Installing frontend dependencies..."
    npm install
    print_success "Frontend dependencies installed"
    cd ..
}

# Setup Google Cloud (optional)
setup_gcloud() {
    if command -v gcloud &> /dev/null; then
        print_step "Google Cloud SDK found. Checking authentication..."
        
        # Source .env file to get GCP_PROJECT
        if [ -f ".env" ]; then
            export $(grep -v '^#' .env | xargs)
        fi
        
        if [ -n "$GCP_PROJECT" ] && [ "$GCP_PROJECT" != "your-gcp-project-id" ]; then
            print_step "Setting up Google Cloud project: $GCP_PROJECT"
            gcloud config set project "$GCP_PROJECT"
            
            if [ -n "$GOOGLE_APPLICATION_CREDENTIALS" ] && [ -f "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
                print_success "Service account key file found"
                export GOOGLE_APPLICATION_CREDENTIALS="$GOOGLE_APPLICATION_CREDENTIALS"
            else
                print_warning "No service account key found. Using user authentication."
                print_warning "Run 'gcloud auth application-default login' if needed"
            fi
        else
            print_warning "GCP_PROJECT not configured in .env file"
        fi
    else
        print_warning "Google Cloud SDK not found. Install from: https://cloud.google.com/sdk"
    fi
}

# Verify environment variables
verify_env_vars() {
    print_step "Verifying environment variables..."
    
    # Source .env file
    if [ -f ".env" ]; then
        export $(grep -v '^#' .env | xargs)
    fi
    
    # Check critical variables
    MISSING_VARS=()
    
    # JIRA variables
    [ -z "$JIRA_URL" ] || [ "$JIRA_URL" = "https://your-company.atlassian.net" ] && MISSING_VARS+=("JIRA_URL")
    [ -z "$JIRA_TOKEN" ] || [ "$JIRA_TOKEN" = "your_jira_api_token_here" ] && MISSING_VARS+=("JIRA_TOKEN")
    
    # GitHub variables
    [ -z "$GH_TOKEN" ] || [ "$GH_TOKEN" = "ghp_your_github_personal_access_token" ] && MISSING_VARS+=("GH_TOKEN")
    [ -z "$GH_REPO" ] || [ "$GH_REPO" = "your-username/your-repository" ] && MISSING_VARS+=("GH_REPO")
    
    if [ ${#MISSING_VARS[@]} -gt 0 ]; then
        print_error "Missing or default values for environment variables:"
        for var in "${MISSING_VARS[@]}"; do
            echo "  - $var"
        done
        print_warning "Please update your .env file with actual values"
        return 1
    else
        print_success "All critical environment variables are configured"
        return 0
    fi
}

# Test connections
test_connections() {
    print_step "Testing API connections..."
    
    # Source .env file
    if [ -f ".env" ]; then
        export $(grep -v '^#' .env | xargs)
    fi
    
    # Test JIRA connection
    if [ -n "$JIRA_URL" ] && [ -n "$JIRA_TOKEN" ]; then
        print_step "Testing JIRA connection..."
        if curl -s -H "Authorization: Bearer $JIRA_TOKEN" "$JIRA_URL/rest/api/3/myself" > /dev/null; then
            print_success "JIRA connection successful"
        else
            print_warning "JIRA connection failed - check credentials"
        fi
    fi
    
    # Test GitHub connection
    if [ -n "$GH_TOKEN" ]; then
        print_step "Testing GitHub connection..."
        if curl -s -H "Authorization: token $GH_TOKEN" "https://api.github.com/user" > /dev/null; then
            print_success "GitHub connection successful"
        else
            print_warning "GitHub connection failed - check token"
        fi
    fi
}

# Create startup scripts
create_scripts() {
    print_step "Creating startup scripts..."
    
    # Development script
    cat > start-dev.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting SWE-AGENT in development mode..."

# Load environment variables
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Start all services
npm run dev
EOF
    chmod +x start-dev.sh
    
    # Production script
    cat > start-prod.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting SWE-AGENT in production mode..."

# Load environment variables
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Build frontend
cd frontend && npm run build && cd ..

# Start backend
cd backend && source venv/bin/activate && python app.py
EOF
    chmod +x start-prod.sh
    
    print_success "Startup scripts created"
}

# Main setup function
main() {
    echo "════════════════════════════════════════════════════════════════"
    echo "🤖 SWE-AGENT Automated Setup"
    echo "════════════════════════════════════════════════════════════════"
    
    check_env_file
    check_prerequisites
    setup_python_env
    setup_node_env
    setup_gcloud
    create_scripts
    
    echo ""
    echo "════════════════════════════════════════════════════════════════"
    
    if verify_env_vars; then
        test_connections
        echo ""
        print_success "🎉 Setup completed successfully!"
        echo ""
        echo "Next steps:"
        echo "1. Run './start-dev.sh' to start in development mode"
        echo "2. Visit http://localhost:5173 for the frontend"
        echo "3. API will be available at http://localhost:5050"
        echo ""
        echo "For testing: python3 scripts/test-credentials.py"
    else
        echo ""
        print_warning "Setup completed with warnings"
        echo ""
        echo "Please:"
        echo "1. Update your .env file with actual credentials"
        echo "2. Run this script again to verify setup"
        echo "3. Or run: python3 scripts/test-credentials.py"
    fi
    
    echo "════════════════════════════════════════════════════════════════"
}

# Run main function
main "$@"
