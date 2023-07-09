"""
rename column activated_dt
"""

from yoyo import step

__depends__ = {'20230708_01_9dRbv-add-column-activations-cnt'}

steps = [
    step(
        """
        set lock_timeout to '5s';
        ALTER TABLE promos_activations RENAME activated_dt TO created_dt;
        """
    )
]
