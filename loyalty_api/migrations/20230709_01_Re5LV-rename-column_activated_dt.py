"""
rename column activated_dt
"""

from yoyo import step

__depends__ = {'20230704_02_QsL9h-loyalty-points'}

steps = [
    step(
        """
        set lock_timeout to '5s';
        ALTER TABLE promos_activations RENAME activated_dt TO created_dt;
        """
    )
]
