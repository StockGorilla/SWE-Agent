#!/usr/bin/env python3
"""
SWE-AGENT Credentials Testing Script
Tests all API connections and configurations
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Dict, List, Tuple

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env file
def load_env_file(env_path: str = ".env"):
    """Load environment variables from .env file"""
    if not os.path.exists(env_path):
        print(f"❌ .env file not found at {env_path}")
        return False
    
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value
    
    print(f"✅ Loaded environment variables from {env_path}")
    return True

class CredentialTester:
    """Test all API credentials and configurations"""
    
    def __init__(self):
        self.results: List[Tuple[str, bool, str]] = []
    
    def test_jira_connection(self) -> bool:
        """Test JIRA API connection"""
        print("\n🎫 Testing JIRA Connection...")
        
        jira_url = os.getenv('JIRA_URL')
        jira_token = os.getenv('JIRA_TOKEN')
        jira_email = os.getenv('JIRA_USER_EMAIL')
        
        if not jira_url or 'your-company' in jira_url:
            self.results.append(("JIRA", False, "JIRA_URL not configured"))
            return False
        
        if not jira_token or 'your_jira' in jira_token:
            self.results.append(("JIRA", False, "JIRA_TOKEN not configured"))
            return False
        
        try:
            # Test authentication
            headers = {"Authorization": f"Bearer {jira_token}"}
            response = requests.get(f"{jira_url}/rest/api/3/myself", headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"   ✅ Connected as: {user_data.get('displayName', 'Unknown')}")
                
                # Test search capability
                search_url = f"{jira_url}/rest/api/3/search"
                jql = "assignee=AI-Agent"
                search_response = requests.get(
                    search_url, 
                    headers=headers, 
                    params={"jql": jql, "maxResults": 1},
                    timeout=10
                )
                
                if search_response.status_code == 200:
                    issues = search_response.json().get('issues', [])
                    print(f"   ✅ Found {len(issues)} issues for AI-Agent")
                    self.results.append(("JIRA", True, f"Connected as {user_data.get('displayName')}"))
                    return True
                else:
                    self.results.append(("JIRA", False, f"Search failed: {search_response.status_code}"))
                    return False
            else:
                self.results.append(("JIRA", False, f"Authentication failed: {response.status_code}"))
                return False
                
        except requests.RequestException as e:
            self.results.append(("JIRA", False, f"Connection error: {str(e)}"))
            return False
    
    def test_github_connection(self) -> bool:
        """Test GitHub API connection"""
        print("\n🐙 Testing GitHub Connection...")
        
        gh_token = os.getenv('GH_TOKEN')
        gh_repo = os.getenv('GH_REPO')
        
        if not gh_token or 'your_github' in gh_token:
            self.results.append(("GitHub", False, "GH_TOKEN not configured"))
            return False
        
        if not gh_repo or 'your-username' in gh_repo:
            self.results.append(("GitHub", False, "GH_REPO not configured"))
            return False
        
        try:
            # Test authentication
            headers = {"Authorization": f"token {gh_token}"}
            response = requests.get("https://api.github.com/user", headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"   ✅ Connected as: {user_data.get('login', 'Unknown')}")
                
                # Test repository access
                repo_response = requests.get(
                    f"https://api.github.com/repos/{gh_repo}", 
                    headers=headers, 
                    timeout=10
                )
                
                if repo_response.status_code == 200:
                    repo_data = repo_response.json()
                    print(f"   ✅ Repository access: {repo_data.get('full_name')}")
                    
                    # Check permissions
                    permissions = repo_data.get('permissions', {})
                    if permissions.get('push'):
                        print("   ✅ Push permissions: Available")
                        self.results.append(("GitHub", True, f"Connected as {user_data.get('login')}"))
                        return True
                    else:
                        self.results.append(("GitHub", False, "No push permissions"))
                        return False
                else:
                    self.results.append(("GitHub", False, f"Repository access failed: {repo_response.status_code}"))
                    return False
            else:
                self.results.append(("GitHub", False, f"Authentication failed: {response.status_code}"))
                return False
                
        except requests.RequestException as e:
            self.results.append(("GitHub", False, f"Connection error: {str(e)}"))
            return False
    
    def test_google_cloud_connection(self) -> bool:
        """Test Google Cloud / Gemini connection"""
        print("\n☁️ Testing Google Cloud Connection...")
        
        gcp_project = os.getenv('GCP_PROJECT')
        
        if not gcp_project or 'your-gcp' in gcp_project:
            self.results.append(("Google Cloud", False, "GCP_PROJECT not configured"))
            return False
        
        try:
            # Try to import and initialize Vertex AI
            from google.cloud import aiplatform
            from vertexai import init
            from vertexai.language_models import TextGenerationModel
            
            # Initialize Vertex AI
            region = os.getenv('GCP_REGION', 'us-central1')
            init(project=gcp_project, location=region)
            print(f"   ✅ Initialized project: {gcp_project} in {region}")
            
            # Test model access
            try:
                model = TextGenerationModel.from_pretrained("gemini-1.0-pro")
                print("   ✅ Gemini model access: Available")
                
                # Test simple generation
                response = model.predict("Hello", max_output_tokens=10)
                print(f"   ✅ Test generation: Success")
                
                self.results.append(("Google Cloud", True, f"Project: {gcp_project}"))
                return True
                
            except Exception as e:
                print(f"   ⚠️ Model access failed: {str(e)}")
                self.results.append(("Google Cloud", False, f"Model access failed: {str(e)}"))
                return False
                
        except ImportError as e:
            self.results.append(("Google Cloud", False, f"SDK not installed: {str(e)}"))
            return False
        except Exception as e:
            self.results.append(("Google Cloud", False, f"Authentication failed: {str(e)}"))
            return False
    
    def test_sonarqube_connection(self) -> bool:
        """Test SonarQube connection (optional)"""
        print("\n🔍 Testing SonarQube Connection...")
        
        sonar_url = os.getenv('SONAR_HOST_URL')
        sonar_token = os.getenv('SONAR_TOKEN')
        
        if not sonar_url or not sonar_token:
            self.results.append(("SonarQube", False, "Optional - not configured"))
            return False
        
        try:
            headers = {"Authorization": f"Bearer {sonar_token}"}
            response = requests.get(f"{sonar_url}/api/authentication/validate", headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('valid'):
                    print("   ✅ SonarQube authentication: Valid")
                    self.results.append(("SonarQube", True, "Authentication valid"))
                    return True
                else:
                    self.results.append(("SonarQube", False, "Invalid token"))
                    return False
            else:
                self.results.append(("SonarQube", False, f"Connection failed: {response.status_code}"))
                return False
                
        except requests.RequestException as e:
            self.results.append(("SonarQube", False, f"Connection error: {str(e)}"))
            return False
    
    def test_maven_installation(self) -> bool:
        """Test Maven installation"""
        print("\n🔨 Testing Maven Installation...")
        
        try:
            import subprocess
            result = subprocess.run(['mvn', '--version'], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"   ✅ {version_line}")
                self.results.append(("Maven", True, version_line))
                return True
            else:
                self.results.append(("Maven", False, "Maven command failed"))
                return False
                
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.results.append(("Maven", False, f"Maven not found: {str(e)}"))
            return False
    
    def test_backend_import(self) -> bool:
        """Test backend module imports"""
        print("\n🐍 Testing Backend Imports...")
        
        try:
            # Test MCP client import
            sys.path.insert(0, str(project_root / "backend"))
            from orchestrator.mcp_client import orchestrator
            print("   ✅ MCP client import: Success")
            
            # Test Gemini client import
            from orchestrator.gemini_client import generate_text
            print("   ✅ Gemini client import: Success")
            
            # Test workflow import
            from orchestrator.workflow import run_multi_issue_workflow
            print("   ✅ Workflow import: Success")
            
            self.results.append(("Backend Imports", True, "All modules imported successfully"))
            return True
            
        except ImportError as e:
            self.results.append(("Backend Imports", False, f"Import failed: {str(e)}"))
            return False
    
    def print_summary(self):
        """Print test results summary"""
        print("\n" + "="*60)
        print("📊 CREDENTIAL TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for _, success, _ in self.results if success)
        total = len(self.results)
        
        for service, success, message in self.results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{service:<20} {status:<10} {message}")
        
        print("-"*60)
        print(f"Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 All tests passed! Your SWE-AGENT is ready to run.")
            return True
        else:
            print(f"\n⚠️ {total - passed} test(s) failed. Please check your configuration.")
            return False

def main():
    """Main test function"""
    print("🔐 SWE-AGENT Credential Testing")
    print("="*60)
    
    # Load environment variables
    if not load_env_file():
        sys.exit(1)
    
    # Create tester instance
    tester = CredentialTester()
    
    # Run all tests
    tester.test_jira_connection()
    tester.test_github_connection()
    tester.test_google_cloud_connection()
    tester.test_sonarqube_connection()
    tester.test_maven_installation()
    tester.test_backend_import()
    
    # Print summary
    success = tester.print_summary()
    
    if success:
        print("\nNext steps:")
        print("1. Run: ./start-dev.sh")
        print("2. Visit: http://localhost:5173")
        sys.exit(0)
    else:
        print("\nPlease fix the failing tests and run again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
