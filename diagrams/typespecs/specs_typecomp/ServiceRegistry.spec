/* The service registry maintains a list of services and their
   url endpoints. The design assumes deploy time registration
   rather than runtime registration. The design assumes that
   clients can construct the url using a defined standard for
   service urls and therefor do not need to rely heavily on
   registry lookups at runtime.
*/
module ServiceRegistry {

    /* TYPE DECLARATIONS */

	/* Information about a service such as its name and its 
	   namespace are captured in the ServiceInfo structure.
	   The keys and values in the structure are:
		service_name - holds a string that is the service name.
		namespace - holds a string that is an enumeration of the
					different types of deployments, such as
					prod, dev, test, etc.
		hostname  - is the name of the host (or ip adress) that the 
				service is running on.
                port      - is the port number that the service is listening on.
                ip_allows - is a list of IP addresses that should be allowed
                                to connect to this service. The default is all.

	*/
	typedef structure {
		string service_name;
		string namespace;
		string hostname;
		int port;
		list<string> ip_allows;
	} ServiceInfo;




    /* FUNCTION DECLARATIONS */

    /*  Register a service. Takes a service struct, and returns the
        service id that is assigned to the newly registered service.
        If the registration of a service is unsuccessful, either an
        error is thrown, or zero is returned.

	The side effect of the register_service call (either directly
	or via an agent on the frontend machine(s)) would be to create
	the nginx configuration stanza that maps api.kbase.us/name/namespace
	to the registered URL. See the update_nginx() function.
    */
    funcdef register_service(ServiceInfo info) returns(int service_id) authentication required;
    
    /* Deregister (delete) an existing service. Takes a service struct,
       and returns 1 if successfully deregistered, returns 0 if failed due
       to authentication issues or on input validation errors.  The namespace
       of the service to be deregistered must be specified in the input
       argument.
    */
    funcdef deregister_service(ServiceInfo info) returns(int success) authentication required;
    
    /* Update the nginx conf file. This function should be considered
	private in so far as it would only be called from the 
	register_service and deregister_service.
    */
	funcdef update_nginx(ServiceInfo info) returns(int success) authentication required;

    /* Provide a list of available services. The enumerate_services
       simply returns the entire set of services that are available.
    */
    funcdef enumerate_services() returns(list<ServiceInfo>);

    /* Provide a list of available service urls. The enumerate_service_urls
       returns the entire set of service urls that are registered in
       the registry. The url will contain the port.
    */
    funcdef enumerate_service_urls() returns (list<string>);

    /* Get the interface description document for the service. The
       get_service_specification returns a string that represents the
       interface specification for the given service.
    */
    funcdef get_service_specification(string service_name, string namespace) returns(string specification);



    /* These methods deal with service availability. */

    /* Is the service alive. The is_alive function will only verify that
       the end-point can be reached over the WAN. The service_url must include
       the port (protocol://hosthame:port). If no protocol is provided, then
       http is assumed.
    */
    funcdef is_alive(string service_url) returns(int alive) authentication optional;


    /* Get the seconds remaining until the service registration expires. */
    funcdef get_expiration_interval(string service_name, string namespace) returns(int seconds_before_service_expiration);

};

