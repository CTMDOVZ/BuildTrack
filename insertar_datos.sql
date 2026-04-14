-- proyecto base
INSERT INTO Proyectos (NombreProyecto, Ubicacion) 
VALUES ('Edificio Los Pinos', 'Miraflores - Lima');

-- presupuesto inicial de $100,000
INSERT INTO Presupuestos (ProyectoID, MontoBase) 
VALUES (1, 100000.00);

-- proveedoress
INSERT INTO Proveedores (NombreEmpresa, CategoriaMaterial) 
VALUES ('Cementos Lima S.A.', 'Cemento y Concreto'),
       ('Aceros Arequipa', 'Acero Estructural'),
       ('Logística Express', 'Transporte y Fletes');

INSERT INTO Gastos (ProyectoID, ProveedorID, Concepto, Monto) 
VALUES (1, 1, 'Compra inicial de cemento', 40000.00),
       (1, 2, 'Estructuras de acero', 50000.00),
       (1, 1, 'Compra de urgencia por pérdida de material en obra', 15000.00),
       (1, 3, 'Flete adicional por retraso', 13000.00);