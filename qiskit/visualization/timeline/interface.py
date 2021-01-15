# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=missing-return-type-doc

"""Qiskit timeline drawer.

This module provides a common user interface to the timeline drawer.
The `draw` function takes a scheduled circuit to visualize, as well as a style sheet
along with several control arguments.
The drawer canvas object is internally initialized from the input data and
the configured canvas is passed to one of the plotter APIs to generate a visualization data.
"""

from typing import Optional, Dict, Any, List, Tuple

from qiskit import circuit
from qiskit.visualization.exceptions import VisualizationError
from qiskit.visualization.timeline import types, core, stylesheet


def draw(program: circuit.QuantumCircuit,
         style: Optional[Dict[str, Any]] = None,
         time_range: Tuple[int, int] = None,
         disable_bits: List[types.Bits] = None,
         show_clbits: Optional[bool] = None,
         show_idle: Optional[bool] = None,
         show_barriers: Optional[bool] = None,
         show_delays: Optional[bool] = None,
         show_labels: bool = True,
         plotter: Optional[str] = types.Plotter.MPL.value,
         axis: Optional[Any] = None,
         filename: Optional[str] = None):
    r"""Generate visualization data for scheduled circuit programs.

    Args:
        program: Program to visualize. This program should be a `QuantumCircuit` which is
            transpiled with a scheduling_method, thus containing gate time information.
        style: Stylesheet options. This can be dictionary or preset stylesheet classes. See
            :py:class:`~qiskit.visualization.timeline.stylesheets.IQXStandard`,
            :py:class:`~qiskit.visualization.timeline.stylesheets.IQXSimple`, and
            :py:class:`~qiskit.visualization.timeline.stylesheets.IQXDebugging` for details of
            preset stylesheets. See also the stylesheet section for details of configuration keys.
        time_range: Set horizontal axis limit.
        disable_bits: List of qubits of classical bits not shown in the output image.
        show_clbits: A control property to show classical bits.
            Set `True` to show classical bits.
        show_idle: A control property to show idle timeline.
            Set `True` to show timeline without gates.
        show_barriers: A control property to show barrier instructions.
            Set `True` to show barrier instructions.
        show_delays: A control property to show delay instructions.
            Set `True` to show delay instructions.
        show_labels: A control property to show annotations, i.e. name, of gates.
            Set `True` to show annotations.
        plotter: Name of plotter API to generate an output image.
            One of following APIs should be specified::

                mpl: Matplotlib API
                    Matplotlib API to generate 2D image. Timelines are placed along y axis with
                    vertical offset. This API takes matplotlib.axes.Axes as `axis` input.

            `axis` and `style` kwargs may depend on the plotter.
        axis: Arbitrary object passed to the plotter. If this object is provided,
            the plotters uses given `axis` instead of internally initializing a figure object.
            This object format depends on the plotter. See plotters section for details.
        filename: If provided the output image is dumped into a file under the filename.

    Returns:
        Visualization output data.

        The returned data type depends on the `plotter`.
        If matplotlib family is specified, this will be a `matplotlib.pyplot.Figure` data.
        The returned data is generated by the `.get_image` method of the specified plotter API.

    Raises:
        ImportError: When required visualization package is not installed.
        VisualizationError: When invalid plotter API is specified.

    .. _style-dict-doc:

    **Style Dict Details**

    The stylesheet kwarg contains numerous options that define the style of the
    output timeline visualization.
    The stylesheet options can be classified into `formatter`, `generator` and `layout`.
    Those options available in the stylesheet are defined below:

    Args:
        formatter.general.fig_width: Width of output image (default `14`).
        formatter.general.fig_unit_height: Height of output image per timeline.
            The sum of all timeline becomes the height of the output image (default `0.8`).
        formatter.general.dpi: Dot per inch of image if `filename` is set (default `150`).
        formatter.margin.top: Margin from the top boundary of the figure canvas to
            the zero line of the first time slot (default `0.5`).
        formatter.margin.bottom: Margin from the bottom boundary of the figure canvas to
            the zero lien of the last time slot (default `0.5`).
        formatter.margin.left_percent:  Margin from the left boundary of the figure canvas to
            the left limit of the horizontal axis. The value is in units of percentage of
            the whole program duration. If the duration is 100 and the value of 0.5 is set,
            this keeps left margin of 5 (default `0.02`).
        formatter.margin.right_percent: Margin from the right boundary of the figure canvas to
            the right limit of the horizontal axis. The value is in units of percentage of
            the whole program duration. If the duration is 100 and the value of 0.5 is set,
            this keeps right margin of 5 (default `0.02`).
        formatter.margin.link_interval_dt: Allowed overlap of gate links.
            If multiple gate links are drawing within this range, links are horizontally
            shifted not to overlap with each other. This value is in units of
            the system cycle time dt (default `20`).
        formatter.time_bucket.edge_dt: The length of round edge of gate boxes. Gate boxes are
            smoothly faded in and out from the zero line. This value is in units of
            the system cycle time dt (default `10`).
        formatter.margin.minimum_duration: Minimum scheduled circuit duration.
            If the duration of input circuit is below this value, horizontal limit is
            set based on this value. This value is in units of
            the system cycle time dt (default `50`).
        formatter.color.background: Color code of the face color of canvas (default `#FFFFFF`).
        formatter.color.timeslot: Face color of the time slot box (default `#DDDDDD`).
        formatter.color.gate_name: Text color of the gate name annotations (default `#000000`).
        formatter.color.bit_name: Text color of the bit label annotations (default `#000000`).
        formatter.color.barrier: Line color of barriers (default `#222222`).
        formatter.color.gates: A dictionary of the gate box or gate symbol colors
            to use for each element type in the output visualization. The default
            values are::

                {
                    'u0': '#FA74A6',
                    'u1': '#000000',
                    'u2': '#FA74A6',
                    'u3': '#FA74A6',
                    'id': '#05BAB6',
                    'x': '#05BAB6',
                    'y': '#05BAB6',
                    'z': '#05BAB6',
                    'h': '#6FA4FF',
                    'cx': '#6FA4FF',
                    'cy': '#6FA4FF',
                    'cz': '#6FA4FF',
                    'swap': '#6FA4FF',
                    's': '#6FA4FF',
                    'sdg': '#6FA4FF',
                    'dcx': '#6FA4FF',
                    'iswap': '#6FA4FF',
                    't': '#BB8BFF',
                    'tdg': '#BB8BFF',
                    'r': '#BB8BFF',
                    'rx': '#BB8BFF',
                    'ry': '#BB8BFF',
                    'rz': '#BB8BFF',
                    'reset': '#808080',
                    'measure': '#808080'
                }

            You must specify all the necessary values if using this. If a gate name is not
            specified, the color in `formatter.color.default_gate` is applied.
        formatter.color.default_gate: Default gate color. This color is applied when
            a gate name to visualize is not contained in the dictionary of
            `formatter.color.gates` (default `#BB8BFF`).
        formatter.latex_symbol.gates: A dictionary of latex representation of gate names
            to use for each element type in the output visualization. The default
            values are::

                {
                    'u0': r'{\rm U}_0',
                    'u1': r'{\rm U}_1',
                    'u2': r'{\rm U}_2',
                    'u3': r'{\rm U}_3',
                    'id': r'{\rm Id}',
                    'x': r'{\rm X}',
                    'y': r'{\rm Y}',
                    'z': r'{\rm Z}',
                    'h': r'{\rm H}',
                    'cx': r'{\rm CX}',
                    'cy': r'{\rm CY}',
                    'cz': r'{\rm CZ}',
                    'swap': r'{\rm SWAP}',
                    's': r'{\rm S}',
                    'sdg': r'{\rm S}^\dagger',
                    'dcx': r'{\rm DCX}',
                    'iswap': r'{\rm iSWAP}',
                    't': r'{\rm T}',
                    'tdg': r'{\rm T}^\dagger',
                    'r': r'{\rm R}',
                    'rx': r'{\rm R}_x',
                    'ry': r'{\rm R}_y',
                    'rz': r'{\rm R}_z',
                    'reset': r'|0\rangle',
                    'measure': r'{\rm Measure}'
                }

            You must specify all the necessary values if using this. There is
            no provision for passing an incomplete dict in.
        formatter.latex_symbol.frame_change: Latex representation of
            the frame change symbol (default r`\circlearrowleft`).
        formatter.unicode_symbol.frame_change: Unicode representation of
            the frame change symbol (default u'\u21BA').
        formatter.box_height.gate: Height of gate box (default `0.5`).
        formatter.box_height.timeslot: Height of time slot (default `0.6`).
        formatter.layer.gate: Layer index of gate boxes. Larger number comes
            in the front of the output image (default `3`).
        formatter.layer.timeslot: Layer index of time slots. Larger number comes
            in the front of the output image (default `0`).
        formatter.layer.gate_name: Layer index of gate name annotations. Larger number comes
            in the front of the output image (default `5`).
        formatter.layer.bit_name: Layer index of bit labels. Larger number comes
            in the front of the output image (default `5`).
        formatter.layer.frame_change: Layer index of frame change symbols. Larger number comes
            in the front of the output image (default `4`).
        formatter.layer.barrier: Layer index of barrier lines. Larger number comes
            in the front of the output image (default `1`).
        formatter.layer.gate_link: Layer index of gate link lines. Larger number comes
            in the front of the output image (default `2`).
        formatter.alpha.gate: Transparency of gate boxes. A value in the range from
            `0` to `1`. The value `0` gives completely transparent boxes (default `1.0`).
        formatter.alpha.timeslot: Transparency of time slots. A value in the range from
            `0` to `1`. The value `0` gives completely transparent boxes (default `0.7`).
        formatter.alpha.barrier: Transparency of barrier lines. A value in the range from
            `0` to `1`. The value `0` gives completely transparent lines (default `0.5`).
        formatter.alpha.gate_link: Transparency of gate link lines. A value in the range from
            `0` to `1`. The value `0` gives completely transparent lines (default `0.8`).
        formatter.line_width.gate: Line width of the fringe of gate boxes (default `0`).
        formatter.line_width.timeslot: Line width of the fringe of time slots (default `0`).
        formatter.line_width.barrier: Line width of barrier lines (default `3`).
        formatter.line_width.gate_link: Line width of gate links (default `3`).
        formatter.line_style.barrier: Line style of barrier lines. This
            conforms to the line style spec of matplotlib (default `'-'`).
        formatter.line_style.gate_link: Line style of gate link lines. This
            conforms to the line style spec of matplotlib (default `'-'`).
        formatter.text_size.gate_name: Text size of gate name annotations (default `12`).
        formatter.text_size.bit_name: Text size of bit labels (default `15`).
        formatter.text_size.frame_change: Text size of frame change symbols (default `18`).
        formatter.text_size.axis_label: Text size of axis labels (default `13`).
        formatter.label_offset.frame_change: Offset of zero duration gate name annotations
            from the zero line of time slot (default `0.25`).
        formatter.control.show_idle: Set `True` to show time slots without gate (default `True`).
        formatter.control.show_clbits: Set `True` to show time slots of
            classical bits (default `True`).
        formatter.control.show_barriers: Set `True` to show barriers (default `True`).
        formatter.control.show_delays: Set `True` to show delay boxes (default `True`).
        generator.gates: List of callback functions that generates drawings
            for gates. Arbitrary callback functions satisfying the generator format
            can be set here. There are some default generators in the timeline drawer. See
            :py:mod:`~qiskit.visualization.timeline.generators` for more details.
            No default generator is set (default `[]`).
        generator.bits: List of callback functions that generates drawings for bit labels
            and time slots. Arbitrary callback functions satisfying the generator format
            can be set here. There are some default generators in the timeline drawer. See
            :py:mod:`~qiskit.visualization.timeline.generators` for more details.
            No default generator is set (default `[]`).
        generator.barriers: List of callback functions that generates drawings
            for barriers. Arbitrary callback functions satisfying the generator format
            can be set here. There are some default generators in the timeline drawer. See
            :py:mod:`~qiskit.visualization.timeline.generators` for more details.
            No default generator is set (default `[]`).
        generator.gate_links: List of callback functions that generates drawings
            for gate links. Arbitrary callback functions satisfying the generator format
            can be set here. There are some default generators in the timeline drawer. See
            :py:mod:`~qiskit.visualization.timeline.generators` for more details.
            No default generator is set (default `[]`).
        layout.bit_arrange: Callback function that sorts bits. See
            :py:mod:`~qiskit.visualization.timeline.layouts` for more details.
            No default layout is set. (default `None`).
        layout.time_axis_map: Callback function that determines the layout of
            horizontal axis labels. See :py:mod:`~qiskit.visualization.timeline.layouts`
            for more details. No default layout is set. (default `None`).

    Examples:
        To visualize a scheduled circuit program, you can call this function with set of
        control arguments. Most of appearance of the output image can be controlled by the
        stylesheet.

        Drawing with the default stylesheet.

        .. jupyter-execute::

            from qiskit import QuantumCircuit, transpile, schedule
            from qiskit.visualization.timeline import draw
            from qiskit.test.mock import FakeAlmaden

            qc = QuantumCircuit(2)
            qc.h(0)
            qc.cx(0,1)

            qc = transpile(qc, FakeAlmaden(), scheduling_method='alap')
            draw(qc)

        Drawing with the simple stylesheet.

        .. jupyter-execute::

            from qiskit import QuantumCircuit, transpile, schedule
            from qiskit.visualization.timeline import draw, IQXSimple
            from qiskit.test.mock import FakeAlmaden

            qc = QuantumCircuit(2)
            qc.h(0)
            qc.cx(0,1)

            qc = transpile(qc, FakeAlmaden(), scheduling_method='alap')
            draw(qc, style=IQXSimple())

        Drawing with the stylesheet suited for program debugging.

        .. jupyter-execute::

            from qiskit import QuantumCircuit, transpile, schedule
            from qiskit.visualization.timeline import draw, IQXDebugging
            from qiskit.test.mock import FakeAlmaden

            qc = QuantumCircuit(2)
            qc.h(0)
            qc.cx(0,1)

            qc = transpile(qc, FakeAlmaden(), scheduling_method='alap')
            draw(qc, style=IQXDebugging())

        You can partially customize a preset stylesheet when call it::

            my_style = {
                'formatter.general.fig_width': 16,
                'formatter.general.fig_unit_height': 1
            }
            style = IQXStandard(**my_style)

            # draw
            draw(qc, style=style)

        In the same way as above, you can create custom generator or layout functions
        and update existing stylesheet with custom functions.
        This feature enables you to control the most of appearance of the output image
        without modifying the codebase of the scheduled circuit drawer.
    """
    # update stylesheet
    temp_style = stylesheet.QiskitTimelineStyle()
    temp_style.update(style or stylesheet.IQXStandard())

    # update control properties
    if show_idle is not None:
        temp_style['formatter.control.show_idle'] = show_idle

    if show_clbits is not None:
        temp_style['formatter.control.show_clbits'] = show_clbits

    if show_barriers is not None:
        temp_style['formatter.control.show_barriers'] = show_barriers

    if show_delays is not None:
        temp_style['formatter.control.show_delays'] = show_delays

    # create empty canvas and load program
    canvas = core.DrawerCanvas(stylesheet=temp_style)
    canvas.load_program(program=program)

    #
    # update configuration
    #

    # time range
    if time_range:
        canvas.set_time_range(*time_range)

    # bits not shown
    if disable_bits:
        for bit in disable_bits:
            canvas.set_disable_bits(bit, remove=True)

    # show labels
    if not show_labels:
        labels = [types.LabelType.DELAY,
                  types.LabelType.GATE_PARAM,
                  types.LabelType.GATE_NAME]
        for label in labels:
            canvas.set_disable_type(label, remove=True)

    canvas.update()

    #
    # Call plotter API and generate image
    #

    if plotter == types.Plotter.MPL.value:
        try:
            from qiskit.visualization.timeline.plotters import MplPlotter
        except ImportError as ex:
            raise ImportError('Must have Matplotlib installed.') from ex

        plotter_api = MplPlotter(canvas=canvas, axis=axis)
        plotter_api.draw()
    else:
        raise VisualizationError('Plotter API {name} is not supported.'.format(name=plotter))

    # save figure
    if filename:
        plotter_api.save_file(filename=filename)

    return plotter_api.get_image()
