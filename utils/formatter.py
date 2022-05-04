import altair as alt


def create_layered_bar_chart(
    data: alt.Data,
    x_shorthand: str,
    x_axis_title: str,
    y_shorthand: str,
    y_axis_title: str,
    z_shorthand: str,
    z_axis_title: str
) -> alt.Chart:
    return alt.Chart(data).mark_bar(opacity=0.7).encode(
        x=alt.X(
            shorthand=x_shorthand,
            axis=alt.Axis(title=x_axis_title)
        ),
        y=alt.Y(
            shorthand=y_shorthand,
            axis=alt.Axis(format='$.2f', title=y_axis_title),
            stack=None
        ),
        color=alt.Color(
            shorthand=z_shorthand,
            scale=alt.Scale(scheme='set1'),
            title=z_axis_title,
            legend=alt.Legend(orient='top')
        )
    )


def get_dollar_str(value: float) -> str:
    if value < 0:
        dollar_str = "-"
    else:
        dollar_str = ""
    dollar_str += "$%.2f" % (value.__abs__())
    return dollar_str
