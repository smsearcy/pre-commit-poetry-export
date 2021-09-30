# pre-commit-poetry-export

![tests workflow](https://github.com/smsearcy/pre-commit-poetry-export/actions/workflows/tests.yml/badge.svg)

[pre-commit](https://pre-commit.com/) hook to keep `requirements.txt` updated in a project that uses [Poetry](https://python-poetry.org/) for managing dependencies.

Forked from https://github.com/avlm/pre-commit-poetry-export,
updated to exclude development requirements and
reworked the implementation.

## Why?
Your life is easier and the build is faster if you use `requirements.txt` file to install dependencies inside a docker image. But, it's not hard to forget to update the requirements file using `poetry export` and remember only when CI can't build the image.

## How to Use
Add the following to your `.pre-commit-config.yaml` file:

```yaml
repos:
  - repo: https://github.com/smsearcy/pre-commit-poetry-export
    rev: v0.2.0
    hooks:
      - id: poetry-export
```

Run `pre-commit run --all-files` to create the `requirements.txt` based on the current `poetry.lock` file.
Future changes to `poetry.lock` will trigger the hook to run again.

## How it Works
This hook runs the following steps:
- If `requirements.txt` doesn't exist then it will be created and the hook will fail.
- Otherwise, if `requirements.txt` exists then the output of `poetry export` is compared to the current contents via a checksum.
  If they match then the hook passes, otherwise, `requirements.txt` is updated and the hook fails.

If the hook has updated or created your requirements file, you can now `git add requirements.txt` and finish your commit.

Found any issues or want to suggest an improvement in the code?
Please contribute by opening an issue.

Thanks! :)
