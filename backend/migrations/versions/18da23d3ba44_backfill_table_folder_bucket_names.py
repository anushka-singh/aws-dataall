"""backfill_table_folder_bucket_names

Revision ID: 18da23d3ba44
Revises: 328e35e39e1e
Create Date: 2024-06-20 16:52:29.435802

"""

from alembic import op
from sqlalchemy import orm, Column, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from dataall.base.db import utils, Resource

Base = declarative_base()


# revision identifiers, used by Alembic.
revision = '18da23d3ba44'
down_revision = '328e35e39e1e'
branch_labels = None
depends_on = None


class S3Dataset(Resource, Base):
    __tablename__ = 's3_dataset'
    datasetUri = Column(String, ForeignKey('dataset.datasetUri'), primary_key=True)


class DatasetBucket(Resource, Base):
    __tablename__ = 'dataset_bucket'
    datasetUri = Column(String, ForeignKey('s3_dataset.datasetUri', ondelete='CASCADE'), nullable=False)
    bucketUri = Column(String, primary_key=True, default=utils.uuid('bucket'))
    S3BucketName = Column(String, nullable=False)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    try:
        bind = op.get_bind()
        session = orm.Session(bind=bind)

        print('Updating bucket names...')
        buckets: [DatasetBucket] = session.query(DatasetBucket).all()
        for bucket in buckets:
            bucket.name = bucket.S3BucketName
            session.commit()

    except Exception as e:
        print(f'Failed to init permissions due to: {e}')
        raise Exception
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
