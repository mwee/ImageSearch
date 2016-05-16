"""empty message

Revision ID: 9a216fa5b1f4
Revises: 5056f69d2cba
Create Date: 2016-05-15 17:27:45.499777

"""

# revision identifiers, used by Alembic.
revision = '9a216fa5b1f4'
down_revision = '5056f69d2cba'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('keyword_relevance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('keyword', sa.String(), nullable=True),
    sa.Column('relevance', sa.Float(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['image.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('keyword_relevance')
    op.drop_table('image')
    ### end Alembic commands ###
