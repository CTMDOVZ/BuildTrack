-- 1. Tabla de Proyectos
CREATE TABLE Proyectos (
    ProyectoID INTEGER PRIMARY KEY AUTOINCREMENT,
    NombreProyecto VARCHAR(100) NOT NULL,
    Ubicacion VARCHAR(100),
    Estado VARCHAR(20) DEFAULT 'En Ejecución'
);

-- 2. Tabla de Presupuestos (Límite financiero por proyecto)
CREATE TABLE Presupuestos (
    PresupuestoID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProyectoID INTEGER UNIQUE,
    MontoBase DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (ProyectoID) REFERENCES Proyectos(ProyectoID)
);

-- 3. Tabla de Proveedores (Catálogo logístico)
CREATE TABLE Proveedores (
    ProveedorID INTEGER PRIMARY KEY AUTOINCREMENT,
    NombreEmpresa VARCHAR(100) NOT NULL,
    CategoriaMaterial VARCHAR(50)
);

-- 4. Tabla de Gastos (El registro operativo en campo)
CREATE TABLE Gastos (
    GastoID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProyectoID INTEGER,
    ProveedorID INTEGER,
    Concepto VARCHAR(200) NOT NULL,
    Monto DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (ProyectoID) REFERENCES Proyectos(ProyectoID),
    FOREIGN KEY (ProveedorID) REFERENCES Proveedores(ProveedorID)
);
--ss