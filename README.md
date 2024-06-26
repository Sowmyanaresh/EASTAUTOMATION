# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Automation testing for East application

### How do I get set up? ###
* Install python 3.10 and Visual Studio Code
* Install the necessary packages listed in requirements.txt using pip
* Update the test user and environment specific parameters in the config.ini file inside the configurations folder

* Summary of set up - The testing framework has 3 layers as described below - 
1. The bottom layer contains wrapper functions for elementary operations such as click, enter text, enter iframe. The code for this layer goes in Base class (in Helpers)

2. The middle layer uses the bottom layer to develop wrapper functions that comprise of multiple steps and are frequently used. Examples - a) traverse to TOA from application landing page (openTOA.py) b) Complete login process (loginPage.py)

3. The third and top most layer is the test suite where we use the lower layers to write the test steps

### How to run the test case
Enter the following command with test-automation folder being the root directory - change the test case python file (test_smoke.py here) appropriately
pytest -v -s  --html=Reports\report.html --self-contained-html  testCases/test_smoke.py