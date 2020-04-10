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

#include <gnuradio/digital/crc32_bb.h>
// pydoc.h is automatically generated in the build directory
#include <crc32_bb_pydoc.h>

void bind_crc32_bb(py::module& m)
{

    using crc32_bb    = ::gr::digital::crc32_bb;


    py::class_<crc32_bb, gr::tagged_stream_block, gr::block, gr::basic_block,
        std::shared_ptr<crc32_bb>>(m, "crc32_bb", D(crc32_bb))

        .def(py::init(&crc32_bb::make),
           py::arg("check") = false,
           py::arg("lengthtagname") = "packet_len",
           py::arg("packed") = true,
           D(crc32_bb,make)
        )
        



        ;




}






