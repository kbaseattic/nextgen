# Current devops challenges

* Heavy deployment--services currently use a full virtual machine
* Difficult to allow developers to deploy their own mini-KBase for development purposes
  -For example, narrative can be deployed locally, but services that a local deployment depends on are much harder
* Would like a process to populate dev environments with enough test data to be useful (probably should be done by service developers?)
* We want to be able to deploy the next version of a module without disrupting the current version, then run tests against the new deployment, then promote the new version only if tests pass
