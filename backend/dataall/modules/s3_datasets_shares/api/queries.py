from dataall.base.api import gql
from dataall.modules.s3_datasets_shares.api.resolvers import (
    get_dataset_shared_assume_role_url,
    list_shared_tables_by_env_dataset,
    list_shared_databases_tables_with_env_group,
    get_s3_consumption_data,
)


getSharedDatasetTables = gql.QueryField(
    name='getSharedDatasetTables',
    args=[
        gql.Argument(name='datasetUri', type=gql.NonNullableType(gql.String)),
        gql.Argument(name='envUri', type=gql.NonNullableType(gql.String)),
    ],
    type=gql.ArrayType(gql.Ref('SharedDatasetTableItem')),
    resolver=list_shared_tables_by_env_dataset,
)

getDatasetSharedAssumeRoleUrl = gql.QueryField(
    name='getDatasetSharedAssumeRoleUrl',
    args=[gql.Argument(name='datasetUri', type=gql.String)],
    type=gql.String,
    resolver=get_dataset_shared_assume_role_url,
    test_scope='Dataset',
)


getS3ConsumptionData = gql.QueryField(
    name='getS3ConsumptionData',
    args=[gql.Argument(name='shareUri', type=gql.String)],
    type=gql.Ref('S3ConsumptionData'),
    resolver=get_s3_consumption_data,
)


listS3DatasetsSharedWithEnvGroup = gql.QueryField(
    name='listS3DatasetsSharedWithEnvGroup',
    resolver=list_shared_databases_tables_with_env_group,
    args=[
        gql.Argument(name='groupUri', type=gql.NonNullableType(gql.String)),
        gql.Argument(name='environmentUri', type=gql.NonNullableType(gql.String)),
    ],
    type=gql.ArrayType(gql.Ref('SharedDatabaseTableItem')),
)
