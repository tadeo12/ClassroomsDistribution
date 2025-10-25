
import io
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def initializeGraphsPanel():
    if "progressBar" not in st.session_state:
        st.session_state.progressBar = st.progress(0, text="Iniciando...")
        
    if "graphRows" not in st.session_state:
        st.session_state.graphRows = []
        num_rows =  8
        for _ in range(num_rows):
            row = st.container()
            col1, col2 = row.columns(2)
            st.session_state.graphRows.append((col1.empty(), col2.empty()))

    if "statsHistory" not in st.session_state:
        st.session_state.statsHistory = []

def plotLine(df, x_col, y_cols, title, xlabel, ylabel, labels=None, colors=None):
    """Genera un fig, ax con líneas de un DataFrame."""
    fig, ax = plt.subplots()
    for i, y_col in enumerate(y_cols):
        lbl = labels[i] if labels else y_col
        color = colors[i] if colors else None
        ax.plot(df[x_col], df[y_col], label=lbl, color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if labels:
        ax.legend()
    return fig, ax

def save_fig(fig):
    """Convierte un fig en un buffer PNG listo para PDF."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf
from ConfigManager import ConfigManager

def updateProgress(newStats, solution):
    # actualizar barra de progreso
    p = newStats["progressPercent"]
    cost = newStats["bestCost"]
    st.session_state.progressBar.progress(p, text=f"Progreso: {p}%  Mejor penalización: {cost}")

    # detectar tipo de evaluación
    penalty_mode = ConfigManager().getConfig().get("penalty_function", "fwp")
    match penalty_mode:
        case "sum":
            penalty_label = "Penalización (suma simple)"
        case "fwp":
            penalty_label = "Penalización ponderada"
        case "norm":
            penalty_label = "Penalización normalizada"
        case "happy_norm":
            penalty_label = "Penalización normalizada (feliz)"
        case _:
            penalty_label = "Penalización"

    # expandir constraints (soporta estructura nueva o vieja)
    expanded_stats = newStats.copy()

    def expand_constraint_dict(prefix, constraint_dict):
        expanded = {}
        for k, v in constraint_dict.items():
            if isinstance(v, dict):
                # si es del formato {"raw":..,"max":..,"normalized":..,"weighted":..}
                # tomamos el valor más representativo (weighted o normalized)
                value = (
                    v.get("weighted")
                    if "weighted" in v
                    else v.get("normalized", v.get("raw"))
                )
            else:
                value = v
            expanded[f"{prefix}_{k}"] = value
        return expanded

    expanded_stats.update(expand_constraint_dict("current", newStats.get("currentCostsByConstraint", {})))
    expanded_stats.update(expand_constraint_dict("best", newStats.get("bestCostsByConstraint", {})))

    st.session_state.statsHistory.append(expanded_stats)

    df = pd.DataFrame(st.session_state.statsHistory)

    # fila 1
    fig, ax = plotLine(df, "iteration", ["bestCost", "currentCost"], "Costos", "Iteración", "Valor",
                       labels=["Mejor costo", "Costo actual"], colors=["blue", "orange"])
    st.session_state.graphRows[0][0].pyplot(fig)
    plt.close(fig)

    fig, ax = plotLine(df, "iteration", ["temperature"], "Temperatura", "Iteración", "Valor")
    st.session_state.graphRows[0][1].pyplot(fig)
    plt.close(fig)

    # fila 2
    fig, ax = plotLine(df, "iteration", ["iterationsWithoutImprove"], "Iteraciones sin mejorar", "Iteración", "Cantidad")
    st.session_state.graphRows[1][0].pyplot(fig)
    plt.close(fig)

    fig, ax = plotLine(df, "iteration", ["iterationsWithoutChanges"], "Iteraciones sin cambiar", "Iteración", "Cantidad")
    st.session_state.graphRows[1][1].pyplot(fig)
    plt.close(fig)

    # fila 3
    fig, ax = plotLine(df, "iteration", ["maxWithoutImproveInterval"], "Máximo sin mejorar (intervalo)", "Iteración", "Cantidad")
    st.session_state.graphRows[2][0].pyplot(fig)
    plt.close(fig)

    fig, ax = plotLine(df, "iteration", ["maxWithoutChangesInterval"], "Máximo sin cambios (intervalo)", "Iteración", "Cantidad")
    st.session_state.graphRows[2][1].pyplot(fig)
    plt.close(fig)

    # fila 4+ - Constraints
    constraints = newStats.get("currentCostsByConstraint", {}).keys()
    row_index = 3
    col_index = 0
    for c in constraints:
        title = f"Constraint: {c} — {penalty_label}"
        fig, ax = plotLine(df, "iteration", [f"current_{c}", f"best_{c}"],
                           title, "Iteración", "Penalización",
                           labels=[f"Actual {c}", f"Mejor {c}"], colors=["orange", "blue"])
        st.session_state.graphRows[row_index][col_index].pyplot(fig)
        plt.close(fig)
        if col_index == 0:
            col_index = 1
        else:
            col_index = 0
            row_index += 1


def generateFiguresForPdf(statsHistory):
    df = pd.DataFrame(statsHistory)
    figs = []

    fig, ax = plotLine( df, "iteration", ["bestCost", "currentCost"], "Costos", "Iteración", "Valor", labels=["Mejor costo", "Costo actual"], colors=["blue", "orange"])
    figs.append(save_fig(fig))

    fig, ax = plotLine(df, "iteration", ["temperature"], "Temperatura", "Iteración", "Valor")
    figs.append(save_fig(fig))

    fig, ax = plotLine(df, "iteration", ["iterationsWithoutImprove"], "Iteraciones sin mejorar", "Iteración", "Cantidad")
    figs.append(save_fig(fig))

    fig, ax = plotLine(df, "iteration", ["iterationsWithoutChanges"], "Iteraciones sin cambiar", "Iteración", "Cantidad")
    figs.append(save_fig(fig))

    fig, ax = plotLine(df, "iteration", ["maxWithoutImproveInterval"], "Máximo sin mejorar (intervalo)", "Iteración", "Cantidad")
    figs.append(save_fig(fig))

    fig, ax = plotLine(df, "iteration", ["maxWithoutChangesInterval"], "Máximo sin cambios (intervalo)", "Iteración", "Cantidad")
    figs.append(save_fig(fig))

    constraints = [c.replace("current_", "") for c in df.columns if c.startswith("current_")]
    for c in constraints:
        if pd.api.types.is_numeric_dtype(df[f"current_{c}"]) and pd.api.types.is_numeric_dtype(df[f"best_{c}"]):
            fig, ax = plotLine(df, "iteration", [f"current_{c}", f"best_{c}"],
                               f"Constraint: {c}", "Iteración", "Penalización",
                               labels=[f"Actual {c}", f"Mejor {c}"], colors=["orange", "blue"])
            figs.append(save_fig(fig))

    return figs
