import streamlit as st
import pandas as pd
import sqlite3

# Configuración de la página
st.set_page_config(page_title="BuildTrack ERP", layout="wide")

# Conectar a la base de datos que ya creamos
conn = sqlite3.connect('buildtrack.db', check_same_thread=False)

# Título del Sistema
st.title("🏗️ BuildTrack - Sistema de Gestión y Control Financiero")
st.markdown("---")

# 1. SEGURIDAD Y ROLES (Simulación de Login)
st.sidebar.header("Acceso al Sistema")
rol = st.sidebar.selectbox("Seleccione su Rol", ["Residente de Obra (Campo)", "Gerencia General (Finanzas)"])

# 2. VISTA 1: RESIDENTE DE OBRA (Registro de datos)
if rol == "Residente de Obra (Campo)":
    st.header("📝 Registro Rápido de Gastos")
    st.write("Ingrese los gastos operativos de la obra en tiempo real.")
    
    with st.form("registro_gasto"):
        # En un sistema completo esto saldría de la base de datos, aquí lo simplificamos
        proyecto = st.selectbox("Proyecto", ["Edificio Los Pinos (ID: 1)"])
        proveedor = st.selectbox("Proveedor", ["Cementos Lima S.A. (ID: 1)", "Aceros Arequipa (ID: 2)", "Logística Express (ID: 3)"])
        concepto = st.text_input("Concepto del Gasto (Ej. Compra de cemento extra)")
        monto = st.number_input("Monto del Gasto (USD)", min_value=0.0, format="%.2f")
        
        submit = st.form_submit_button("Registrar Gasto en la Base de Datos")
        
        if submit and concepto != "" and monto > 0:
            c = conn.cursor()
            # Insertamos el nuevo gasto amarrado al Proyecto 1 y al Proveedor seleccionado
            proveedor_id = int(proveedor.split("ID: ")[1].replace(")", ""))
            c.execute("INSERT INTO Gastos (ProyectoID, ProveedorID, Concepto, Monto) VALUES (1, ?, ?, ?)", (proveedor_id, concepto, monto))
            conn.commit()
            st.success(f"¡Éxito! Gasto de ${monto} registrado correctamente.")

# 3. VISTA 2: GERENCIA GENERAL (Dashboard y KPIs)
elif rol == "Gerencia General (Finanzas)":
    st.header("📊 Dashboard Financiero - Control de Sobrecostos")
    
    # Ejecutamos tu consulta SQL estrella para obtener el KPI
    query = """
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
    """
    
    df = pd.read_sql_query(query, conn)
    
    if not df.empty:
        # Extraer los datos para las tarjetas métricas
        presupuesto = df['Presupuesto_Inicial'].iloc[0]
        gasto_real = df['Gasto_Total_Real'].iloc[0]
        sobrecosto_pct = df['Porcentaje_Sobrecosto'].iloc[0]
        
        # Mostrar tarjetas (KPIs visuales)
        col1, col2, col3 = st.columns(3)
        col1.metric("Presupuesto Inicial", f"${presupuesto:,.2f}")
        col2.metric("Gasto Real Acumulado", f"${gasto_real:,.2f}")
        
        # Semáforo de alerta para el sobrecosto
        if sobrecosto_pct > 0:
            col3.metric("Sobrecosto Actual", f"{sobrecosto_pct}%", "- Alerta Roja", delta_color="inverse")
            st.error("⚠️ El proyecto ha superado el presupuesto inicial. Revise el detalle de gastos.")
        else:
            col3.metric("Margen Sano", f"{sobrecosto_pct}%", "Dentro del presupuesto")
            st.success("✅ El proyecto se mantiene dentro del presupuesto.")
            
        # Mostrar la tabla cruda extraída de tu SQL
        st.subheader("Detalle del KPI por Proyecto")
        st.dataframe(df, use_container_width=True)
# --- NUEVO BLOQUE: HISTORIAL DE TRANSACCIONES s---
        st.markdown("---")
        st.subheader("Historial Detallado de Gastos (Transacciones)")
        
        query_detalle = """
        SELECT 
            g.GastoID AS ID, 
            p.NombreProyecto AS Proyecto, 
            pr.NombreEmpresa AS Proveedor, 
            g.Concepto, 
            g.Monto
        FROM Gastos g
        JOIN Proyectos p ON g.ProyectoID = p.ProyectoID
        JOIN Proveedores pr ON g.ProveedorID = pr.ProveedorID
        ORDER BY g.GastoID DESC;
        """
        
        df_detalle = pd.read_sql_query(query_detalle, conn)
        st.dataframe(df_detalle, use_container_width=True)