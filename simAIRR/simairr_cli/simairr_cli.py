import argparse
from simAIRR.config_validator.ConfigValidator import ConfigValidator
from simAIRR.workflows.Workflows import Workflows

parser = argparse.ArgumentParser(prog='simAIRR')
parser.add_argument('-i', '--specification_path', help='path to YAML specification file describing the desired parameters',
                    required=True)
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1', help='check the version of simAIRR tool')
args = parser.parse_args()


def execute():
    config_validator = ConfigValidator(user_yaml_path=args.specification_path)
    validated_config = config_validator.execute()
    desired_workflow = Workflows(**validated_config)
    desired_workflow.execute()
