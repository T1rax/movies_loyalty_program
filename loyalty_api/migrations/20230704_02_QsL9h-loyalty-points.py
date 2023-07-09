"""
add table loyalty_cards
"""

from yoyo import step

__depends__ = {'20230704_01_QteZZ-init'}

steps = [
    step(
        """
        create table if not exists loyalty_cards (
            id bigserial primary key,
            user_id uuid not null,
            loyalty_level smallint not null,
            created_dt timestamp with time zone default now(),
            updated_dt timestamp with time zone default now()
        );
        
        create table if not exists loyalty_transactions (
            id bigserial primary key,
            loyalty_id bigint not null,
            user_id uuid not null,
            points smallint not null,
            source varchar,
            created_dt timestamp with time zone default now()
        );
        """,
        """
        drop table if exists loyalty_cards;
        drop table if exists loyalty_transactions;
        """
    )
]
