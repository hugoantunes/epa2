/************************************************************************************
												AJAX THREADS
	
	This is a simple set of functions that enable real AJAX "threading." It uses a
	global array of requests to track the threads. I just keep incrementing the array
	index, but I do delete expired entries as they are satisfied.
	
	This LOOKS simpler than ajax_queue.js, but is actually more complex to implement.
	
	For some time, I was under the impression that real threads weren't possible.
	
	That's because I made some mistakes in my implementation, and assumed some things
	about JavaScript that weren't true. JavaScript LOOKS like C, but sure as heck don't
	BEHAVE like it (for Ss and Gs, try doing an alert() with a function pointer as the
	parameter. If you are a C programmer, you'll be ROTFL).
	
	In any case, the real reason I had this impression was because I wasn't handling
	the client side properly. I was implementing a system that allowed instances to be
	overwritten, and this terminated the transaction.
	
	This won't fix that. That's because this is below that level. Like I said, this
	LOOKS simple, but you need to implement a fairly robust handler system on top of
	it in order to keep from stomping all over yourself. If you want simpler and more
	reliable, then use ajax_queue.js. It will be a lot easier to keep track of.
	
	Consider this in the same way you consider ajax_queue.js. It is a "low-level driver."
	This is not a threading framework, but could easily be the basis for a more
	comprehensive solution.
	
	HOW THIS MESS WORKS:
	
	This uses a global array (g_callback_array), which contains all the executing
	threads. When the thread is complete, the array elements for that thread are
	scragged, but the index keeps going. Since this happens on only one page, this
	shouldn't be a problem.
	
	UPDATE: As of version 1.0.1, I now re-use old elements.
	
	You can provide two callbacks to the request: a "simple" callback, and a
	"complex" callback. The "simple" callback is called only at the end of the
	request, and has fewer parameters. The "complex" callback is invoked at each
	stage of the request, and has a couple more useful parameters.
	
	In order to ensure that the callback to the request is always valid, I actually
	construct each "core" callback out of whole cloth, and slap it into the array
	element for that thread. Once the request is complete, the function is deleted,
	along with all the rest of the stuff.
	
	The "core" callback is used as a "router," in the same manner as in
	ajax_queue.js. It consolidates the HTTPRequest response with the data we keep
	in the array, and invokes the callback supplied by the calling context. This
	can be used to help the calling context re-establish its context in a callback.
	
	Your callback functions need to look like this:
	
			function SimpleCallback(in_text, in_param, in_param2)
			
	Where "in_text" is the response from the HTTPRequest, "in_param" is the first
	parameter you supplied, and "in_param2" is the second parameter.
	
			function ComplexCallback(in_stage, in_text, in_param, in_param2, in_index)
	
	This function adds two more parameters: "in_stage" is the stage of the HTTPRequest,
	and "in_index" is the actual index into the g_callback_array array for this request.
	
	The complex callback is always called before the simple callback. If you want to
	use it for catching the complete stage, then look for in_stage == 4.
	
	Version: 1.6.1
	
	January 31st, 2008:		Made the counter in a bit more robust. It had issues with IE5
	
	October 9th, 2007:		Added SimpleAJAXCall()
	
	September 19th, 2007:		Simplified the SupportsAjax() call and now use the more flexible XHTMLRequestObject
									generator provided by Jeremy Lucier.
									I also added timeouts.
	
	January 6th, 2007:			Duh. Boy did I make a silly mistake. I had the wrong comparison operator
									for my "SupportsAjax()" function wrapper. Since I had incorrectly applied
									the typeof operator previously, this was masked, but when I stripped it for
									the IE5 fix, the bug came to the surface.
	
	December 20th, 2006:		I don't need g_callback_index anymore, so I made it a local.
	
	December 19th, 2006:		I fixed a bug in which the callback index was being unneccessarily
									incremented.

	December 19th, 2006:		I fixed the SupportsAjax() test. It wasn't done properly.
	
	December 19th, 2006:		I now re-use old array elements, as opposed to continuously
									incrementing the pointer.
			
	Copyright:	Go ahead and use this as you wish. You can remove this copyright, and you don't
					have to give me credit, but don't be takin' credit yourself, or mis-assign the
					credit.
					
				Â©2006-2007, Chris Marshall http://www.cmarshall.net/
*/

var	g_callback_array = new Array();	// This holds the threads.

/****************************************************************
	This is where the call is actually made. A new element is
	added to the array, and the sub-array elements are set to
	the items passed in.
	
	Parameters:
		in_url:					The URL to be called. It should include
									all arguments. If the method is a POST,
									the arguments will be stripped and sent
									separately.
		in_simple_callback:		A function pointer to the "simple" callback.
		in_method:				The calling method. "GET" or "POST". "GET" is default.
		in_complex_callback:	A function pointer to the "complex" callback.
		in_param:				A parameter to be returned to the callbacks.
		in_param2:				A second parameter.
		in_timeout_callback:	The callback to be called upon the thread timing out.
		in_timeout_delay:		The delay, in seconds, before the timeout is declared.
	
	Function Return: The g_callback_array index of the request, null otherwise.
*/
function MakeNewAJAXCall(in_url, in_simple_callback, in_method, in_complex_callback, in_param, in_param2, in_timeout_callback, in_timeout_delay ){
	if(!in_method){
		in_method = "GET";
	}
	if(!in_timeout_delay){
		in_timeout_delay = 90;	// 90 seconds default.
	}
	var callback_index = 1;	// We start at 1, so we don't send back "0" for a valid request.
	// Just keep going up until we hit an unoccupied slot.
	while(g_callback_array[callback_index]&&(typeof(g_callback_array[callback_index])!='undefined')){callback_index++};
	// Create the new array element.
	g_callback_array[callback_index] = new Array();
	g_callback_array[callback_index]['request_callback'] = in_simple_callback;
	g_callback_array[callback_index]['request_method'] = in_method;
	g_callback_array[callback_index]['request_complex_callback'] = in_complex_callback;
	g_callback_array[callback_index]['request_param'] = in_param;
	g_callback_array[callback_index]['request_param2'] = in_param2;
	g_callback_array[callback_index]['timeoutcallback'] = in_timeout_callback;
	/*
		Okay, what happens here is that we create a complete new callback for this HTTPRequest.
		I do it this way, to ensure that a static callback is available. If you declare a class
		member function as a callback, it will be called, but "this" will be worthless. There does
		not seem to be a decent way for JavaScript to establish an object context, so I use a static
		array. The caller can use "in_param" to reference an object, which can be called with its
		context intact.
		
		UPDATE: I have found that you can pass object references, but this works extremely well, and
		is relatively simple, so I see no reason to change it.
	*/
	var funcbody = 'var index='+callback_index+';';
	funcbody += 'var stage=g_callback_array[index]["request_object"].readyState;';
	funcbody += 'var resp="";';
	// IE throws a fit if you try to peek before Christmas.
	funcbody += 'if((navigator.appName!="Microsoft Internet Explorer") || (stage==4)){resp=g_callback_array[index]["request_object"].responseText};';
	// The "Complex" callback is always called before the final, "Simple" callback. It is called for each stage.
	funcbody += 'if(g_callback_array[index]["request_complex_callback"]){g_callback_array[index]["request_complex_callback"](stage, resp, g_callback_array[index]["request_param"], g_callback_array[index]["request_param2"], index)};';
	// The "Simple" callback is only called once when the request is final.
	funcbody += 'if((stage==4) && g_callback_array[index]["request_callback"]){g_callback_array[index]["request_callback"](resp, g_callback_array[index]["request_param"], g_callback_array[index]["request_param2"])};';
	// We clean up after ourselves. Once the request is complete, we delete the array element.
	funcbody += 'if(stage==4){';
	funcbody += 'if(g_callback_array[index]["timeout_t"]){clearTimeout(g_callback_array[index]["timeout_t"])};';	// Kill the pending timeout.
	funcbody += 'g_callback_array[index]["request_object"]=null;';
	funcbody += 'g_callback_array[index]["request_callback"]=null;';
	funcbody += 'g_callback_array[index]["request_method"]=null;';
	funcbody += 'g_callback_array[index]["request_complex_callback"]=null;';
	funcbody += 'g_callback_array[index]["request_param"]=null;';
	funcbody += 'g_callback_array[index]["callback"]=null;';
	funcbody += 'g_callback_array[index]["timeoutcallback"]=null;';
	funcbody += 'g_callback_array[index]=null;';
	funcbody += "}";
	
	// This is what is called upon a timeout.
	// We make sure a callback function was provided. If so, we call it.
	var	funcbodytimeout = 'if(g_callback_array['+callback_index+']["request_object"]){g_callback_array['+callback_index+']["request_object"].onreadystatechange=null;g_callback_array['+callback_index+']["request_object"].abort()};';
	funcbodytimeout += 'if(g_callback_array['+callback_index+']["timeoutcallback"]){g_callback_array['+callback_index+']["timeoutcallback"](g_callback_array['+callback_index+']["request_param"], g_callback_array['+callback_index+']["request_param2"],'+callback_index+')};';
	funcbodytimeout += 'g_callback_array['+callback_index+']["request_object"]=null;';
	funcbodytimeout += 'g_callback_array['+callback_index+']["request_callback"]=null;';
	funcbodytimeout += 'g_callback_array['+callback_index+']["request_method"]=null;';
	funcbodytimeout += 'g_callback_array['+callback_index+']["request_complex_callback"]=null;';
	funcbodytimeout += 'g_callback_array['+callback_index+']["request_param"]=null;';
	funcbodytimeout += 'g_callback_array['+callback_index+']["callback"]=null;';
	funcbodytimeout += 'g_callback_array['+callback_index+']["timeoutcallback"]=null;';
	funcbodytimeout += 'g_callback_array['+callback_index+']=null;';

	// Here's where we actually set the functions into the array.
	g_callback_array[callback_index]['callback'] = new Function (funcbody);
	
	g_callback_array[callback_index]['timeout_t'] = setTimeout(new Function (funcbodytimeout),(in_timeout_delay * 1000));
	
	// Here's where the actual AJAX call is made.
	var ret = null;
	if(CallXMLHTTPObject ( in_url, in_method, g_callback_array[callback_index]['callback'], callback_index )){
		ret = callback_index;
	}
	return ret;
};

/****************************************************************
	Here is where the actual call is made to the server.
	
	Parameters:
		in_url:			The URL to be called. It should include
							all arguments. If the method is a POST,
							the arguments will be stripped and sent
							separately.
		in_method:		The calling method. "GET" or "POST".
		in_callback:	A function pointer to the "core" callback that
							exists only in the array.
		in_index:		The index into the main array for this request.
		
	Function Return: True if the request was successful, false otherwise.
*/
function CallXMLHTTPObject ( in_url, in_method, in_callback, in_index ) {
	try {
		var sVars = null;
		
		// Split the URL up, if this is a POST.
		if ( in_method == "POST" ) {
			var rmatch = /^([^\?]*)\?(.*)$/.exec ( in_url );
			in_url = rmatch[1];
			sVars = unescape ( rmatch[2] );
		}
		
		// Create the request object and start the request going.
		g_callback_array[in_index]['request_object'] = MakeNewRequestObject();
		g_callback_array[in_index]['request_object'].open(in_method, in_url, true);
		
		if ( in_method == "POST" ) {
			g_callback_array[in_index]['request_object'].setRequestHeader("Method", "POST "+in_url+" HTTP/1.1");
			g_callback_array[in_index]['request_object'].setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
		}
		
		g_callback_array[in_index]['request_object'].onreadystatechange = in_callback;
		g_callback_array[in_index]['request_object'].send(sVars);
		
		return true;
	} catch ( z ) {
	}
	
	return false;
};

/****************************************************************
	Constructs a new HTTP Request object. IE and the rest of the
	world have different ideas about what constitutes an HTTP
	Request class, so we deal with that here.
	
	We use the conditional Jscript stuff that IE supports to create
	an *.XMLHTTP object, or the standard Mozilla/Netscape XMLHttpRequest object.
	
	We use this as a test. If this object can't create the HTTP request object
	(either XMLHttpRequest or *.XMLHTTP), then the browser can't handle AJAX.

	Function Return: A new request object.
*/
function MakeNewRequestObject() {
	var	ret;
	if ( !ret && (typeof XMLHttpRequest != 'undefined') ) {
		ret = new XMLHttpRequest();
	}
	// check the dom to see if this is IE or not
	if (window.XMLHttpRequest) {
		// Not IE
		ret = new XMLHttpRequest();
	} else if (window.ActiveXObject) {
		// Hello IE!
		// Instantiate the latest MS ActiveX Objects
		if (dm_xmlhttprequest_type) {
			ret = new ActiveXObject(dm_xmlhttprequest_type);
		} else {
			// loops through the various versions of XMLHTTP to ensure we're using the latest
			var versions = ["Msxml2.XMLHTTP.7.0", "Msxml2.XMLHTTP.6.0", "Msxml2.XMLHTTP.5.0", "Msxml2.XMLHTTP.4.0", "MSXML2.XMLHTTP.3.0", "MSXML2.XMLHTTP", "Microsoft.XMLHTTP"];
			for (var i = 0; i < versions.length ; i++) {
         	try {
					// try to create the object
						// if it doesn't work, we'll try again
						// if it does work, we'll save a reference to the proper one to speed up future instantiations
					ret = new ActiveXObject(versions[i]);
					if (ret) {
						dm_xmlhttprequest_type = versions[i];
						break;
					}
            }
            catch (objException) {
            	// trap; try next one
				};
			};
		}
	}
	
	return ret;
};

/******************************************************************
	Returns true if the browser will support Ajax
	
	Very simple. We just create a request object. If it succeeds, we're in like Flint.

	Function Return: True if the client supports AJAX, false otherwise.
*/

if (typeof SupportsAjax == 'undefined'){	// In case we included ajax_threads.js
	function SupportsAjax ( ) {
		var test_obj = MakeNewRequestObject();
		
		if ( test_obj ) {
			test_obj = null;
			return true;
			}
		
		test_obj = null;
		
		return false;
	};
}

if ( typeof SimpleAJAXCall == 'undefined' ){
	/******************************************************************
		Completely simplified AJAX Call. Just add a callback.
		
		Params:
			in_uri: 			The URI to call. Even if it is a POST, you
								specify the URI as if it were a GET. The class
								will take care of stripping out the parameters.
								This parameter is required.
								
			in_callback:	A function to be called upon completion
								Your callback should have the following format:
								
								function Callback(in_string)
								
								You don't have to worry about a parameter, as
								none will be sent in this simplified callback.
								This parameter is required.
								
			in_method:		The HTTP method to use (default is GET).
								Must be either 'GET' or 'POST' (case-insensitive)
								This parameter is optional.
								
			in_param:		A "context keeper" parameter. This will be passed
								into your callback.
								This parameter is optional.
								
		Function return:
			true if the call was successfully queued (not actually sent as
			a request), false if there was any type of error. The type of
			error is not specified. It could be a required parameter was not
			sent in, the browser does not support AJAX, or there was an issue
			with the queue mechanism.
	*/
	
	function SimpleAJAXCall ( in_uri, in_callback, in_method, in_param ) {
		// The method indicator is actually optional, so we make it GET if nothing was passed.
		if ( (typeof in_method == 'undefined') || ((in_method != 'GET')&&(in_method != 'POST')) ) {
			in_method = 'GET';
			}
		
		in_method = in_method.toUpperCase();
		
		// We verify that the proper parameters have been passed in.
		if ( SupportsAjax() && (typeof in_uri != 'undefined') && in_uri && (typeof in_callback == 'function') ) {
			return MakeNewAJAXCall ( in_uri, in_callback, in_method, null, in_param );
			}
		else {
			return false;
			}
	}
}