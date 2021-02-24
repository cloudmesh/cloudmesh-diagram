from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.diagram.api.manager import Manager
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE


class DiagramCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_diagram(self, args, arguments):
        """
        ::

          Usage:
                diagram --file=FILE
                diagram list

          This command does some useful things.

          Arguments:
              FILE   a file name

          Options:
              -f      specify the file

        """
        arguments.FILE = arguments['--file'] or None

        VERBOSE(arguments)


        if arguments.FILE:
            print("option a")

        elif arguments.list:
            print("option b")

        return ""
