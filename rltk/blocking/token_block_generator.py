from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from rltk.dataset import Dataset
from rltk.blocking.block_generator import BlockGenerator
from rltk.blocking.block import Block
from rltk.blocking.block_black_list import BlockBlackList


class TokenBlockGenerator(BlockGenerator):
    """
    Token block generator. The return for :meth:`block` should be a `list` or `set`.
    """

    def block(self, dataset, function_: Callable = None, property_: str = None,
              block: Block = None, block_black_list: BlockBlackList = None):
        """
        The return of `property_` or `function_` should be list or set.
        """
        block = super()._block_args_check(function_, property_, block)
        for r in dataset:
            value = function_(r) if function_ else getattr(r, property_)
            if not isinstance(value, list) and not isinstance(value, set):
                raise ValueError('Return of the function or property should be a list')
            for v in value:
                if block_black_list and block_black_list.has(v):
                    continue
                if not isinstance(v, str):
                    raise ValueError('Elements in return list should be string')
                block.add(v, dataset.id, r.id)
                if block_black_list:
                    block_black_list.add(v, block)
        return block

    def generate(self, block1: Block, block2: Block, output_block: Block = None):
        output_block = super()._generate_args_check(output_block)
        for block_id, ds_id, record_id in block1:
                output_block.add(block_id, ds_id, record_id)
        for block_id, ds_id, record_id in block2:
                output_block.add(block_id, ds_id, record_id)
        return output_block
