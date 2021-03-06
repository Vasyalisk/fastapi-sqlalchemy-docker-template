"""auto

Revision ID: f23ea41bea22
Revises: 3745bac25848
Create Date: 2022-03-19 18:47:31.439064

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f23ea41bea22'
down_revision = '3745bac25848'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=True),
    sa.Column('from_email', sa.String(length=320), nullable=True),
    sa.Column('to_emails', sa.ARRAY(sa.String(length=320)), nullable=True),
    sa.Column('sent_at', sa.DateTime(), nullable=True),
    sa.Column('content_text', sa.Text(), nullable=True),
    sa.Column('content_html', sa.Text(), nullable=True),
    sa.Column('subject', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uid')
    )
    op.add_column('app_user', sa.Column('email', sa.String(length=320), nullable=False))
    op.drop_constraint('app_user_username_key', 'app_user', type_='unique')
    op.create_unique_constraint(None, 'app_user', ['email'])
    op.drop_column('app_user', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('app_user', sa.Column('username', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'app_user', type_='unique')
    op.create_unique_constraint('app_user_username_key', 'app_user', ['username'])
    op.drop_column('app_user', 'email')
    op.drop_table('mail')
    # ### end Alembic commands ###
