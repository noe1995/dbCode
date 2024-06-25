{
    "table_name": "almacencalles",
    "columns": [
        {
            "name": "idalmcalle",
            "type": "INT",
            "size": 11,
            "auto_increment": true,
            "not_null": true
        },
        {
            "name": "nombrecalle",
            "type": "VARCHAR",
            "size": 10,
            "collate": "latin1_swedish_ci",
            "not_null": true
        },
        {
            "name": "almacen",
            "type": "VARCHAR",
            "size": 4,
            "collate": "latin1_swedish_ci",
            "not_null": false,
            "default": null
        },
        {
            "name": "inix",
            "type": "DOUBLE",
            "not_null": true
        },
        {
            "name": "iniy",
            "type": "DOUBLE",
            "not_null": true
        },
        {
            "name": "finx",
            "type": "DOUBLE",
            "not_null": true
        },
        {
            "name": "finy",
            "type": "DOUBLE",
            "not_null": true
        },
        {
            "name": "ladoracks",
            "type": "TINYINT",
            "size": 4,
            "not_null": true
        }
    ],
    "collate": "latin1_swedish_ci",
    "engine": "InnoDB"
}