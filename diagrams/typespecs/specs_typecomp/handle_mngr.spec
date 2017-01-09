/* The HandleMngr module provides an interface for the workspace
  service to make handles sharable. When the owner shares a
  workspace object that contains Handles, the underlying shock
  object is made readable to the person that the workspace object
  is being shared with.
*/
module HandleMngr {
	/* The is_readable function will return true if the
	  underlying shock object is readable by the owner of the
	  token. The token is passed by the client.
	*/
	funcdef is_readable(string token, string nodeurl) returns(int) authentication
		optional;

	/* The add_read_acl functions will update the acl of the shock
	  node that the handle references. The function is only accessible to a 
	  specific list of users specified at startup time. The underlying
	  shock node will be made readable to the user requested.
	*/
	typedef string HandleId;
	funcdef add_read_acl(list<HandleId> hids, string username)
		returns () authentication required;
};
