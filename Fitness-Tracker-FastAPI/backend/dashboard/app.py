import os
from typing import List

import httpx
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html


def _normalize_base_url(base_url: str) -> str:
    """Ensure API base URL has no trailing slash for consistent joining."""
    return base_url[:-1] if base_url.endswith("/") else base_url


def _fetch_fitness_rows(api_base_url: str, user_id: int) -> List[dict]:
    """Fetch fitness rows for a user from the FastAPI backend."""
    normalized = _normalize_base_url(api_base_url)
    url = f"{normalized}/fitness/{user_id}"
    with httpx.Client(timeout=5.0) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.json()


def _empty_figure(message: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=message, x=0.5, y=0.5, showarrow=False, xref="paper", yref="paper"
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
    return fig


def create_dash_app(api_base_url: str | None = None) -> Dash:
    """Create a Dash app mounted under /dashboard that polls the FastAPI API."""
    base_url = api_base_url or os.getenv("API_BASE_URL", "http://localhost:8000")

    dash_app = Dash(
        __name__,
        requests_pathname_prefix="/dashboard/",
        title="Fitness Dashboard",
        update_title=None,
        suppress_callback_exceptions=True,
    )

    dash_app.layout = html.Div(
        [
            html.H1("Fitness Tracker Dashboard", style={"marginBottom": "0.4rem"}),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("User ID", htmlFor="user-id"),
                            dcc.Input(
                                id="user-id", type="number", value=1, min=1, step=1
                            ),
                        ],
                        style={
                            "display": "flex",
                            "gap": "0.5rem",
                            "alignItems": "center",
                        },
                    ),
                    html.Div(id="summary"),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                },
            ),
            html.Div(
                [
                    dcc.Graph(
                        id="calories-by-workout",
                        style={"flex": "1", "minWidth": "300px"},
                    ),
                    dcc.Graph(
                        id="duration-over-sessions",
                        style={"flex": "1", "minWidth": "300px"},
                    ),
                ],
                style={
                    "display": "flex",
                    "gap": "1rem",
                    "flexWrap": "wrap",
                    "marginTop": "1rem",
                },
            ),
            dcc.Interval(id="refresh-interval", interval=5_000, n_intervals=0),
            html.Div(
                id="hidden-base-url", style={"display": "none"}, children=base_url
            ),
        ],
        style={"maxWidth": "1100px", "margin": "0 auto", "padding": "1rem"},
    )

    @dash_app.callback(
        Output("calories-by-workout", "figure"),
        Output("duration-over-sessions", "figure"),
        Output("summary", "children"),
        Input("user-id", "value"),
        Input("refresh-interval", "n_intervals"),
        prevent_initial_call=False,
    )
    def refresh_charts(user_id: int | None, _n: int):  # type: ignore[unused-argument]
        if not user_id:
            msg = "Enter a user id to view workouts."
            return _empty_figure(msg), _empty_figure(msg), html.Div(msg)

        try:
            rows = _fetch_fitness_rows(base_url, int(user_id))
        except Exception as exc:  # pragma: no cover - runtime feedback only
            error_text = (
                f"Could not load data: {exc}" if user_id else "No user selected"
            )
            return (
                _empty_figure(error_text),
                _empty_figure(error_text),
                html.Div(error_text),
            )

        if not rows:
            msg = "No workouts yet for this user."
            return _empty_figure(msg), _empty_figure(msg), html.Div(msg)

        df = pd.DataFrame(rows)
        df = df.sort_values("id")

        calories_fig = _empty_figure("No data")
        duration_fig = _empty_figure("No data")

        if not df.empty:
            calories_fig = go.Figure(
                data=[
                    go.Bar(x=df["workout"], y=df["calories"], marker_color="#5b8def"),
                ],
                layout=go.Layout(title="Calories burned by workout"),
            )

            duration_fig = go.Figure(
                data=[
                    go.Scatter(
                        x=df.index,
                        y=df["duration"],
                        mode="lines+markers",
                        marker=dict(color="#34a853"),
                    ),
                ],
                layout=go.Layout(
                    title="Duration by session order",
                    xaxis_title="Session",
                    yaxis_title="Minutes",
                ),
            )

        total_calories = int(df["calories"].sum()) if not df.empty else 0
        total_minutes = int(df["duration"].sum()) if not df.empty else 0
        session_count = len(df)

        summary_block = html.Div(
            [
                html.Div(f"Sessions: {session_count}"),
                html.Div(f"Total minutes: {total_minutes}"),
                html.Div(f"Total calories: {total_calories}"),
            ],
            style={"display": "flex", "gap": "1rem", "fontWeight": "600"},
        )

        return calories_fig, duration_fig, summary_block

    return dash_app
