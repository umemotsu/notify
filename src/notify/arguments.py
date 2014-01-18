# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import sys
import argparse

def split_arguments(args):
    """
    Split specified arguments to two list.

    This is used to distinguish the options of the program and
    execution command/arguments.

    Parameters
    ----------
    args : list
        Command line arguments

    Returns
    -------
    list : options, arguments
        options indicate the optional arguments for the program and
        arguments indicate the execution command/arguments
    """
    prev = False
    for i, value in enumerate(args[1:]):
        if value.startswith('-'):
            prev = True
        elif prev:
            prev = False
        else:
            return args[:i+1], args[i+1:]
    return args, []

def parse_arguments(args, config):
    """
    Parse specified arguments via config

    Parameters
    ----------
    args : list
        Command line arguments
    config : object
        ConfigParser instance which values are used as default values of
        options

    Returns
    -------
    list : arguments, options
        options indicate the return value of ArgumentParser and arguments
        indicate the execution command/arguments
    """
    from conf import config_to_options
    opts = config_to_options(config)

    usage = ("%(prog)s "
             "[-h] [-t TO_ADDR] [-f FROM_ADDR] [-e ENCODING] [-s SUBJECT]\n"
             "              "
             "[-o HOST] [-p PORT] [--username USERNAME] [--password PASSWORD]\n"
             "              "
             "[--setup] [--check] COMMAND ARGUMENTS")
    description = """
    Call COMMAND with ARGUMENTS and send notification email to TO_ADDR
    """
    epilog = "(C) 2014, hashnote.net Alisue"
    parser = argparse.ArgumentParser(
            usage=usage,
            description=description,
            epilog=epilog)
    parser.add_argument('-t', '--to-addr',
                        default=opts.to_addr,
                        help=('Destination of the email.'))
    parser.add_argument('-f', '--from-addr',
                        default=opts.from_addr,
                        help=('Source of the email.'))
    parser.add_argument('-s', '--subject',
                        default=opts.subject,
                        help=('Subject of the email'))
    parser.add_argument('-e', '--encoding',
                        default=opts.encoding,
                        help=('Encoding of the email'))
    parser.add_argument('-o', '--host',
                        default=opts.host,
                        help=('Host address of MUA'))
    parser.add_argument('-p', '--port', type=int,
                        default=opts.port,
                        help=('Port number of MUA'))
    parser.add_argument('--username',
                        default=opts.username,
                        help=('Username of the authentication'))
    parser.add_argument('--password',
                        help=('Password of the authentication'))
    parser.add_argument('--setup', default=False,
                        action='store_true',
                        help=('Setup %(prog)s configuration'))
    parser.add_argument('--check', default=False,
                        action='store_true',
                        help=('Send %(prog)s configuration via email for '
                              'checking. Only for Unix system.'))

    # display if no arguments were passed
    args = args or sys.argv
    if len(args) == 1:
        parser.print_help()
        sys.exit(0)

    # split argv to two array
    lhs, rhs = split_arguments(args)
    # parse options
    opts = parser.parse_args(args=lhs[1:])
    return rhs, opts