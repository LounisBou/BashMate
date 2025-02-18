#!/bin/zsh

# Vérifier si la version de Python est 3.11.x
if [[ $(/Users/lounis/.pyenv/shims/python --version) != *"3.11"* ]]; then
    # Utiliser pyenv pour changer la version de Python
    pyenv global 3.11
fi

# Vérifier si Open WebUI est installé
if [[ $(/Users/lounis/.pyenv/shims/pip list | grep open-webui) == "" ]]; then
    # Installer Open WebUI
    /Users/lounis/.pyenv/shims/pip install --user open-webui
fi

# Démarrer Open WebUI en arrière-plan
/Users/lounis/.pyenv/shims/open-webui serve &