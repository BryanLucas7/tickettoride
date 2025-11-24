#!/usr/bin/env fish

# Script to activate the backend virtual environment from any directory
# Usage: source /path/to/project/activate.fish

set PROJECT_ROOT (dirname (realpath (status --current-filename)))
source $PROJECT_ROOT/venv/bin/activate.fish