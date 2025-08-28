#!/bin/bash
set -e

if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    exit 1
fi

sudo apt-get install -y xdotool gedit python3-pip 

CONDA_PATHS=(
    "$HOME/miniconda3"
    "$HOME/anaconda3"
    "$HOME/miniforge3"
    "$HOME/mambaforge"
    "/opt/miniconda3"
    "/opt/anaconda3"
    "/usr/local/miniconda3"
    "/usr/local/anaconda3"
)

init_conda() {
    local conda_path="$1"
    local __conda_setup  # Declare locally to avoid global pollution

    #__conda_setup="$('$conda_path/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
    #if [ $? -eq 0 ]; then
    #    eval "$__conda_setup"
    #    unset __conda_setup  # Clean up after successful eval
    #    return 0
    #fi

    # Fallbacks if hook fails
    if [ -f "$conda_path/etc/profile.d/conda.sh" ]; then
        . "$conda_path/etc/profile.d/conda.sh"
        return 0
    else
        export PATH="$conda_path/bin:$PATH"
        return 0
    fi
}

# Find and init Conda
CONDA_FOUND=0
for conda_path in "${CONDA_PATHS[@]}"; do
    if [ -d "$conda_path" ]; then
        init_conda "$conda_path"
        CONDA_FOUND=1
        break
    fi
done

if [ $CONDA_FOUND -eq 0 ]; then
    echo "Conda not found in common paths. Please install or specify path."
    exit 1
fi


eval "$(conda shell.bash hook)"

if ! conda env list | grep -q "^tjm "; then
    conda create -n tjm
fi

conda activate tjm

if ! conda list pip | grep -q pip; then
    conda install -y pip
fi

if ! pip show pyautogui &> /dev/null; then
    pip install pyautogui pyinstaller
fi

pyinstaller --onefile --console --name post_writer main.py

sudo cp ./dist/post_writer /usr/bin/post_writer
