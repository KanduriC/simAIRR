import pandas as pd


class GeneValidator:
    def __init__(self):
        self.valid_genes = {
            'humanTRA': {
                'valid_v_genes': ['TRAV9-2','TRAV9-2','TRAV9-2','TRAV9-1','TRAV8-7','TRAV26-1','TRAV25','TRAV13-2','TRAV26-1','TRAV12-2','TRAV23','TRAV24','TRAV4','TRAV20','TRAV16','TRAV8-6','TRAV20','TRAV8-4','TRAV18','TRAV17','TRAV12-2','TRAV12-1','TRAV21','TRAV1-2','TRAV24','TRAV10','TRAV1-2','TRAV8-4','TRAV36','TRAV19','TRAV14','TRAV11','TRAV5','TRAV23','TRAV38-1','TRAV2','TRAV13-2','TRAV1-1','TRAV22','TRAV6','TRAV14','TRAV8-1','TRAV20','TRAV21','TRAV23','TRAV12-1','TRAV38-1','TRAV41','TRAV6','TRAV2','TRAV8-2','TRAV8-4','TRAV12-3','TRAV13-1','TRAV38-2','TRAV8-6','TRAV14','TRAV12-3','TRAV13-1','TRAV29','TRAV13-1','TRAV40','TRAV26-2','TRAV14','TRAV9-2','TRAV26-2','TRAV27','TRAV8-3','TRAV27','TRAV1-1','TRAV12-2','TRAV27','TRAV29','TRAV23','TRAV8-3','TRAV30','TRAV30','TRAV30','TRAV34','TRAV35','TRAV35','TRAV26-1','TRAV36','TRAV20','TRAV36','TRAV36','TRAV38-1','TRAV38-1','TRAV39','TRAV6','TRAV8-4','TRAV6','TRAV6','TRAV6','TRAV7','TRAV8-1','TRAV30','TRAV8-2','TRAV8-4','TRAV8-3','TRAV8-4','TRAV3','TRAV8-4'],
                'valid_j_genes': ['TRAJ9','TRAJ8','TRAJ7','TRAJ61','TRAJ60','TRAJ58','TRAJ57','TRAJ56','TRAJ55','TRAJ54','TRAJ52','TRAJ50','TRAJ48','TRAJ24','TRAJ25','TRAJ23','TRAJ18','TRAJ13','TRAJ6','TRAJ49','TRAJ19','TRAJ51','TRAJ22','TRAJ12','TRAJ20','TRAJ13','TRAJ24','TRAJ11','TRAJ15','TRAJ14','TRAJ2','TRAJ23','TRAJ15','TRAJ47','TRAJ30','TRAJ21','TRAJ53','TRAJ1','TRAJ16','TRAJ26','TRAJ28','TRAJ36','TRAJ41','TRAJ27','TRAJ29','TRAJ37','TRAJ3','TRAJ59','TRAJ31','TRAJ32','TRAJ39','TRAJ47','TRAJ17','TRAJ43','TRAJ33','TRAJ10','TRAJ37','TRAJ34','TRAJ45','TRAJ38','TRAJ5','TRAJ4','TRAJ40','TRAJ35','TRAJ42','TRAJ46','TRAJ32','TRAJ44'],
            },
            'humanTRB': {
                'valid_v_genes': ['TRBV12', 'TRBV6', 'TRBV7', 'TRBV11', 'TRBV25', 'TRBV5', 'TRBV3-1','TRBV17','TRBV18','TRBV16','TRBV29-1','TRBV7-9','TRBV15','TRBV25-1','TRBV11-2','TRBV14','TRBV23-1','TRBV12-2','TRBV30','TRBV10-3','TRBV15','TRBV20-1','TRBV6-7','TRBV12-5','TRBV30','TRBV6-6','TRBV4-1','TRBV26','TRBV2','TRBV5-7','TRBV4-2','TRBV7-3','TRBV12-4','TRBV5-8','TRBV6-2','TRBV5-4','TRBV7-9','TRBV6-1','TRBV6-3','TRBV9','TRBV7-6','TRBV7-7','TRBV7-2','TRBV10-1','TRBV7-7','TRBV7-9','TRBV3-2','TRBV24-1','TRBV6-4','TRBV7-8','TRBV11-1','TRBV15','TRBV3-1','TRBV7-1','TRBV6-6','TRBV7-3','TRBV12-1','TRBV7-2','TRBV10-2','TRBV7-9','TRBV7-2','TRBV4-3','TRBV5-3','TRBV5-5','TRBV7-9','TRBV7-2','TRBV28','TRBV27','TRBV5-3','TRBV6-8','TRBV30','TRBV6-5','TRBV19','TRBV2','TRBV10-3','TRBV13','TRBV29-1','TRBV10-1','TRBV5-6','TRBV11-3','TRBV6-9','TRBV1','TRBV3-2','TRBV7-8','TRBV12-4','TRBV11-2','TRBV10-1','TRBV7-4','TRBV12-3','TRBV5-4','TRBV11-2','TRBV7-3','TRBV5-1','TRBV4-3','TRBV7-3'],
                'valid_j_genes': ['TRBJ1-6','TRBJ1-6','TRBJ2-7','TRBJ1-2','TRBJ2-2','TRBJ2-5','TRBJ1-5','TRBJ2-4','TRBJ1-1','TRBJ2-7','TRBJ1-4','TRBJ1-3','TRBJ2-3','TRBJ2-6','TRBJ2-1'],
            },
            'humanIGH': {
                'valid_v_genes': ['IGHV7-81','IGHV1-2','IGHV3-30-3','IGHV3-69-1','IGHV3-38-3','IGHV3-30-2','IGHV3-30-3','IGHV3-29','IGHV3-25','IGHV3-23','IGHV3-21','IGHV3-53','IGHV3-15','IGHV3-19','IGHV3-33-2','IGHV3-52','IGHV3-13','IGHV4-39','IGHV3-11','IGHV3-49','IGHV4-59','IGHV4-55','IGHV1-69-2','IGHV1-58','IGHV3-38','IGHV4-59','IGHV5-51','IGHV1-8','IGHV3-53','IGHV1-8','IGHV4-30-4','IGHV1-38-4','IGHV1-3','IGHV7-4-1','IGHV1-2','IGHV2-70','IGHV3-16','IGHV1-45','IGHV3-22','IGHV1-69','IGHV3-20','IGHV3-64','IGHV1-18','IGHV3-43','IGHV5-78','IGHV2-5','IGHV3-33','IGHV3-73','IGHV3-7','IGHV3-63','IGHV3-33-2','IGHV1-46','IGHV7-4-1','IGHV6-1','IGHV3-32','IGHV3-9','IGHV1-68','IGHV2-10','IGHV3-32','IGHV3-21','IGHV2-26','IGHV1-69','IGHV3-33','IGHV3-NL1','IGHV3-35','IGHV3-38','IGHV3-43D','IGHV3-30','IGHV3-47','IGHV3-47','IGHV3-48','IGHV1-NL1','IGHV3-7','IGHV3-54','IGHV4-38-2','IGHV3-62','IGHV5-78','IGHV7-34-1','IGHV3-66','IGHV3-69-1','IGHV3-71','IGHV4-31','IGHV3-29','IGHV3-71','IGHV4-31','IGHV3-72','IGHV3-74','IGHV4-30-2','IGHV4-28','IGHV4-34','IGHV4-30-4','IGHV1-24','IGHV4-38-2','IGHV4-4','IGHV4-61','IGHV5-10-1','IGHV7-34-1'],
                'valid_j_genes': ['IGHJ6','IGHJ6','IGHJ5','IGHJ4','IGHJ3','IGHJ2','IGHJ1'],
            },
            'mouseTRB': {
                'valid_v_genes': ['TRBV6','TRBV13-1','TRBV4','TRBV5','TRBV22','TRBV27','TRBV14','TRBV15','TRBV24','TRBV26','TRBV20','TRBV23','TRBV7','TRBV9','TRBV3','TRBV12-2','TRBV1','TRBV2','TRBV31','TRBV8','TRBV28','TRBV19','TRBV13-3','TRBV12-1','TRBV10','TRBV12-3','TRBV16','TRBV18','TRBV11','TRBV17','TRBV29','TRBV25','TRBV21','TRBV13-2','TRBV30'],
                'valid_j_genes': ['TRBJ1-5','TRBJ2-4','TRBJ1-1','TRBJ2-7','TRBJ1-7','TRBJ2-1','TRBJ2-6','TRBJ2-3','TRBJ1-4','TRBJ1-3','TRBJ1-2','TRBJ2-5','TRBJ2-2','TRBJ1-6'],
            },
        }

    def validate_background_sequences(self, background_sequences, model):
        if model not in self.valid_genes:
            raise ValueError(f"Invalid model '{model}'. Supported models are: {', '.join(self.valid_genes.keys())}")

        valid_v_genes = set(self.valid_genes[model]['valid_v_genes'])
        valid_j_genes = set(self.valid_genes[model]['valid_j_genes'])

        valid_background_sequences = background_sequences[
            (background_sequences.iloc[:, 2].isin(valid_v_genes)) &
            (background_sequences.iloc[:, 3].isin(valid_j_genes))
            ]
        valid_background_sequences = valid_background_sequences.reset_index(drop=True)
        return valid_background_sequences
