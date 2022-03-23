# ArtsyML_app

## What is this?
ArstsyML_app is python package that provides a webpage as an interface for `tf-packaging` branch of [ArtsyML](https://github.com/HelmholtzAI-Consultants-Munich/ArtsyML) package.

## Installation:
ArtsyML_app requires a few popular python packages which are accessible through PyPI and ArtsyML which is not accessible via PyPI yet. Thus, the installation procedure includes three steps: 1) creating a Python3 virtual environment, 2) installing the necessary packages for the ArtsyML_app listed in `requirements.txt` file, 3) installing the `tf-packaging` branch of ArtsyML. We first create a "venv" and name it ".venv_artsyml_app". Then we activate the environment:

```console
$ python3 -m venv .venv_artsyml_app
$ source .venv_artsyml_app/bin/activate
(.venv_artsyml_app) $ 
```

Second, in the root directory of the Artsyml_app (the directory which contains `setup.py`), we installed the required packages:

```console
(.venv_artsyml_app) $ cd PATH/TO/ARTSYML_APP/DIRECTORY
(.venv_artsyml_app) $ pip3 install -e .
```

Third, installing the `tf-packaging` branch of ArtsyML package:

```console
(.venv_artsyml_app) $ cd PATH/TO/ARTSYML/DIRECTORY
(.venv_artsyml_app) $ git checkout remotes/origin/tf-packaging
(.venv_artsyml_app) $ bash install_{cpu | gpu}.sh
```
For more information on the installation of ArtsyML see the README [here](https://github.com/HelmholtzAI-Consultants-Munich/ArtsyML)

## How to run?

To start the application, open a terminal, got to the root directory of the application, activate the virtual environment type:

```console
(.venv_artsyml_app) $ cd PATH/TO/ARTSYML_APP/DIRECTORY
(.venv_artsyml_app) $ python3 run_debug.py
```

It takes a few seconds for preparing ArtsyML objects and a message shows that "Debugger is active!". You can open the application in a browser at `http://127.0.0.1:5000/` address.

## Configuration

You can change configuration of the application using parameters that are set in `config.json`. In following, the parameters in the configuration are explained:

* SECRET_KEY: A secret key used to sign session cookies for protection against cookie data tampering. The secret key can be an arbitrary string. You may create a strong secret key using secrets package like following in a terminal:

```console
$ python3
> import secrets
> secrets.token_hex(16)
```

then a randomly generated string is printed and you can copy and paste it in the json file.

* MAIL_USERNAME: Email account of the application.

* MAIL_PASSWORD: Password of the email account. If you do not have the password of the email, all the functionality of the application works except email sending.

* style_images: Names and paths to the style image as a dictionary. The paths are started from the root directory of the application.

* styling_cycle_seconds: The amount of time in seconds between automatic switching between different styles in cycle mode of application.

* snapshot_dir: The directory that stores the snapshots. The content of the directory is deleted by application regularly for data privacy reasons.
