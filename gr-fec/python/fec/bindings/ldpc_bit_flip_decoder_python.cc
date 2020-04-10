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

#include <gnuradio/fec/ldpc_bit_flip_decoder.h>
// pydoc.h is automatically generated in the build directory
#include <ldpc_bit_flip_decoder_pydoc.h>

void bind_ldpc_bit_flip_decoder(py::module& m)
{




        py::module m_code = m.def_submodule("code");

    using ldpc_bit_flip_decoder    = ::gr::fec::code::ldpc_bit_flip_decoder;


    py::class_<ldpc_bit_flip_decoder, gr::fec::generic_decoder,
        std::shared_ptr<ldpc_bit_flip_decoder>>(m_code, "ldpc_bit_flip_decoder", D(code,ldpc_bit_flip_decoder))

        .def_static("make",&ldpc_bit_flip_decoder::make,
           py::arg("mtrx_obj"),
           py::arg("max_iter") = 100,
           D(code,ldpc_bit_flip_decoder,make)
        )
        




        .def("set_frame_size",&ldpc_bit_flip_decoder::set_frame_size,
            py::arg("frame_size"),
            D(code,ldpc_bit_flip_decoder,set_frame_size)
        )


        .def("rate",&ldpc_bit_flip_decoder::rate,
            D(code,ldpc_bit_flip_decoder,rate)
        )

        ;






}






