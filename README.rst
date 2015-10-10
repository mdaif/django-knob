=====
knob
=====

A Django reusable application that performs remote configurations on multiple devices, distributing the operations using python multiprocessing library.


Quick start
-----------

1. Add "knob" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'knob',
    )

2. Include the knob URLconf in your project urls.py like this::

    url(r'^knob/', include('knob.urls')),

3. Run `python manage.py migrate` to create the knob models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. knob requires you to add email configurations to your settings.py, make sure you at least set the variables EMAIL_BACKEND, EMAIL_HOST, and EMAIL_PORT to proper values.

6. Visit http://127.0.0.1:8000/knob/ to start the configurations.

## Current version
* supports both Telnet and SSH
* A wizard that accepts common credentials, a list of IPs, and a list of commands to be executed on every device on the list.
* Sends a log email to the system admin, indicating both the errors and success operations.
* Providing an option to use a full Python environment. That makes it easy to perform more complex operations like doing regex operations and conditional decisions on the output.

## Future work
* Accepts CSV file(s) as input.

* Better documentation :)
