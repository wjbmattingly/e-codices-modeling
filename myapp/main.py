import numpy as np
import pandas as pd
from bokeh.layouts import column, row
from bokeh.models import Button, ColumnDataSource, TextInput, DataTable, TableColumn, ColorBar, HTMLTemplateFormatter, Spinner, RangeSlider, CustomJS, HoverTool, Div
from bokeh.plotting import figure
from bokeh.palettes import Spectral6
from bokeh.io import curdoc
import os

df = pd.read_csv("ready.csv")
df['alpha'] = 0.5
width = 60
highlighted_idx = []
columns = [
    TableColumn(field="title", title="title"),
    TableColumn(field="image", title="image", formatter=HTMLTemplateFormatter(template=f'<img src="<%= image %>" width={width}>')),
    # TableColumn(field="image", title="image", formatter=HTMLTemplateFormatter(template='<img src="myapp/static/images/0001.jpg" width=60>')),
    TableColumn(field="image", title="download", formatter=HTMLTemplateFormatter(template=r'<a href="<%= image %>", target="_blank">download</a>')),]


def update(attr, old, new):
    """Callback used for plot update when lasso selecting"""
    global highlighted_idx
    subset = df.iloc[new]
    highlighted_idx = new
    subset = subset.iloc[np.random.permutation(len(subset))]
    source.data = subset

def save():
    """Callback used to save highlighted data points"""
    global highlighted_idx
    df.iloc[highlighted_idx][['title', 'image']].to_csv(text_filename.value, index=False)


source = ColumnDataSource(data=dict())
source_orig = ColumnDataSource(data=df)

data_table = DataTable(source=source, columns=columns, row_height=100, width=500 if "color" in df.columns else 500)
source.data = df

p = figure(title="", sizing_mode="scale_both", tools=["lasso_select", "box_select", "pan", "box_zoom", "wheel_zoom", "reset"])
p.toolbar.active_drag = None
p.toolbar.active_inspect = None

circle_kwargs = {"x": "x", "y": "y", "size": 1, "source": source_orig, "alpha": "alpha"}
if "color" in df.columns:
    circle_kwargs.update({"color": mapper})
    color_bar = ColorBar(color_mapper=mapper['transform'], width=8)
    p.add_layout(color_bar, 'right')

scatter = p.circle(**circle_kwargs)
p.plot_width = 500
if "color" in df.columns:
    p.plot_width=350
p.plot_height = 500

## Spinner for Node Size
spinner = Spinner(title="Circle Size", low = 1, high=60, step=1, value=scatter.glyph.size, width=200)
spinner.js_link("value", scatter.glyph, "size")


## Spinner for Image Width
image_width_spinner = Spinner(title="Circle Size", low = 50, high=250, step=1, value=width, width=200)


## Adjust Row Height
row_spinner = Spinner(title="Row Height", low = 100, high=1000, step=10, value=data_table.row_height, width=200)
row_spinner.js_link("value", data_table, "row_height")


scatter.data_source.selected.on_change('indices', update)

text_filename = TextInput(value="out.csv", title="Filename:")
save_btn = Button(label="SAVE")
save_btn.on_click(save)

controls_main = column(spinner, p, text_filename, save_btn)
controls = column(row_spinner, data_table)
curdoc().add_root(row(controls_main, controls))
