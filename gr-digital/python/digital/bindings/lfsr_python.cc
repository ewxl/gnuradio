/*
 * Copyright 2020 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(lfsr.h)                                                    */
/* BINDTOOL_HEADER_FILE_HASH(10d53da7e0116f6ca953fd66ec4b56b6)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/digital/lfsr.h>
// pydoc.h is automatically generated in the build directory
#include <lfsr_pydoc.h>

void bind_lfsr(py::module& m)
{

    using lfsr = ::gr::digital::lfsr;


    py::class_<lfsr, std::shared_ptr<lfsr>>(m, "lfsr", D(lfsr))

        .def(py::init<uint64_t, uint64_t, uint32_t>(),
             py::arg("mask"),
             py::arg("seed"),
             py::arg("reg_len"),
             D(lfsr, lfsr, 0))
        .def(py::init<gr::digital::lfsr const&>(), py::arg("arg0"), D(lfsr, lfsr, 1))


        .def("next_bit", &lfsr::next_bit, D(lfsr, next_bit))


        .def("next_bit_scramble",
             &lfsr::next_bit_scramble,
             py::arg("input"),
             D(lfsr, next_bit_scramble))


        .def("next_bit_descramble",
             &lfsr::next_bit_descramble,
             py::arg("input"),
             D(lfsr, next_bit_descramble))


        .def("reset", &lfsr::reset, D(lfsr, reset))


        .def("pre_shift", &lfsr::pre_shift, py::arg("num"), D(lfsr, pre_shift))


        .def("mask", &lfsr::mask, D(lfsr, mask))

        ;
}
