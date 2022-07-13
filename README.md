# property-api

This is a demo API, designed as a wrapper for 3rd party property APIs.

Currently it's configured with [HouseCanary](https://api-docs.housecanary.com/) but the design aims to be flexible enough that another 3rd party API could swap out seamlessly.  The goal is for any consumer of this API to only need to update its endpoints in that event, with minimal disruption to the interface.


## Setup
This code requires python3.8 to run, and assumes you've installed it as a prerequisite.  (Rather than using the system version, a python package manager is recommended (e.g. [pipenv](https://github.com/pyenv/pyenv))
* Install pipenv: `pip install pipenv`

The rest of the setup can be done via a Makefile:
* `make env`: does all installation via pipenv
* `make test`: runs unit tests
* `make clean`: tears down pipenv environment


## Next Steps
* Actually setting up access to a HouseCanary API Key
* Deployment code: cloud infrastructure via Terraform?  CI/CD integration? 
* Integration testing; can we verify that deployed code is behaving as expected, in an automated fashion?


## Future Development
Since the 3rd party APIs likely do not update regularly, we may be able to forego hitting it on every request, and instead build in a cache where we store results.
We could take an approach where we check the cache on each request, and only make a request to the 3rd party API if the property is not present in the cache (or if the cache is stale).
Alternatively we could even eschew making requests to the 3rd party API altogether in this service, and build the cache as a nightly job.
Much depends on the needs of the users, the scale of the requests, and the data's rate of change.