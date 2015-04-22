module AuthIntegration {
	funcdef test_noauth() returns(string s);
	funcdef test_auth_optional() returns(string s) authentication optional;
	funcdef test_auth_required() returns(string s) authentication required;
};
