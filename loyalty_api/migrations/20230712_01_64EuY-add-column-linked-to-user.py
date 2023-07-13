"""
add colemn linked_to_user
"""

from yoyo import step

__depends__ = {'20230711_02_dlGwt-drop-column-user-ids'}

steps = [
    step(
        """
        set lock_timeout to '5s';
        ALTER TABLE promos
        ADD COLUMN linked_to_user boolean default false
        """,
        """
        set lock_timeout to '5s';
        ALTER TABLE promos
        DROP COLUMN linked_to_user
        """,
    )
]
