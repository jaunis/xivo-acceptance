# -*- coding: UTF-8 -*-

from __future__ import absolute_import

import logging
import os.path
from loadtester.bin import commands
from loadtester.config import ScenarioConfig
from loadtester.scenario import ScenarioRunner, Scenario


def main():
    _init_logging()
    commands.execute_command(_LoadtesterCommand())


def _init_logging():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(levelname)s:%(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)


class _LoadtesterCommand(commands.AbstractCommand):
    def configure_parser(self, parser):
        parser.add_argument('-v', '--verbose', action='store_true', default=False,
                            help='increase logging verbosity')

    def configure_subcommands(self, subcommands):
        subcommands.add_subcommand(_StartSubcommand('start'))

    def pre_execute(self, parsed_args):
        self._set_logging_verbosity(parsed_args)
        self._set_scenario_runner(parsed_args)

    def _set_logging_verbosity(self, parsed_args):
        if parsed_args.verbose:
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)

    def _set_scenario_runner(self, parsed_args):
        parsed_args.scenario_runner = ScenarioRunner()


class _StartSubcommand(commands.AbstractSubcommand):
    _CONFIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../etc'))
    _CONFIG_FILE = os.path.join(_CONFIG_DIR, 'conf.py')

    def configure_parser(self, parser):
        parser.add_argument('-c', '--conf', default=self._CONFIG_FILE,
                            help='path to the config file')
        parser.add_argument('scenario_dir',
                            help='path to the scenario directory')

    def execute(self, parsed_args):
        scenario = Scenario(parsed_args.scenario_dir)
        scenario_config = ScenarioConfig.new_from_filename(parsed_args.conf)
        parsed_args.scenario_runner.start_scenario(scenario, scenario_config)


if __name__ == '__main__':
    main()
