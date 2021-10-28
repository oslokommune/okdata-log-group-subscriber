# okdata-log-group-subscriber

AWS Lambda function for automatically setting up subcriptions to new CloudWatch
Log Groups when they are created. Configure the function by setting the
following environment variables:

| Variable name              | Description                                                                           |
|----------------------------|---------------------------------------------------------------------------------------|
| `DESTINATION_ARN`          | ARN of the resource to set up subscriptions for.                                      |
| `FILTER_PATTERN`           | Only log entries matching this pattern are sent to the destination.                   |
| [`SUBSCRIPTION_WHITELIST`] | Optional regex. Create subscriptions only for log groups with names matching this.    |
| [`SUBSCRIPTION_BLACKLIST`] | Optional regex. Don't create subscriptions for log groups with names containing this. |

## Setup

In these examples, we use the default `python3` distribution on your platform.
If you need a specific version of python you need to run the command for that
specific version. Ie. for 3.8 run `python3.8 -m venv .venv` instead to get a
virtualenv for that version.

### Installing global python dependencies

You can either install globally. This might require you to run as root (use
sudo).

```bash
python3 -m pip install tox black pip-tools
```

Or, you can install for just your user. This is recommended as it does not
require root/sudo, but it does require `~/.local/bin` to be added to `PATH` in
your `.bashrc` or similar file for your shell. E.g.:
`PATH=${HOME}/.local/bin:${PATH}`.

```bash
python3 -m pip install --user tox black pip-tools
```

### Installing local python dependencies in a virtualenv

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```bash
make init
```

## Tests

Tests are run using [tox](https://pypi.org/project/tox/): `make test`

For tests and linting we use [pytest](https://pypi.org/project/pytest/),
[flake8](https://pypi.org/project/flake8/) and
[black](https://pypi.org/project/black/).

## Deploy

Deploy to both dev and prod is automatic via GitHub Actions on push to
`main`. You can alternatively deploy from local machine (requires `saml2aws`)
with: `make deploy` or `make deploy-prod`.
