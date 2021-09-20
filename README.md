# ArtsyML_app

## What is this?

ArstsyML_app is python package that provides a webpage as an interface for `tf-packaging` branch of [ArtsyML](https://github.com/HelmholtzAI-Consultants-Munich/ArtsyML) package.


## Installation:

ArtsyML_app required a few popular python packages which are accessible through PyPI and ArtsyML which is not accessible bia PyPI yet. Thus, the installation procedure incldues three steps: 1) creating a Python3 virtual environment, 2) installing the necessary packages for the ArtsyML_app listed in `requirements.txt` file, 3) installing the `tf-packaging` branch of ArtsyML. We first create a "venv" and name it ".venv_artsyml_app". Then we activate the environment:


```console
$ python3 -m venv .venv_artsyml
$ source .venv_artsyml_app/bin/activate(.venv_artsyml) 
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
(.venv_artsyml_app) $ pip3 install -e .
```

## How to run?
To start the application, open a terminal, got to the root directory of the application, activate the virtual environment type:

```console
(.venv_artsyml_app) $ cd PATH/TO/ARTSYML_APP/DIRECTORY
(.venv_artsyml_app) $ python3 run_debug.py
```

It take few second for prapring ArtsyML objects and a message shows that "Debugger is active!". You can open the application in a browser at `http://127.0.0.1:5000/` address.


## Configuration
You can change configuration of the application using parameters that are set in `config.json`. In following, the parameters in the configuration are explained:

* SECRET_KEY: A secret key used to sign session cookies for protection against cookie data tampering.
    The secret key can be arbitrary string. You may create a strong secret key using secrets package like following:
```console
$ python3
> import secrets
> secrets.token_hex(16)
```
then a random generated string is printed and you can copy and paste it in the json file.

* MAIL_USERNAME: Email account of the application.
* MAIL_PASSWORD: Passwork of the email account. If you have not the password of the email, all the functionality of the application work except email sending.
* style_images: Names and paths to the style image as a dictionary. The paths are started from root directory of the application.
* styling_cycle_seconds: The amount of time in seconds between automatic switch between different style in cycle mode of application.
* snapshot_dir: The directory that stores the snapshots. The content of the directory is deleted by application regularly for data privacy reasons.
