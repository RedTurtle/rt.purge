Introduction
============

This product is only useful if your Plone site use `Varnish`__ reverse proxy.
It will provide a new "*Action*" menu entry named "*Purge*" that will remove from the cache the current
page.

__ http://www.varnish-cache.org/

Configuration
=============

First of all, take a look to the *public.vcl* example file you wil find in the product source "template"
directory.

Dependencies
============

This product is targeted on Plone 3 and Varnish 2.0.x family.

__ plone.app.caching

Also, it need `plone.app.registry`__ (automatically downloaded).

__ http://pypi.python.org/pypi/plone.app.registry

This dependency will download for you:

* zope.proxy
* zope.component
* plone.app.registry
* plone.autoform 
* plone.app.z3cform
* plone.supermodel
* plone.registry
* zope.schema
* plone.z3cform
* zope.security
* collective.z3cform.datetimewidget
* z3c.formwidget.query
* zope.i18n
* z3c.batching
* z3c.form
* zope.location
* zope.browser

See also the example *buildout.cfg* provided.

Versions pinning section example
--------------------------------

Some of those dependencies above can make you crazy, so think about pin specific versions, compatible
with Plone 3.
Here a good version pinning configuration::

    ...
    [versions]
    ...
    plone.app.registry = 1.0b2
    zope.i18n = 3.4.0 
    zope.location = 3.4.0
    zope.site = 3.5.1
    zope.component =  3.5.1
    z3c.form = 2.3.3
    zope.schema = 3.6.4
    zope.proxy = 3.4.2
    plone.app.registry = 1.0b1
    plone.app.z3cform = 0.4.9
    plone.registry = 1.0b1
    plone.z3cform = 0.5.10
    zope.app.broken = 3.4.0
    zope.container = 3.7.0
    zope.security = 3.4.3
    ...

Plone 4?
--------

Plone 4 can use `plone.app.caching`__ so you don't need this product.

Troubleshooting
===============

**"Chaching not enabled. Please see the site configuration"**

  Symptom
    Every page you try to purge will give you the error
    "Chaching not enabled. Please see the site configuration"
  Problem
    You didn't configure Plone properly.
  Solution
    Go the the Plone Control Panel and configure the purging utility as described above.

**Error purging "...". Status (405)**

  Symptom
    Every page you try to purge will give you the error 'Error purging "*pageurl*". Status (405)'
  Problem
    You Varnish configuration is not proper.
  Solution
    Look at your Varnish configuration. If you have this section::
    
        acl purge {
            "localhost";
        }

    and this one::
    
        if (req.request == "PURGE") {
            if (!client.ip ~ purge) {
                error 405 "Not allowed.";
            }
            ....

    Be sure that the "*acl purge*" is the equal to the host name used to call Varnish.
    
    Take a look at the example .vcl file provided with the product.

**Error purging "...". Status (404)**

  Symptom
    Sometimes when you try to purge, you get the error 'Error purging "*pageurl*". Status (404)'
  Problem
    The page you are trying to purge is not in the Varnish cache
  Solution
    Maybe that the page isn't simply in the cache, so there is not problem.
    
    If you are sure that this page is cached, try to download the same without using a Web browser
    (for example, use *curl* or *wget*).

    __ http://en.wikipedia.org/wiki/CURL
    __ http://www.gnu.org/software/wget/ 
    
    If, after this operation, you are able to purge this page from the cache, you have a problem in
    the Varnish configuration.
    
    Web browser send to Varnish additional headers that the proxy can use for as caching key, like
    encodings, language, ...
    
    For example, if you have a section like this::
    
        if (req.http.Accept-Encoding ~ "gzip") {
            set req.hash += "gzip";
        }
        else if (req.http.Accept-Encoding ~ "deflate") {
            set req.hash += "deflate";
        }
    
    think about comment it (is not needed, of course).
    
    Take a look at the example .vcl file provided with the product.




