#!/usr/bin/env python2

from __future__ import print_function

import arrow
import csv
import plotly
import sys

import plotly.graph_objs as go


def parse_committers(path):
    all_committers = set()
    with open(path, 'rb') as f:
        rows = [(arrow.get(int(row[0].split()[0])),
                 row[1]) for row in csv.reader(f)]
    for (start, end) in arrow.Arrow.span_range('month', arrow.get(2015, 5, 1),
                                               arrow.utcnow()):
        committers = set()
        commits = 0

        while rows and rows[0][0] < end:
            (pushdate, user) = rows.pop(0)
            commits += 1
            committers.add(user)
            all_committers.add(user)
        yield (start, commits, len(committers), len(all_committers))


def parse_all():
    for ((month, cpp_commits, cpp_committers, total_cpp_committers),
         (m2, rust_commits, rust_committers, total_rust_committers)) in zip(
             parse_committers(sys.argv[2]), parse_committers(sys.argv[1])):
        assert month == m2
        # month.format('YYYY-MM')
        yield (month, cpp_commits, cpp_committers, total_cpp_committers,
               rust_commits, rust_committers, total_rust_committers)


def write_charts():
    data = list(parse_all())
    print('%d months' % len(data))
    dates = [d[0] for d in data]
    fig = plotly.tools.make_subplots(rows=4, cols=1,
                                     shared_xaxes=True,
                                     print_grid=False,
                                     subplot_titles=(
                                         'Unique Commit Authors by Month',
                                         'Total Unique Commit Authors',
                                         'Commits by Language',
                                     ))
    fig['layout']['xaxis1'].update({
        'type': 'date',
    })
    fig.append_trace(
        go.Scatter(
            x=dates,
            y=[d[2] for d in data],
            name='C/C++',
        ), 1, 1)
    fig.append_trace(
        go.Scatter(
            x=dates,
            y=[d[5] for d in data],
            name='Rust',
        ), 1, 1)
    fig.append_trace(
        go.Scatter(
            x=dates,
            y=[d[3] for d in data],
            yaxis='y2',
            name='C/C++',
        ), 2, 1)
    fig.append_trace(
        go.Scatter(
            x=dates,
            y=[d[6] for d in data],
            yaxis='y2',
            name='Rust',
        ), 2, 1)
    fig.append_trace(
        go.Scatter(
            x=dates,
            y=[d[1] for d in data],
            yaxis='y3',
            name='C/C++',
        ), 3, 1)
    fig.append_trace(
        go.Scatter(
            x=dates,
            y=[d[4] for d in data],
            yaxis='y3',
            name='Rust',
        ), 3, 1)
    fig.append_trace(
        go.Scatter(
            x=dates,
            y=[d[1] for d in data],
            yaxis='y4',
            name='C/C++',
            stackgroup='commits',
            groupnorm='percent',
        ), 4, 1)
    fig.append_trace(
        go.Scatter(
            x=dates,
            y=[d[4] for d in data],
            yaxis='y4',
            name='Rust',
            stackgroup='commits',
        ), 4, 1)
    div = plotly.offline.plot(
        fig,
        output_type='div',
        auto_open=False,
        show_link=False,
    )
    with open(sys.argv[3], 'wb') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Firefox commit authors using Rust and C/C++</title>
<style>
html, body {{
  width: 100%;
  height: 100%;
  margin: 0px;
  padding: 0px;
}}
body > div {{
  width: 100%;
  height: 100%;
}}
</style>
</head>
<body>
Generated from the scripts in <a href="https://github.com/luser/firefox-rust-committers>this repository</a>.
{}
</button>
</body>
</html>
'''.format(div))


if __name__ == '__main__':
    write_charts()
