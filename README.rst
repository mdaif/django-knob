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

3. knob requires you to add email configurations to your settings.py, make sure you at least set the variables EMAIL_BACKEND, EMAIL_HOST, and EMAIL_PORT to proper values.

4. Visit http://<domain>:<port>/knob/ to start the configurations.

Current Features
-----------

* Probes each IP for SSH and Telnet support and uses SSH if available, else falls back to Telnet.
* A wizard that accepts common credentials, a list of IPs, and a list of commands to be executed on every device on the list.
* Sends a log email to the system admin, indicating both the errors and success operations.
* Providing an option to use a full Python environment. That makes it easy to perform more complex operations like doing regex operations and conditional decisions on the output.

How to Use
-----------
1. Specify admin username, password and list of IP addresses then click next.

.. image:: https://cloud.githubusercontent.com/assets/2125212/10410644/854cddb6-6f48-11e5-9820-241dab264770.png
   :height: 100px
   :width: 200 px
   :scale: 50 %

2. In this step you have the option to either use a "fire and forget" approach where you throw commands to the devices without further processing, which can be useful in a case like modifying Access Control Lists (ACLs) with the same entry for a lot of devices. Here is an example of shutting down a Cisco device port.

.. image:: https://cloud.githubusercontent.com/assets/2125212/10410645/855915d6-6f48-11e5-9927-b01042c4d539.png
   :height: 100px
   :width: 200 px
   :scale: 50 %
   
3. Or, you can turn the "Full Python Shell" button on and use the power of python to process the output of the commands and take conditional actions based on some or all of the outputs. You are provided with an object called device that has a method called execute, it's how you interact with the remote device. You can use regex library, use loops, conditions, and so forth. Here is an example of changing the directory on a linux machine, and creating 10 subdirectories named using python's string interpolation.

.. image:: https://cloud.githubusercontent.com/assets/2125212/10410646/8589616e-6f48-11e5-9eaa-7da8c354c691.png
   :height: 100px
   :width: 200 px
   :scale: 50 %

4. Specify an email in order to send a log with all the succeeded and failed destinations along with the failure reason.

.. image:: https://cloud.githubusercontent.com/assets/2125212/10410647/85c4d4f6-6f48-11e5-8c92-adfebdba4920.png
   :height: 100px
   :width: 200 px
   :scale: 50 %

5. Confirm and wait for the log email.

.. image:: https://cloud.githubusercontent.com/assets/2125212/10410648/85c6fff6-6f48-11e5-9401-986bb135df3f.png
   :height: 100px
   :width: 200 px
   :scale: 50 %
   
Future work
-----------
* Ability to provide external files as input.
* Ability to log custom output from remote operations.
