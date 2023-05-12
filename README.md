## Introduction
# Test Automation Success Factors
- 1. Test Automation Engineer: right combination of factors, usually the best person is the one with strong Development and QA background,
depending on the needs of each individual project.
- 2. Test Automation Architecture: this is a very important success factor according to ISTQB TAE syllabus and according to
practical experience working on automation projects. The TAA has to be carefully designed from the beginning of the project such that:
- a. It will be easily extended going forward, to accomodate new features and changes to existing features
- b. It will be as easily to maintain as possible: maintenance is a very important important topic in automation
- Note: see the proposed HOPR TAA in `./documentation/tas_architecture`

## Type of Tests implemented
Proposal: start with unit and integration tests of the API and then move upward to start building a few system, end-to-end, and
acceptance tests as the system grows in complexity and adoption.

- Unit tests: The TAS has to be itself tested while implementing features into it, so in order to test the features I setup some unit tests
in the `./tests_unit` directory. There we can play around and experiment while implementing new features of the TAS and also we can use that
section to extend further with the unit testing of the API if desired.
- Integration tests: Since the company just started in 2020, I'm assuming I will be the first official QA into the company having to start all QA
processes from scratch. Even if this is not the case its probably less likely the product has evolved too many layers of testing in just about 2 years.
So, we first have to usually start with some unit and integration tests and as the company grows in size and in features we can move higher up the
testing pyramid and also implement some performance, system, e2e tests.
So, the purpose of integration tests is to test that each individual feature interacts with the other components in the correct way.
For example, messages feature has to interact with the node feature, because the messages has to be sent between nodes. Also, in order to have access
to messages APIs, we need the Tokens feature to obtain an authentication token, etc.
- System tests: we check how the system performs overall, it is usually performed after Integration testing. It is carried out for performing both
functional and non-functional testing (performance, fuzz). Since the testing is limited to the evaluation of functional requirements, hence, it includes black-box testing techniques only.
- Acceptance tests: 

## Project Setup
In order to setup the project we need to run the following commands (Ubuntu)
- `pip3 install --upgrade pip3`
- `pip3 install -r requirements.txt`
- `docker run --rm -d --network host --name pluto_cluster gcr.io/hoprassociation/hopr-pluto:1.92.7`
- `docker logs -f pluto_cluster`
- We use host network mode by adding `--network host` to the original command so that we can do a port-mapping to localhost

## Running tests
Unit tests are just built with the purpose to test the TAS wrapper library itself, but you should run the integration tests.
- Run integration tests: `pytest -v tests_integration/`
- Run all tests: `pytest -v`
- Run test from a specific file: `pytest <filename> -v`
- Run tests containing a string in its name: `pytest -k <substring> -v`
- Run marked tests: `pytest -m <markername> -v`

## Shutting down the container
- `docker stop pluto_cluster`

## Generate codebase documentation
- Run the command `python -m pydoc sys`