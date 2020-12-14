# Contributing

1) Setup virtual env. Vscode should automatically make it your default environment.

    ```git
    python3 -m  venv venv
    ```

2) Setup pre-commit to run on every commit.

    ```git
    pre-commit install
    ```

    You also could run it manually.

    ```git
    pre-commit run --all-files
    ```

3) Create a new branch using the following command.

    ```git
    git checkout -b branch_name
    ```

4) After making your changes or adding any features, create a pull request. After it is reviewed it will be merged to the code base. 