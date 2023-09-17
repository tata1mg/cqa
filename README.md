### CQA

CQA is an aggregator over popular code quality analysis tools for python.
This tool performs static code analysis and security scan during development and CI/CD pipelines.


### How to install

Open terminal and run below commands.
````
git clone git@github.com:tata1mg/cqa.git
cd cqa/

make install
or
python3 setup.py install

CQA can be installed via

pip3 install git+ssh://git@github.com/tata1mg/cqa.git

````

### How to use 

Add CQA as dependency in your main project.

````
run cqa -h for options

usage: cqa [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] {hook,run} ...

positional arguments:
  {hook,run}
    hook                for options regarding the git hook
    run                 run the given static code analysis tools on the given paths

optional arguments:
  -h, --help            show this help message and exit
  
  --path: Specifies the path(s) to the file(s) or directory(ies) to be analyzed,
         If not provided, cqa will analyze all files in the current directory and its subdirectories.

  --logLevel: Sets the log level. Can be one of DEBUG, INFO, WARNING, ERROR, or CRITICAL.

  --format: Automatically formats the code by fixing formatting and style issues.

  --fail: Causes the command to exit with a non-zero exit code if any errors are found by the static analysis tools.le

   Example: 1. cqa run --path /path/to/my/project --logLevel DEBUG --format
            
            2. cqa hook --install to install pre-commit hook
````

### Tools used

Tools used:

 - The **pylama** package is used for linting and formatting Python code. It is used to ensure that the code adheres to the established coding style and conventions.

 - The **isort** package is used to automatically sort imports in a Python codebase. This helps to improve the readability and maintainability of the code.

 - The **pytype** package is used to automatically infer and check any type-related issues. This is used to ensure no bugs are faced at runtime.

 - The **black** package is used to automatically format Python code according to the established coding style and conventions. This helps to ensure that the code is consistent and easy to read.
 
 - The **Bandit** package is used to check for security vulnerabilities in Python code. It runs a number of security checks and produces a report of any potential vulnerabilities that it finds.
 
 - The **detect_secrets** package is used to check for sensitive information, such as passwords or API keys, in a codebase. This helps to ensure that such information is not accidentally committed to version control.
 
 - The **safety** package is used to check for vulnerable dependencies in project. This helps to ensure that the dependencies used in a project do not have known security vulnerabilities.

config.ini file can be created under project root directory for specifying various configurations of above tools.


### How to raise issues
Please use github issues to raise any bug or feature request

### Discussions

Please use github discussions for any topic related to this project

### Contributions

Soon we will be inviting open source contributions.

### Supported python versions
3.7.x,3.8.x,3.9.x