##
## Copyright 2020 Free Software Foundation, Inc.
##
## This file is part of GNU Radio
##
## SPDX-License-Identifier: GPL-3.0-or-later
##
##
<%
    namespace = header_info['namespace']
    modname = header_info['module_name']
%>\
${license}

/* This file is automatically generated using bindtool */

#include <pybind11/pybind11.h>
#include <pybind11/complex.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <${prefix_include_root}/${basename}.h>

void bind_${basename}(py::module& m)
{
${render_namespace(namespace=namespace,modname=modname,modvar='m')}
}

<%def name='render_constructor()' >
</%def>

<%def name='render_function()' >
</%def>

<%def name='render_namespace(namespace, modname, modvar)'>
<%
    classes=namespace['classes']
    free_functions=namespace['free_functions']
    free_enums = namespace['enums']
    subnamespaces = []
    if 'namespaces' in namespace:
      subnamespaces = namespace['namespaces']
%>\
% for cls in classes:
% if classes:
    using ${cls['name']}    = ${namespace['name']}::${cls['name']};
% endif ##classes
% endfor ##classes
% for cls in classes:

<%
try:
        member_functions = cls['member_functions']
except:
        member_functions = []
try:
        constructors = cls['constructors']
except:
        constructors = []
try:
        class_enums = cls['enums']
except: 
        class_enums = []
try:
        class_variables = cls['variables']
except:
        class_variables = []

try:
        def find_make_function(member_fcns):
            for mf in member_fcns:
                if mf['name'] == 'make':
                    return mf
            return None

        make_function = find_make_function(member_functions)
except:
        make_function = None

isablock = False
if 'bases' in cls:
  base_str = '::'.join(list(filter(lambda x: x != '::',cls['bases'])))
  bases_with_block = [s for s in cls['bases'] if 'block' in s]
  if bases_with_block:
    isablock = True
    # The goal is to make gr::sync_block have the entire chain back to basic_block
    #  if base_str == gr::sync_block, base_str == gr::sync_block,gr::block,gr::basic_block
    if (base_str.endswith('gr::sync_block') or 
          base_str.endswith('gr::sync_interpolator') or 
          base_str.endswith('gr::sync_decimator') or 
          base_str.endswith('gr::tagged_stream_block')):
        base_str += ", gr::block"
    if base_str.endswith('gr::block'):
        base_str += ", gr::basic_block"
%>
    py::class_<${cls['name']}\
% if 'bases' in cls:
, ${base_str},
% else: 
,
% endif\
 
        std::shared_ptr<${cls['name']}>>(${modvar}, "${cls['name']}", D(${cls['name']}))

% if make_function: ## override constructors with make function
<%
fcn = make_function
fcn_args = fcn['arguments']
%>\
        .def(py::init(&${cls['name']}::${make_function['name']})${',' if fcn_args else ''}
% for arg in fcn_args:
           py::arg("${arg['name']}")${" = " + arg['default'] if arg['default'] else ''},
% endfor 
           D(${cls['name']},${make_function['name']})
        )
        
% else:
% for fcn in constructors:
<%
fcn_args = fcn['arguments']
%>\
\
% if len(fcn_args) == 0:
        .def(py::init<>())
%else:
        .def(py::init<\
% for arg in fcn_args:
${arg['dtype']}${'>(),' if loop.index == len(fcn['arguments'])-1 else ',' }\
% endfor ## args
\
% for arg in fcn_args:
           py::arg("${arg['name']}")${" = " + arg['default'] if arg['default'] else ''},
% endfor 
        ##    D(${cls['name']},${cls['name']}
        )
% endif
% endfor ## constructors
% endif ## make

% for fcn in member_functions:
<%
fcn_args = fcn['arguments']
fcn_name = fcn['name']
matcher = lambda x,name: x['name'] == name
overloaded = sum([matcher(f,fcn_name) for f in member_functions]) > 1
overloaded_str = ''
if overloaded:
  overloaded_str = '({} ({}::*)({}))'.format(fcn['return_type'],cls['name'],', '.join([f['dtype'] for f in fcn_args]))
%>\
% if fcn['name'] != 'make':
% if len(fcn_args) == 0:
        .def("${fcn['name']}",${overloaded_str}&${cls['name']}::${fcn['name']},D(${cls['name']},${fcn['name']}))
%else:
        .def("${fcn['name']}",${overloaded_str}&${cls['name']}::${fcn['name']},
% for arg in fcn_args:
            py::arg("${arg['name']}")${" = " + arg['default'] if arg['default'] else ''},
% endfor ## args 
            D(${cls['name']},${fcn['name']})
        )
% endif
% endif ## Not a make function
% endfor ## member_functions
        ;
% endfor ## classes

% if free_enums:
% for en in free_enums:
<%
values = en['values']
%>\
    py::enum_<${namespace['name']}::${en['name']}>(${modvar},"${en["name"]}")
% for val in values:
        .value("${val[0]}", ${namespace['name']}::${val[0]}) // ${val[1]}
% endfor 
        .export_values()
    ;
% endfor
% endif

% if free_functions:
% for fcn in free_functions:
<%
fcn_args = fcn['arguments']
fcn_name = fcn['name']
matcher = lambda x,name: x['name'] == name
overloaded = sum([matcher(f,fcn_name) for f in free_functions]) > 1
overloaded_str = ''
if overloaded:
  overloaded_str = '({} (*)({}))'.format(fcn['return_type'],', '.join([f['dtype'] for f in fcn_args]))
%>\
% if len(fcn_args) == 0:
    ${modvar}.def("${fcn['name']}",${overloaded_str}&${namespace['name']}::${fcn['name']},D(${cls['name']},${fcn['name']}));
%else:
    ${modvar}.def("${fcn['name']}",${overloaded_str}&${namespace}::${fcn['name']},
% for arg in fcn_args:
        py::arg("${arg['name']}")${" = " + arg['default'] if arg['default'] else ''}, 
% endfor
        D(${cls['name']},${fcn['name']})
    );
% endif
% endfor
% endif ## free_functions
\
% for sns in subnamespaces:
<%  
  submod_name = sns['name'].split('::')[-1]
  next_modvar = modvar + '_' + submod_name
%>
        py::module ${next_modvar} = ${modvar}.def_submodule("${submod_name}");
${render_namespace(namespace=sns,modname=modname,modvar=next_modvar)}
% endfor

</%def>