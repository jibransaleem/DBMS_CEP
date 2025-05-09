"""Updated job_status enum and job_deadline field

Revision ID: 7c911b98e8fe
Revises: 
Create Date: 2025-04-13 03:09:48.486309

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7c911b98e8fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('jobposts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('job_deadline', sa.Date(), nullable=False))
        batch_op.add_column(sa.Column('job_status', sa.Enum('open', 'closed'), nullable=False))
        batch_op.alter_column('job_description',
               existing_type=mysql.VARCHAR(length=200),
               type_=sa.String(length=300),
               existing_nullable=False)
        batch_op.alter_column('job_qualification',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=300),
               existing_nullable=False)
        batch_op.alter_column('job_location',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('jobposts', schema=None) as batch_op:
        batch_op.alter_column('job_location',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=False)
        batch_op.alter_column('job_qualification',
               existing_type=sa.String(length=300),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('job_description',
               existing_type=sa.String(length=300),
               type_=mysql.VARCHAR(length=200),
               existing_nullable=False)
        batch_op.drop_column('job_status')
        batch_op.drop_column('job_deadline')

    # ### end Alembic commands ###
