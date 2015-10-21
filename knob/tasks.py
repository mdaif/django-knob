from __future__ import absolute_import
from .helpers import ConnectionHandler
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

import logging


logger = logging.getLogger(__name__)


@shared_task(name='tasks.configure_batch')
def configure_batch(ip, telnet_commands, username, password, python_shell):
    logger.debug("Celery is Handling the following request, %s, %s", ip, str(telnet_commands))

    try:
        with ConnectionHandler(ip, username, password) as device:
            telnet_commands = telnet_commands.replace('\\r', '\r')
            logger.debug("executing commands: %s", telnet_commands)
            if python_shell:
                exec(telnet_commands)
            else:
                telnet_commands = telnet_commands.replace('\\r', '\r').splitlines()
                for telnet_command in telnet_commands:
                    device.execute(telnet_command)

    except Exception as e:
        logger.error(e.message)
        return False, ip, e.message
    else:
        return True, ip, None




@shared_task(name='tasks.email_admin')
def email_admin(results_pairs, email):
    logger.debug("Finished ... preparing log email")
    failed = []
    succeeded = []
    for result in results_pairs:
        if result[0]:
            succeeded.extend(["{0}".format(result[1])])
        else:
            failed.extend(["{0}: {1}".format(result[1], result[2])])

    msg = ["The following destinations succeeded:\n", "\n".join(succeeded)]
    if failed:
        msg.append("\nThe following destinations failed:\n{0}".format( "\n".join(failed)))

    send_mail('Configurations Results', "".join(msg), settings.EMAIL_SOURCE_ADDRESS, [email], fail_silently=False)
