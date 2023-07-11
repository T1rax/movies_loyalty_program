"""
add clumn updated_dt
"""

from yoyo import step

__depends__ = {'20230709_01_Re5LV-rename-column_activated_dt'}

steps = [
    step(
        """
        set lock_timeout to '5s';
        ALTER TABLE promos_activations
        ADD COLUMN updated_dt timestamp with time zone default now()
        """,
        """
        set lock_timeout to '5s';
        ALTER TABLE promos_activations
        DROP COLUMN updated_dt
        """,
    )
]
