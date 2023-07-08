"""
add column activations_cnt
"""

from yoyo import step

__depends__ = {'20230704_02_QsL9h-loyalty-points', '__init__'}

steps = [
    step(
        """
        set lock_timeout to '5s';
        ALTER TABLE promos_activations
        ADD COLUMN activations_cnt smallint NULL
        """,
        """
        set lock_timeout to '5s';
        ALTER TABLE promos_activations
        DROP COLUMN activations_cnt
        """,
    )
]
