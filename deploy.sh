#!/bin/bash
# Deployment script for Prex Challenge server monitoring system

# Variables - EC2 instance details
EC2_HOST="56.124.17.51" # Public IP of the EC2 instance
KEY_PATH="./prex-challenge-key.pem"
REMOTE_USER="ubuntu" # Default user for Ubuntu AMIs
REMOTE_DIR="/home/ubuntu/prex-challenge"

# Check if key exists and has correct permissions
if [ ! -f "$KEY_PATH" ]; then
    echo "Error: Key file not found at $KEY_PATH"
    exit 1
fi

# Ensure key has correct permissions (required by SSH)
chmod 400 "$KEY_PATH"

# Create a deployment package, excluding unnecessary files
echo "Creating deployment package..."
tar --exclude="venv" --exclude=".git" --exclude="__pycache__" --exclude="*.log" --exclude="data" -czf prex-challenge.tar.gz ./

# Create remote directory if it doesn't exist
echo "Creating remote directory..."
ssh -i "$KEY_PATH" -o StrictHostKeyChecking=no "$REMOTE_USER@$EC2_HOST" "mkdir -p $REMOTE_DIR"

# Copy files to EC2 instance
echo "Copying files to EC2 instance..."
scp -i "$KEY_PATH" prex-challenge.tar.gz "$REMOTE_USER@$EC2_HOST:$REMOTE_DIR/"

# Extract files and set up environment on the EC2 instance
echo "Setting up environment on EC2 instance..."
ssh -i "$KEY_PATH" "$REMOTE_USER@$EC2_HOST" << EOF
    cd $REMOTE_DIR
    tar -xzf prex-challenge.tar.gz
    rm prex-challenge.tar.gz

    # Install dependencies
    sudo apt update
    sudo apt install -y python3-pip python3-venv
    
    # Create and activate virtual environment
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
    # Create data directory
    mkdir -p data
    
    # Stop any existing API server
    pkill -f "python3 api_server/run_api.py" || true
    
    # Start API server in background
    nohup python3 api_server/run_api.py --host 0.0.0.0 --port 5000 > api_server.log 2>&1 &
    
    # Set up firewall to allow access to port 5000
    sudo ufw allow 5000/tcp
    
    echo "Deployment completed. API server running on port 5000."
EOF

# Clean up local deployment package
rm prex-challenge.tar.gz

echo "Deployment script completed."
echo "To test the agent against your EC2 instance, run:"
echo "python agent/run_agent.py --url http://$EC2_HOST:5000/ --once"
