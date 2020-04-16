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

#include <gnuradio/digital/constellation_soft_decoder_cf.h>
// pydoc.h is automatically generated in the build directory
#include <constellation_soft_decoder_cf_pydoc.h>

void bind_constellation_soft_decoder_cf(py::module& m)
{

    using constellation_soft_decoder_cf    = ::gr::digital::constellation_soft_decoder_cf;


    py::class_<constellation_soft_decoder_cf, gr::sync_interpolator, gr::sync_block, gr::block, gr::basic_block,
        std::shared_ptr<constellation_soft_decoder_cf>>(m, "constellation_soft_decoder_cf", D(constellation_soft_decoder_cf))

        .def(py::init(&constellation_soft_decoder_cf::make),
           py::arg("constellation"),
           D(constellation_soft_decoder_cf,make)
        )
        



        ;




}







