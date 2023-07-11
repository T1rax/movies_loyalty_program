"""
drop column user_ids
"""

from yoyo import step

__depends__ = {'20230711_01_LImWQ-add-table-user-promos'}

steps = [
    step(
        """
        ALTER TABLE promos 
        DROP COLUMN user_ids;
        """
    )
]
