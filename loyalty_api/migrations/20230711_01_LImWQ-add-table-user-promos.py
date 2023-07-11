"""
add table user_promos
"""

from yoyo import step

__depends__ = {'20230709_02_ERJiu-add-column-updated-dt', '__init__'}

steps = [
    step(
        """
        create table if not exists user_promos (
            id uuid primary key,
            promo_id bigint not null,
            user_id uuid not null,
            created_dt timestamp with time zone default now()
        );
        """,
        """
        drop table if exists user_promos;
        """
    )
]
