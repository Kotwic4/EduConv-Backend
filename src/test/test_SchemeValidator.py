from src.models.db_models import *
from src.datasets.scheme_validator import *
import unittest

class test_api(unittest.TestCase):
    def test_conv_valid(self):
        valid_conv_layer = {"kernel_size":[3,3],"filters":30}
        args = {}
        conds = {
            'was_flatten': False,
            'was_dense': False,
            'was_conv': False,
            'was_activation': False,
            'was_pooling': False,
            'was_dropout': False,
            'was_batch_normalization': False}
        errors = SchemeValidator.validate_conv_layer(valid_conv_layer,conds)
        self.assertEqual( errors , None)
        