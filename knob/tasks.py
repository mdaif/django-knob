from .helpers import ConnectionHandler
from django.core.mail import send_mail
from django.conf import settings
import multiprocessing
import logging


def configure_batch(args):
    ips, telnet_commands, username, password, python_shell = args
    print multiprocessing.current_process()
    results = []
    for ip in ips:
        try:
            with ConnectionHandler(ip, username, password) as device:
                if python_shell:
                    commands = telnet_commands.replace('\\r', '\r')
                    exec(commands)
                else:
                    telnet_commands = telnet_commands.replace('\\r', '\r').splitlines()
                    for telnet_command in telnet_commands:
                        device.execute(telnet_command)

        except Exception as e:
                results.append((False, ip, e.message))
        else:
            results.append((True, ip, None))

    return results


def email_admin(results_pairs):
    email = email_admin.email  # again .. I know .. sorry :(
    failed = []
    succeeded = []
    for pairs in results_pairs:
        failed.extend(["{0}: {1}".format(pair[1], pair[2]) for pair in pairs if not pair[0]])
        succeeded.extend(["{0}".format(pair[1]) for pair in pairs if pair[0]])
    msg = ["The following destinations succeeded:\n", "\n".join(succeeded)]
    if failed:
        msg.append("\nThe following destinations failed:\n{0}".format( "\n".join(failed)))

    send_mail('Configurations Results', "".join(msg), settings.EMAIL_SOURCE_ADDRESS, [email], fail_silently=False)
    email_admin.pool.close()
