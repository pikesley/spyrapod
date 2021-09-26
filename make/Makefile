all: style test clean  ## run `style`, `test`, `clean` (default target)

format: isort black  ## run the formatters

black:  ## run the `black` formatter
	python -m black .

isort:  ## run the `isort` formatter
	python -m isort .

style: format  ## run `pylama` (rules are in `setup.cfg`)
	python -m pylama

test:  ## run the tests
	python -m pytest \
		--verbose \
		--exitfirst \
		--last-failed \
		--random-order \
		--cov \
		--capture no

clean:  ## clean the cruft
	@for cruft in $$(find . -name __pycache__) ; do rm -fr $${cruft} ; done
	@rm -fr .pytest_cache

populate: guard-CLIENT_ID guard-CLIENT_SECRET  ## backfill historic data
	@python populate.py
	@python process.py

refresh: guard-CLIENT_ID guard-CLIENT_SECRET  ## collect latest data
	@python refresh.py
	@python process.py

guard-%:
	@ if [ -z "${${*}}" ]; then \
			echo "You must provide the $* variable"; \
			exit 1; \
	fi

# absolute voodoo from @rgarner
help:  ## show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
