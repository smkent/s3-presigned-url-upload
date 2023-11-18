# s3-presigned-url-upload: Presigned URL s3 upload test project

[![Build](https://img.shields.io/github/checks-status/smkent/s3-presigned-url-upload/main?label=build)][gh-actions]
[![codecov](https://codecov.io/gh/smkent/s3-presigned-url-upload/branch/main/graph/badge.svg)][codecov]
[![GitHub stars](https://img.shields.io/github/stars/smkent/s3-presigned-url-upload?style=social)][repo]

This is a utility project to test presigned URLs with an S3 bucket, particularly
for testing object upload using a presigned POST request URL and parameters.

Access keys, secret keys, and the bucket base URL are reused from `s3cmd`'s
configuration file, `~/.s3cfg`.

## Invocation

### Usage with Poetry (recommended)

```console
poetry install
poetry run s3-presigned-url-upload
```

### Usage with pip

```console
pip install boto3 requests
python s3_presigned_url_upload/main.py
```

## Usage

To generate a presigned POST request upload URL and parameters:

```console
poetry run s3-presigned-url-upload upload -b my-bucket -f dest-object-name.txt
```

To generate and execute a presigned POST request upload URL and parameters:

```console
poetry run s3-presigned-url-upload upload -b my-bucket -f dest-object-name.txt -l local-file-to-upload.txt
```

## Development

### [Poetry][poetry] installation

Via [`pipx`][pipx]:

```console
pip install pipx
pipx install poetry
pipx inject poetry poetry-dynamic-versioning poetry-pre-commit-plugin
```

Via `pip`:

```console
pip install poetry
poetry self add poetry-dynamic-versioning poetry-pre-commit-plugin
```

### Development tasks

* Setup: `poetry install`
* Run static checks: `poetry run poe lint` or
  `poetry run pre-commit run --all-files`
* Run static checks and tests: `poetry run poe test`

---

Created from [smkent/cookie-python][cookie-python] using
[cookiecutter][cookiecutter]

[codecov]: https://codecov.io/gh/smkent/s3-presigned-url-upload
[cookie-python]: https://github.com/smkent/cookie-python
[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[gh-actions]: https://github.com/smkent/s3-presigned-url-upload/actions?query=branch%3Amain
[pipx]: https://pypa.github.io/pipx/
[poetry]: https://python-poetry.org/docs/#installation
[repo]: https://github.com/smkent/s3-presigned-url-upload
