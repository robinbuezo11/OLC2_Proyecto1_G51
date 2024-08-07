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
                label: "Cerrar",
                id: "close",
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
        label: "Reportes",
        items: [
            {
                label: "AST",
                id: "ast",
            },
            {
                label: "Tabla de Símbolos",
                id: "symbols",
            },
            {
                label: "Errores",
                id: "errors",
            },
            {
                label: "Tokens",
                id: "tokens",
            },
            {
                label: "Manual Técnico",
                id: "tech"
            },
            {
                label: "Manual de Usuario",
                id: "user"
            },
            {
                label: "Reporte de Gramática",
                id: "grammar"
            }
        ]
    },
    {
        label: "Generar C3D",
        id: "c3d"
    },
    {
        label: "Ejecutar",
        id: "execute",
    }
];

export default TopbarItems;