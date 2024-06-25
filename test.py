import struct
import os
from tabulate import tabulate
import json

def parse_create_query(query):
    table_definition = {}
    columns = []
    
    # Parse the query to extract the table name and columns
    query_parts = query.split()
    table_name = query_parts[2]
    column_defs = query_parts[4:-1]
    
    for column_def in column_defs:
        column_parts = column_def.split()
        column_name = column_parts[0].strip('`')
        column_type = ''
        for part in column_parts[1:]:
            if part.upper() in ['INT', 'VARCHAR', 'DOUBLE', 'TINYINT']:
                column_type = part
                break
        
        # Extract the column size if it's specified
        column_size = None
        if '(' in column_type:
            column_type, column_size = column_type.split('(')
            column_size = int(column_size[:-1])
        
        # Add the column to the table definition
        columns.append({
            "name": column_name,
            "type": column_type,
            "size": column_size
        })
    
    table_definition["table_name"] = table_name
    table_definition["columns"] = columns
    
    return table_definition

def main():
    # Ruta del archivo.ibd
    data_path = os.path.join('almacencalles', 'almacencalles.ibd')

    # Ingresar el query CREATE
    query = input("Ingrese el query CREATE: ")
    table_definition = parse_create_query(query)

    # Tamaño de cada fila en bytes
    row_size = 0
    for column in table_definition["columns"]:
        if column["type"] == "INT":
            row_size += 4
        elif column["type"] == "VARCHAR":
            row_size += column["size"]
        elif column["type"] == "DOUBLE":
            row_size += 8
        elif column["type"] == "TINYINT":
            row_size += 1

    # Leer los datos del archivo.ibd
    with open(data_path, 'rb') as ibd_file:
        data = []
        while True:
            row_data = ibd_file.read(row_size)
            if not row_data:
                break
            unpacked_data = []
            offset = 0
            for column in table_definition["columns"]:
                if column["type"] == "INT":
                    unpacked_data.append(struct.unpack_from('i', row_data, offset)[0])
                    offset += 4
                elif column["type"] == "VARCHAR":
                    unpacked_data.append(struct.unpack_from(str(column["size"]) + '', row_data, offset)[0].decode('latin1').strip())
                    offset += column["size"]
                elif column["type"] == "DOUBLE":
                    unpacked_data.append(struct.unpack_from('d', row_data, offset)[0])
                    offset += 8
                elif column["type"] == "TINYINT":
                    unpacked_data.append(struct.unpack_from('b', row_data, offset)[0])
                    offset += 1
            data.append(unpacked_data)

    # Escribir los datos de la tabla en formato JSON en el archivo almacencalles.frml
    with open('almacencalles/almacencalles.frml', 'w') as f:
        json.dump(table_definition, f, indent=4)

    # Mostrar los datos en consola, ordenados por idalmcalle
    headers = [column["name"] for column in table_definition["columns"]]
    table_data = [row for row in sorted(data, key=lambda x: x[0])]
    sorted_table_data = [dict(zip(headers, row)) for row in table_data]
    sorted_table_data = sorted(sorted_table_data, key=lambda x: list(x.keys()))

    print(tabulate(sorted_table_data, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()