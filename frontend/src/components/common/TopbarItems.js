const TopbarItems = [
    {
        label: "Archivo",
        items: [
            {
                label: "Nuevo",
                id: "new",
            },
            {
                label: "Abrir",
                id: "open",
            },
            {
                label: "Guardar",
                id: "save",
            },
            {
                label: "Guardar como",
                id: "saveAs",
            },
            {
                label: "Cerrar",
                id: "close",
            },
            {
                label: "Salir",
                id: "exit",
            }
        ]
    },
    {
        label: "Herramientas",
        items: [
            {
                label: "Base de datos",
                items: [
                    {
                        label: "Crear base de datos",
                        id: "createDB",
                    },
                    {
                        label: "Eliminar base de datos",
                        id: "dropDB",
                    },
                    {
                        label: "Crear DUMP",
                        id: "createDump",
                    },
                    {
                        label: "Seleccionar base de datos",
                        id: "selectDB",
                    }
                ]
            },
            {
                label: "SQL",
                items: [
                    {
                        label: "Nuevo Query",
                        id: "newQuery",
                    },
                    {
                        label: "Ejecutar Query",
                        id: "executeQuery",
                    }
                ]
            },
            {
                label: "Exportar",
                id: "export",
            },
            {
                label: "Importar",
                id: "import",
            }
        ]
    },
    {
        label: "Ejecutar",
        id: "execute",
    }
];

export default TopbarItems;