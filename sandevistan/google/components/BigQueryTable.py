from constructs import Construct
from cdktf_cdktf_provider_google import bigquery_table

class BigQueryTable(bigquery_table.BigqueryTable):
    def __init__(
        self, 
        scope: Construct,
        id: str,
        dataset_id: str,
        table_id: str,
        schema: dict,
        **kwargs
    ):

        if("labels" in kwargs):
            kwargs["labels"] = {"cdktf-sandevistan": scope.name, **kwargs["labels"]}
        else:
            kwargs["labels"] = {"cdktf-sandevistan": scope.name}

        table_schema_str = '['

        for field in schema:
            if field['name'] is None or \
            field['type'] is None or \
            field['mode'] is None or \
            field['description'] is None:
                raise Exception('Schema inválido. Verifique se o campo possui todos os parâmetros obrigatórios: name, type, mode e description')
            else:
                table_schema_str += '{'
                table_schema_str += '"name":"'
                table_schema_str += field['name']
                table_schema_str += '","type":"'
                table_schema_str += field['type']
                table_schema_str += '","mode":"'
                table_schema_str += field['mode']
                table_schema_str += '","description":"'
                table_schema_str += field['description']
                table_schema_str += '"},'
        table_schema_str = table_schema_str[0:-1]
        table_schema_str += ']'


        schema_str = table_schema_str

        super().__init__(scope, id, dataset_id=dataset_id, table_id=table_id, schema=schema_str, **kwargs)