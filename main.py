import numpy as np
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🔍 Ejercicio 3.24 – Momento de una Fuerza 3D con Visualización y Análisis")

# Sidebar – Parámetros editables

st.sidebar.header("UVG CAMPUS SUR")
st.sidebar.header("📏 Parámetros del sistema")
altura_y = st.sidebar.number_input("Altura del techo (y)", value=90)
ancho_x = st.sidebar.number_input("Ancho del puntal (x)", value=5)
profundidad_AD = st.sidebar.number_input("Distancia AD (z)", value=36)
altura_AD = st.sidebar.number_input("Distancia AD (y)", value=6)
dist_BD_z = st.sidebar.number_input("Distancia BD (z)", value=66)
dist_DC_x = st.sidebar.number_input("Distancia DC (x)", value=48)
fuerza_magnitud = st.sidebar.number_input("Fuerza aplicada (lb)", value=57.0)

st.sidebar.text("Esteban Rivas – 23703 \nClaudia Gómez – 23701 \nEduar Hidalgo – 231473 \nNoé Ramírez – 231626")

# Enunciado dinámico
st.markdown(f"""
> **Ejercicio 3.24**  
> El puntal de madera **AB** se emplea temporalmente para sostener el techo en voladizo.  
> Si el puntal ejerce en **A** una fuerza de **{fuerza_magnitud:.1f} lb** dirigida a lo largo de **BA**, determine el momento de esta fuerza respecto al punto **C**.
""")

# Puntos en el espacio (B es el origen)
A = np.array([-ancho_x, altura_y, - (dist_BD_z - profundidad_AD)])
B = np.array([0, 0, 0])
D = np.array([-ancho_x, (altura_y + altura_AD), -dist_BD_z])
C = np.array([-(dist_DC_x + ancho_x), (altura_y + altura_AD), -dist_BD_z])

# Cálculos
vec_BA = A - B
u_BA = vec_BA / np.linalg.norm(vec_BA)
F_vec = fuerza_magnitud * u_BA
r_CA = A - C
M_C = np.cross(r_CA, F_vec)

# Paso a paso explicativo
st.subheader("🧮 Paso a paso del cálculo")

st.markdown("**1. Vector dirección del puntal** $\\vec{BA}$:")
st.latex(r"\vec{BA} = \begin{bmatrix} %d \\ %d \\ %d \end{bmatrix}" % tuple(vec_BA))

st.markdown("**2. Vector unitario en dirección de la fuerza:**")
st.latex(r"\hat{u}_{BA} = \frac{\vec{BA}}{|\vec{BA}|} = \begin{bmatrix} %.3f \\ %.3f \\ %.3f \end{bmatrix}" % tuple(u_BA))

st.markdown(f"**3. Vector de fuerza aplicada en A:** $\\vec{{F}} = {fuerza_magnitud:.1f} \\cdot \hat{{u}}_{{BA}}$")
st.latex(r"\vec{F} = \begin{bmatrix} %.2f \\ %.2f \\ %.2f \end{bmatrix} \; \text{lb}" % tuple(F_vec))

st.markdown("**4. Vector de posición desde C hasta A:**")
st.latex(r"\vec{r}_{CA} = \vec{A} - \vec{C} = \begin{bmatrix} %d \\ %d \\ %d \end{bmatrix}" % tuple(r_CA))

st.markdown("**5. Momento de la fuerza alrededor de C:**")
st.latex(r"\vec{M}_C = \vec{r}_{CA} \times \vec{F} = \begin{bmatrix} %.2f \\ %.2f \\ %.2f \end{bmatrix} \; \text{lb} \cdot \text{in}" % tuple(M_C))

# Visualización 3D
fig = go.Figure()

# Puntos
for label, point in zip(['A', 'B', 'C', 'D'], [A, B, C, D]):
    fig.add_trace(go.Scatter3d(
        x=[point[0]], y=[point[1]], z=[point[2]],
        mode='markers+text',
        text=[label], textposition="top center",
        marker=dict(size=6, color="skyblue"), name=label
    ))

# Líneas estructurales
def draw_line(p1, p2, name, color="black", dash=None):
    fig.add_trace(go.Scatter3d(
        x=[p1[0], p2[0]], y=[p1[1], p2[1]], z=[p1[2], p2[2]],
        mode="lines",
        line=dict(color=color, width=4, dash=dash),
        name=name
    ))

draw_line(B, A, "Puntal AB", "blue")
draw_line(A, D, "AD", "gray")
draw_line(D, C, "DC", "gray")
draw_line(A, C, "r_CA", "green", dash="dash")

# Flecha de fuerza
end_arrow = A + u_BA * 20
fig.add_trace(go.Scatter3d(
    x=[A[0], end_arrow[0]], y=[A[1], end_arrow[1]], z=[A[2], end_arrow[2]],
    mode="lines",
    line=dict(color="red", width=6),
    name="Fuerza aplicada"
))
fig.add_trace(go.Cone(
    x=[end_arrow[0] * 1.03], y=[end_arrow[1] * 1.03], z=[end_arrow[2] * 1.03],
    u=[u_BA[0]], v=[u_BA[1]], w=[u_BA[2]],
    sizemode="absolute", sizeref=5,
    anchor="tip", colorscale="Reds", showscale=False
))

fig.update_layout(
    scene=dict(
        xaxis_title="X (in)", yaxis_title="Y (in)", zaxis_title="Z (in)",
        aspectmode="cube"
    ),
    title="📐 Visualización 3D del sistema",
    margin=dict(l=0, r=0, t=30, b=0)
)

col1, col2 = st.columns([1, 1.5])

with col1:
    st.image("3.24.png", caption="Sistema de soporte – Ejercicio 3.24", width=300)

with col2:
    st.plotly_chart(fig, use_container_width=True)

st.subheader("📌 Resultado final del momento respecto a C")

magnitud_Mc = np.linalg.norm(M_C)
direccion = []

if M_C[0] > 0: direccion.append("eje X (positivo)")
elif M_C[0] < 0: direccion.append("eje X (negativo)")

if M_C[1] > 0: direccion.append("eje Y (positivo)")
elif M_C[1] < 0: direccion.append("eje Y (negativo)")

if M_C[2] > 0: direccion.append("eje Z (positivo)")
elif M_C[2] < 0: direccion.append("eje Z (negativo)")

direccion_texto = ", ".join(direccion)

st.markdown(f"""
**🔹 El momento total respecto al punto C tiene una magnitud de:**  
$$
\\left\\| \\vec{{M}}_C \\right\\| = {magnitud_Mc:.2f} \\, \\text{{lb}} \\cdot \\text{{in}}
$$

**🔹 Dirección aproximada:** {direccion_texto}  
Esto indica que la tendencia rotacional generada por la fuerza aplicada intenta hacer girar la estructura en las direcciones mencionadas alrededor del punto C.

---
""")
