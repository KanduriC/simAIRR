import sys
import yaml
from simAIRR.util.utilities import merge_dicts
from simAIRR.workflows.Workflows import Workflows


class ConfigValidator:

    default_config_dict = {'mode': None, 'olga_model', 'output_path', 'n_sequences', 'n_repertoires', 'n_threads', 'seed',
                 'public_seq_proportion', 'public_seq_pgen_count_mapping_file', 'signal_pgen_count_mapping_file',
                 'signal_sequences_file', 'positive_label_rate', 'phenotype_burden', 'phenotype_pool_size'}

    def __init__(self, user_yaml_path):
        """
        1. type checking
        2. allowed values
        3. required
        :param user_yaml_path:
        """
        self.user_yaml_path = user_yaml_path

    def _parse_user_yaml(self):
        with open(self.user_yaml_path, "r") as yaml_file:
            try:
                yaml_obj = yaml.load(yaml_file, Loader=yaml.FullLoader)
                assert yaml_obj is not None, "The supplied yaml file," + self.user_yaml_path + ", is empty"
            except Exception as e:
                print(
                    "Error: that looks like an invalid yaml file. Consider validating your yaml file using one of the "
                    "online yaml validators; for instance: https://jsonformatter.org/yaml-validator")
                print("Exception: %s" % str(e))
                sys.exit(1)
        return yaml_obj

    def _validate_user_config(self, config_obj):
        assert config_obj['mode'] is not None, f"Error: argument 'mode' is required"
        self._schema_validator(schema_dict=self._get_mode_specific_schema_dict(mode=config_obj['mode']),
                               document_dict=config_obj)

    def _get_mode_specific_default_params_dict(self, mode):
        mode_agnostic_dict = {}
        baseline_dict = {}
        public_component_dict = {}
        signal_implant_dict = {}
        signal_feasibility_dict ={}
        mode_specific_dicts = {"baseline_repertoire_generation": merge_dicts(mode_agnostic_dict, baseline_dict),
        "public_component_correction": merge_dicts(mode_agnostic_dict, public_component_dict),
        "signal_implantation": merge_dicts(mode_agnostic_dict, signal_implant_dict),
        "signal_feasibility_assessment": merge_dicts(mode_agnostic_dict, signal_feasibility_dict)}
        return mode_specific_dicts[mode]

    def _get_mode_specific_schema_dict(self, mode):
        mode_agnostic_dict = {}
        baseline_dict = {}
        public_component_dict = {}
        signal_implant_dict = {}
        signal_feasibility_dict ={}
        mode_specific_dicts = {"baseline_repertoire_generation": merge_dicts(mode_agnostic_dict, baseline_dict),
        "public_component_correction": merge_dicts(mode_agnostic_dict, public_component_dict),
        "signal_implantation": merge_dicts(mode_agnostic_dict, signal_implant_dict),
        "signal_feasibility_assessment": merge_dicts(mode_agnostic_dict, signal_feasibility_dict)}
        return mode_specific_dicts[mode]

    def _update_user_config(self, mode, config_obj):
        updated_config_obj = self._get_mode_specific_default_params_dict.update(config_obj)
        return updated_config_obj

    def _schema_validator(self, schema_dict, document_dict):
        for key in schema_dict.keys():
            assert isinstance(document_dict[key], schema_dict[key]['type'])
            if schema_dict[key]['required']:
                assert document_dict[key] is not None, f"Error: argument {key} is required"
            assert document_dict[key] in schema_dict[key]['allowed'], f"Error: invalid value supplied for argument {key}"

    def execute(self):
        usr_yaml = self._parse_user_yaml()
        self._validate_user_config(self, usr_yaml)
        updated_config = self._update_user_config(usr_yaml['mode'], usr_yaml)
        return updated_config


