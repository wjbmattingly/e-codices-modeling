from bokeh.io import curdoc
from bokeh.plotting import figure

p = figure(x_range=(0,10), y_range=(0,10))
p.image_url(x=5, y=5, w=2, h=2, url=["myapp/static/images/0001.jpg"])

curdoc().add_root(p)
