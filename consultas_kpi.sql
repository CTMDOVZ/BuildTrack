SELECT 
    p.NombreProyecto,
    b.MontoBase AS Presupuesto_Inicial,
    SUM(g.Monto) AS Gasto_Total_Real,
    (SUM(g.Monto) - b.MontoBase) AS Sobrecosto_En_Dinero,
    ROUND(((SUM(g.Monto) - b.MontoBase) * 100.0) / b.MontoBase, 2) AS Porcentaje_Sobrecosto
FROM Proyectos p
JOIN Presupuestos b ON p.ProyectoID = b.ProyectoID
JOIN Gastos g ON p.ProyectoID = g.ProyectoID
GROUP BY p.ProyectoID;
--ss