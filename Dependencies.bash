#!/bin/bash

# Fonction pour installer un paquet Python avec pip3 si ce n'est pas déjà installé
install_python_package_if_not_installed() {
    local package_name="$1"
    python3 -m pip install "$package_name"
}


# Installation de bibliothèques Python
echo -e "\n\e[36m# Installation de bibliothèques Python\e[0m"
install_python_package_if_not_installed "onvif-zeep==0.2.12"
install_python_package_if_not_installed "ultralytics==8.1.14"
install_python_package_if_not_installed "numpy==1.23.1"


# LOGO
echo -e "\e[34m                                                  \e[0m"
echo -e "\e[34m  ___________     ______________    _____________ \e[0m"
echo -e "\e[34m |   _______  |  |_____    _____|  |__________   |\e[0m"
echo -e "\e[34m |  |       | |        |  |                  /  / \e[0m"
echo -e "\e[37m |  |_______| |        |  |                /  /  \e[0m"
echo -e "\e[37m |  __________|        |  |              /  /   \e[0m"
echo -e "\e[37m |  |                  |  |            /  /     \e[0m"
echo -e "\e[31m |  |                  |  |           /  /_______ \e[0m"
echo -e "\e[31m |__|                  |__|         /____________|\e[0m"
echo -e "\e[31m                                                  \e[0m"