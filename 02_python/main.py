import argparse
import logging
from utils.command_handler import CommandHandler
from utils.command_parser import CommandParser

# TODO 1-1: Use argparse to parse the command line arguments (verbose and log_file).
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true", help="Weather to print verbose. Default is false.", default=False)
parser.add_argument("-l", "--log_path", type=str, help="The path of log file. Default is file_explorer.log", default="file_explorer.log")
args = parser.parse_args()

# TODO 1-2: Set up logging and initialize the logger object.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

info_handler = logging.FileHandler(args.log_path)
info_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
info_handler.setFormatter(formatter)

logger.addHandler(info_handler)

command_parser = CommandParser(args.verbose)
handler = CommandHandler(command_parser)

while True:
    command = input(">> ")
    logger.info(f"Input command: {command}")
    handler.execute(command)