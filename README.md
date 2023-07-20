# okdata-log-group-subscriber

AWS Lambda function for automatically setting up subscriptions to new CloudWatch
Log Groups when they are created. Configure the function by setting the
following environment variables:

| Variable name              | Description                                                                           |
|----------------------------|---------------------------------------------------------------------------------------|
| `DESTINATION_ARN`          | ARN of the resource to set up subscriptions for.                                      |
| `FILTER_PATTERN`           | Only log entries matching this pattern are sent to the destination.                   |
| [`SUBSCRIPTION_WHITELIST`] | Optional regex. Create subscriptions only for log groups with names matching this.    |
| [`SUBSCRIPTION_BLACKLIST`] | Optional regex. Don't create subscriptions for log groups with names containing this. |

Note that CloudTrail logging *must* be enabled on the AWS account in order for
this component to be able to subscribe to `CreateLogGroup` events.

## Tests

Tests are run using [tox](https://pypi.org/project/tox/): `make test`

For tests and linting we use [pytest](https://pypi.org/project/pytest/),
[flake8](https://pypi.org/project/flake8/) and
[black](https://pypi.org/project/black/).

## Deploy

Deploy to both dev and prod is automatic via GitHub Actions on push to
`main`. You can alternatively deploy from local machine (requires `saml2aws`)
with: `make deploy` or `make deploy-prod`.
