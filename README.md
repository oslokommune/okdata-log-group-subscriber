# okdata-log-group-subscriber

AWS Lambda function for automatically setting up subscriptions to new CloudWatch
Log Groups when they are created. Configure the function by setting the
following environment variables:

| Variable name              | Description                                                                           |
|----------------------------|---------------------------------------------------------------------------------------|
| `DESTINATION_ARN`          | ARN of the resource to set up subscriptions for.                                      |
| `FILTER_PATTERN`           | Only log entries matching this pattern are sent to the destination.                   |
| [`SUBSCRIPTION_ALLOWLIST`] | Optional regex. Create subscriptions only for log groups with names matching this.    |
| [`SUBSCRIPTION_DENYLIST`]  | Optional regex. Don't create subscriptions for log groups with names containing this. |

Note that CloudTrail logging *must* be enabled on the AWS account in order for
this component to be able to subscribe to `CreateLogGroup` events.

## Tests

Tests are run using [tox](https://pypi.org/project/tox/): `make test`

For tests and linting we use [pytest](https://pypi.org/project/pytest/),
[flake8](https://pypi.org/project/flake8/) and
[black](https://pypi.org/project/black/).

## Deploy

The service is defined in `template.yaml` and deployed with the [AWS SAM
CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).
Per-environment settings (stack name, deployment bucket, region) live in
`samconfig.toml`.

Deploy to both dev and prod is automatic via GitHub Actions on push to main. You
can alternatively deploy from local machine with: `make deploy` or `make
deploy-prod`. This requires the SAM CLI and a local `python3.14` interpreter.
If you don't have Python 3.14, build inside Docker with `sam build
--use-container` instead.

The GitHub deploy role can only update an existing stack: it is not allowed to
create IAM roles. The first deployment to an environment must therefore be done
from a local machine with administrator access.
