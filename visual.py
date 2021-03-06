'''
Bokeh https://docs.bokeh.org/en/latest/docs/first_steps/first_steps_9.html
'''

from bokeh.plotting import figure, show, curdoc
from bokeh.layouts import gridplot, layout
from bokeh.models import Div, RangeSlider, ColumnDataSource
from matgen import core

filename = 'tests/test_data/pass1_model_2d.txt'
#c = core.CellComplex(filename=filename, measures=True, theta=True)
c = core.CellComplex(filename=filename)

with open('tests/test_data/pass_1_misorientation.txt', 'r') as file:
    for line, edge in zip(file, c.edges):
        edge.theta = float(line.strip())

def get_xy(v_ids):
    vs = c.get_many('v', v_ids)
    xs = [v.x for v in vs]
    ys = [v.y for v in vs]
    return xs, ys

s0 = ColumnDataSource(data=dict(x=[], y=[]))
s1 = ColumnDataSource(data=dict(x=[], y=[]))
s2 = ColumnDataSource(data=dict(x=[], y=[]))
s3 = ColumnDataSource(data=dict(x=[], y=[]))

p0 = figure(
    title="J0", x_axis_label='x', y_axis_label='y',
    x_range=(-0.1, 1.1), y_range=(-0.1, 1.1)
)
p0.scatter('x', 'y', source=s0, color='black', size=2)

p1 = figure(
    title="J1", x_axis_label='x', y_axis_label='y',
    x_range=(-0.1, 1.1), y_range=(-0.1, 1.1)
)
p1.scatter('x', 'y', source=s1, color='black', size=2)

p2 = figure(
    title="J2", x_axis_label='x', y_axis_label='y',
    x_range=(-0.1, 1.1), y_range=(-0.1, 1.1)
)
p2.scatter('x', 'y', source=s2, color='black', size=2)

p3 = figure(
    title="J3", x_axis_label='x', y_axis_label='y',
    x_range=(-0.1, 1.1), y_range=(-0.1, 1.1)
    )
p3.scatter('x', 'y', source=s3, color='black', size=2)

range_slider = RangeSlider(
    title="Choose theta", # a title to display above the slider
    start=0,  # set the minimum value for the slider
    end=62,  # set the maximum value for the slider
    step=1,  # increments for the slider
    value=(0, 62),  # initial values for slider
    )

div = Div(
    text=f"""
          <p>Select {round(range_slider.value[0])}""" +\
        f""" - {round(range_slider.value[1])}:</p>
          """,
    width=200,
    height=30,
)

def update_data(attrname, new, old):

    div.text = f"""
          <p>Select {round(range_slider.value[0])}""" +\
        f""" - {round(range_slider.value[1])}:</p>
          """
    
    lt = round(range_slider.value[0])
    ut = round(range_slider.value[1])
    c.reset_special(lt, ut)

    x, y = get_xy(c.get_junction_ids_of_type(0))
    s0.data = dict(x=x, y=y)
    x, y = get_xy(c.get_junction_ids_of_type(1))
    s1.data = dict(x=x, y=y)
    x, y = get_xy(c.get_junction_ids_of_type(2))
    s2.data = dict(x=x, y=y)
    x, y = get_xy(c.get_junction_ids_of_type(3))
    s3.data = dict(x=x, y=y)

range_slider.on_change('value', update_data)

grid = gridplot([[p1, p2, p3], [p0, None, None]], width=400, height=400)

layout = layout(
    [
        [range_slider, div],
        [grid],
    ]
)

curdoc().add_root(layout)

# show(layout)