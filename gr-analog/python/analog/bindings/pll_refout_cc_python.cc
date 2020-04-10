/*
 * Copyright 2020 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/* This file is automatically generated using bindtool */

#include <pybind11/pybind11.h>
#include <pybind11/complex.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/analog/pll_refout_cc.h>
// pydoc.h is automatically generated in the build directory
#include <pll_refout_cc_pydoc.h>

void bind_pll_refout_cc(py::module& m)
{

    using pll_refout_cc    = ::gr::analog::pll_refout_cc;


    py::class_<pll_refout_cc, gr::sync_block, gr::block, gr::basic_block,
        std::shared_ptr<pll_refout_cc>>(m, "pll_refout_cc", D(pll_refout_cc))

        .def(py::init(&pll_refout_cc::make),
           py::arg("loop_bw"),
           py::arg("max_freq"),
           py::arg("min_freq"),
           D(pll_refout_cc,make)
        )
        



        ;




}






