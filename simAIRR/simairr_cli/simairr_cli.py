import argparse
import logging
import os.path
import sys
from simAIRR.config_validator.ConfigValidator import ConfigValidator
from simAIRR.util.utilities import makedir_if_not_exists
from simAIRR.workflows.Workflows import Workflows

parser = argparse.ArgumentParser(prog='simAIRR')
parser.add_argument('-i', '--specification_path', help='path to YAML specification file describing the desired '
                                                       'parameters', required=True)
parser.add_argument('-q', '--quiet', required=False, action='store_true', help='whether to turn on quiet mode '
                                                                               '(no logs printed to the screen)')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1', help='check the version of simAIRR '
                                                                                      'tool')
args = parser.parse_args()


def execute():
    config_validator = ConfigValidator(user_yaml_path=args.specification_path)
    validated_config = config_validator.execute()
    makedir_if_not_exists(validated_config.get('output_path'), fail_if_exists=True)
    _initialize_logging()
    logging.info('Validation of user-supplied parameter specification completed.')
    desired_workflow = Workflows(**validated_config)
    desired_workflow.execute()
    logging.info('simAIRR workflow execution completed.')


def _initialize_logging():
    log_format = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=logging.DEBUG,
                        filename=os.path.join(validated_config.get('output_path'), "log.txt"), filemode='a')
    if args.quiet is False:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(log_format)
        logging.getLogger().addHandler(stdout_handler)

# if __name__ == '__main__':
#     val_config = ConfigValidator(user_yaml_path='/Users/kanduric/Desktop/simairr_gliph_seq_assessment.yaml').execute()
#     makedir_if_not_exists(val_config.get('output_path'), fail_if_exists=True)
#     logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=logging.DEBUG,
#                         filename=os.path.join(val_config.get('output_path'), "log.txt"), filemode='a')
#     logging.info('Validation of user-supplied parameter specification completed.')
#     des_workflow = Workflows(**val_config)
#     des_workflow.execute()
#     logging.info('simAIRR workflow execution completed.')

# val_config = ConfigValidator(user_yaml_path='/Users/kanduric/Desktop/simairr_config.yaml').execute()
# makedir_if_not_exists(val_config.get('output_path'), fail_if_exists=True)
# logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=logging.DEBUG,
#                     filename=os.path.join(val_config.get('output_path'), "log.txt"), filemode='a')
# logging.info('Validation of user-supplied parameter specification completed.')
# des_workflow = Workflows(**val_config)
# des_workflow.execute()
# logging.info('simAIRR workflow execution completed.')
