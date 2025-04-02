# Check if the 'venv' folder exists, if not, create the virtual environment
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
else
  echo "Virtual environment already exists."
fi

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
