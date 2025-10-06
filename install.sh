#!/bin/bash
"""
OptiMac Enhanced - Quick Installation Script
This script sets up OptiMac Enhanced with all dependencies

Usage: curl -sSL https://raw.githubusercontent.com/VonKleistL/OptiMac/main/install.sh | bash
"""

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/VonKleistL/OptiMac.git"
INSTALL_DIR="$HOME/OptiMac"
APP_NAME="OptiMac Enhanced"

echo -e "${BLUE}"
cat << "EOF"
   ___        _   _ __  __            
  / _ \ _ __ | |_(_)  \/  | __ _  ___ 
 | | | | '_ \| __| | |\/| |/ _` |/ __|
 | |_| | |_) | |_| | |  | | (_| | (__ 
  \___/| .__/ \__|_|_|  |_|\__,_|\___|
       |_|                           
 Enhanced v2.0 - Apple Silicon Optimizer
EOF
echo -e "${NC}"

echo -e "${GREEN}🚀 Installing OptiMac Enhanced...${NC}"

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}❌ This installer is for macOS only!${NC}"
    exit 1
fi

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed!${NC}"
    echo -e "${YELLOW}Please install Python 3 from https://www.python.org${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 found: $(python3 --version)${NC}"

# Check for Git
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is required but not installed!${NC}"
    echo -e "${YELLOW}Please install Xcode Command Line Tools: xcode-select --install${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Git found: $(git --version)${NC}"

# Remove existing installation if it exists
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}⚠️  Existing installation found. Removing...${NC}"
    rm -rf "$INSTALL_DIR"
fi

# Clone the repository
echo -e "${BLUE}📦 Downloading OptiMac Enhanced...${NC}"
git clone "$REPO_URL" "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Install Python dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
pip3 install -r requirements.txt --user

# Make scripts executable
chmod +x build_dmg.sh
chmod +x install.sh

# Create desktop shortcut
DESKTOP_FILE="$HOME/Desktop/OptiMac Enhanced.command"
cat > "$DESKTOP_FILE" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
python3 enhanced_macos_optimizer.py
EOF
chmod +x "$DESKTOP_FILE"

# Create menu bar launcher
MENU_BAR_FILE="$HOME/Desktop/OptiMac Menu Bar.command"
cat > "$MENU_BAR_FILE" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
python3 enhanced_macos_optimizer.py --menubar
EOF
chmod +x "$MENU_BAR_FILE"

# Create Applications shortcut (for Finder sidebar)
APPS_SHORTCUT="$HOME/Applications/OptiMac Enhanced.command"
mkdir -p "$HOME/Applications"
ln -sf "$DESKTOP_FILE" "$APPS_SHORTCUT"

echo -e "${GREEN}"
cat << "EOF"
🎉 OptiMac Enhanced installed successfully!

🚀 How to run:
1. Double-click "OptiMac Enhanced.command" on your Desktop
2. Or run: python3 ~/OptiMac/enhanced_macos_optimizer.py
3. For menu bar mode: python3 ~/OptiMac/enhanced_macos_optimizer.py --menubar

🔧 Features:
• Menu bar integration for quick access
• Save and load optimization profiles
• Spotlight re-indexing capability
• Automatic update checking
• One-click system optimizations

🛡️ Safety:
• All optimizations are reversible
• Backup your system before major changes
• Use advanced options with caution

💬 Support:
• Issues: https://github.com/VonKleistL/OptiMac/issues
• Discussions: https://github.com/VonKleistL/OptiMac/discussions

EOF
echo -e "${NC}"

# Ask if user wants to run now
echo -e "${BLUE}🔥 Would you like to launch OptiMac Enhanced now? (y/n)${NC}"
read -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}🚀 Launching OptiMac Enhanced...${NC}"
    python3 enhanced_macos_optimizer.py &
    echo -e "${GREEN}✅ OptiMac Enhanced is now running!${NC}"
fi

echo -e "${BLUE}Thank you for choosing OptiMac Enhanced! ❤️${NC}"