"""
loyalty_points
"""

from yoyo import step

__depends__ = {'20230704_01_QteZZ-init'}

steps = [
    step(
        """
        create table if not exists loyalty_account (
            id bigserial primary key,
            user_id uuid not null,
            loyalty_level varchar(10) not null,
            creation_dt timestamp with time zone default now(),
            update_dt timestamp with time zone default now()
        );
        
        create table if not exists loyalty_transactions (
            id bigserial primary key,
            loyalty_id bigserial not null,
            user_id uuid not null,
            points smallint not null,
            source varchar,
            transaction_dt timestamp with time zone default now()
        );
        """,
        """
        drop table if exists loyalty_account;
        drop table if exists loyalty_transactions;
        """
    )
]
