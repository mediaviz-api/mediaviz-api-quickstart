# Check if the 'venv' folder exists, if not, create the virtual environment
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python -m venv .venv
else
  echo "Virtual environment already exists."
fi

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt
