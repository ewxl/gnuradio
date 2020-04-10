#
# Copyright 2010-2012,2020 Free Software Foundation, Inc.
#
# This file was generated by gr_modtool, a tool from the GNU Radio framework
# This file is a part of gr-howto
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
#
"""
Updates the *pydoc_h files for a module
Execute using: python update_pydoc.py xml_path outputfilename

The file instructs Pybind11 to transfer the doxygen comments into the
python docstrings.

"""
from __future__ import unicode_literals

import os, sys, time, glob, re

from doxyxml import DoxyIndex, DoxyClass, DoxyFriend, DoxyFunction, DoxyFile
from doxyxml import DoxyOther, base

def py_name(name):
    bits = name.split('_')
    return '_'.join(bits[1:])

def make_name(name):
    bits = name.split('_')
    return bits[0] + '_make_' + '_'.join(bits[1:])


class Block(object):
    """
    Checks if doxyxml produced objects correspond to a gnuradio block.
    """

    @classmethod
    def includes(cls, item):
        if not isinstance(item, DoxyClass):
            return False
        # Check for a parsing error.
        if item.error():
            return False
        friendname = make_name(item.name())
        is_a_block = item.has_member(friendname, DoxyFriend)
        # But now sometimes the make function isn't a friend so check again.
        if not is_a_block:
            is_a_block = di.has_member(friendname, DoxyFunction)
        return is_a_block

class Block2(object):
    """
    Checks if doxyxml produced objects correspond to a new style
    gnuradio block.
    """

    @classmethod
    def includes(cls, item):
        if not isinstance(item, DoxyClass):
            return False
        # Check for a parsing error.
        if item.error():
            return False
        is_a_block2 = item.has_member('make', DoxyFunction) and item.has_member('sptr', DoxyOther)
        return is_a_block2


def utoascii(text):
    """
    Convert unicode text into ascii and escape quotes and backslashes.
    """
    if text is None:
        return ''
    out = text.encode('ascii', 'replace')
    # swig will require us to replace blackslash with 4 backslashes
    # TODO: evaluate what this should be for pybind11
    out = out.replace(b'\\', b'\\\\\\\\')
    out = out.replace(b'"', b'\\"').decode('ascii')
    return str(out)


def combine_descriptions(obj):
    """
    Combines the brief and detailed descriptions of an object together.
    """
    description = []
    bd = obj.brief_description.strip()
    dd = obj.detailed_description.strip()
    if bd:
        description.append(bd)
    if dd:
        description.append(dd)
    return utoascii('\n\n'.join(description)).strip()

def format_params(parameteritems):
    output = ['Args:']
    template = '    {0} : {1}'
    for pi in parameteritems:
        output.append(template.format(pi.name, pi.description))
    return '\n'.join(output)

entry_templ = '%feature("docstring") {name} "{docstring}"'
def make_entry(obj, name=None, templ="{description}", description=None, params=[]):
    """
    Create a docstring key/value pair, where the key is the object name.

    obj - a doxyxml object from which documentation will be extracted.
    name - the name of the C object (defaults to obj.name())
    templ - an optional template for the docstring containing only one
            variable named 'description'.
    description - if this optional variable is set then it's value is
            used as the description instead of extracting it from obj.
    """
    if name is None:
        name=obj.name()
    if "operator " in name:
        return ''
    if description is None:
        description = combine_descriptions(obj)
    if params:
        description += '\n\n'
        description += utoascii(format_params(params))
    docstring = templ.format(description=description)

    return {name: docstring}


def make_class_entry(klass, description=None, ignored_methods=[], params=None):
    """
    Create a class docstring key/value pair.
    """
    if params is None:
        params = klass.params
    output = {}
    output.update(make_entry(klass, description=description, params=params))
    for func in klass.in_category(DoxyFunction):
        if func.name() not in ignored_methods:
            name = klass.name() + '::' + func.name()
            output.update(make_entry(func, name=name))
    return output


def make_block_entry(di, block):
    """
    Create class and function docstrings of a gnuradio block
    """
    descriptions = []
    # Get the documentation associated with the class.
    class_desc = combine_descriptions(block)
    if class_desc:
        descriptions.append(class_desc)
    # Get the documentation associated with the make function
    make_func = di.get_member(make_name(block.name()), DoxyFunction)
    make_func_desc = combine_descriptions(make_func)
    if make_func_desc:
        descriptions.append(make_func_desc)
    # Get the documentation associated with the file
    try:
        block_file = di.get_member(block.name() + ".h", DoxyFile)
        file_desc = combine_descriptions(block_file)
        if file_desc:
            descriptions.append(file_desc)
    except base.Base.NoSuchMember:
        # Don't worry if we can't find a matching file.
        pass
    # And join them all together to make a super duper description.
    super_description = "\n\n".join(descriptions)
    # Associate the combined description with the class and
    # the make function.
    output = {}
    output.update(make_class_entry(block, description=super_description))
    output.update(make_entry(make_func, description=super_description,
                                  params=block.params))
    return output

def make_block2_entry(di, block):
    """
    Create class and function docstrings of a new style gnuradio block
    """
    # For new style blocks all the relevant documentation should be
    # associated with the 'make' method.
    class_description = combine_descriptions(block)
    make_func = block.get_member('make', DoxyFunction)
    make_description = combine_descriptions(make_func)
    description = class_description + "\n\nConstructor Specific Documentation:\n\n" + make_description
    # Associate the combined description with the class and
    # the make function.
    output = {}
    output.update(make_class_entry(
            block, description=description,
            ignored_methods=['make'], params=make_func.params))
    makename = block.name() + '::make'
    output.update(make_entry(
            make_func, name=makename, description=description,
            params=make_func.params))
    return output

def get_docstrings_dict(di, custom_output=None):

    output = {}
    if custom_output:
        output.update(custom_output)

    # Create docstrings for the blocks.
    blocks = di.in_category(Block)
    blocks2 = di.in_category(Block2)

    make_funcs = set([])
    for block in blocks:
        try:
            make_func = di.get_member(make_name(block.name()), DoxyFunction)
            # Don't want to risk writing to output twice.
            if make_func.name() not in make_funcs:
                make_funcs.add(make_func.name())
                output.update(make_block_entry(di, block))
        except block.ParsingError:
            sys.stderr.write('Parsing error for block {0}\n'.format(block.name()))
            raise

    for block in blocks2:
        try:
            make_func = block.get_member('make', DoxyFunction)
            make_func_name = block.name() +'::make'
            # Don't want to risk writing to output twice.
            if make_func_name not in make_funcs:
                make_funcs.add(make_func_name)
                output.update(make_block2_entry(di, block))
        except block.ParsingError:
            sys.stderr.write('Parsing error for block {0}\n'.format(block.name()))
            raise

    # Create docstrings for functions
    # Don't include the make functions since they have already been dealt with.
    funcs = [f for f in di.in_category(DoxyFunction)
             if f.name() not in make_funcs and not f.name().startswith('std::')]
    for f in funcs:
        try:
            output.update(make_entry(f))
        except f.ParsingError:
            sys.stderr.write('Parsing error for function {0}\n'.format(f.name()))

    # Create docstrings for classes
    block_names = [block.name() for block in blocks]
    block_names += [block.name() for block in blocks2]
    klasses = [k for k in di.in_category(DoxyClass)
               if k.name() not in block_names and not k.name().startswith('std::')]
    for k in klasses:
        try:
            output.update(make_class_entry(k))
        except k.ParsingError:
            sys.stderr.write('Parsing error for class {0}\n'.format(k.name()))

    # Docstrings are not created for anything that is not a function or a class.
    # If this excludes anything important please add it here.

    return output

def sub_docstring_in_pydoc_h(pydoc_files, docstrings_dict, output_dir):
    for pydoc_file in pydoc_files:
        file_in = open(pydoc_file,'r').read()
        for key, value in docstrings_dict.items():  
            doc_key = key.split("::")
            if 'gr' in doc_key:
                doc_key.remove('gr') 
            doc_key = '_'.join(doc_key)
            regexp = r'(__doc_{} =\sR\"doc\()[^)]*(\)doc\")'.format(doc_key)
            regexp = re.compile(regexp, re.MULTILINE)
            (file_in, nsubs) = regexp.subn(r'\1'+value+r'\2', file_in, count=1)

        output_pathname = os.path.join(output_dir, os.path.basename(pydoc_file).replace('_template.h','.h'))
        with open(output_pathname,'w') as file_out:
            file_out.write(file_in)

if __name__ == "__main__":
    # Parse command line options and set up doxyxml.
    err_msg = "Execute using: python update_pydoc.py xml_path [outputfilename]"
    if len(sys.argv) < 4:
        raise Exception(err_msg)
    xml_path = sys.argv[1]
    bindings_dir = sys.argv[2]
    output_dir = sys.argv[3]
    dbg_output_filename = sys.argv[4] if len(sys.argv) >= 5 else None
    di = DoxyIndex(xml_path)

    # Generate the docstrings interface file.
    docstrings_dict = get_docstrings_dict(di)
    if dbg_output_filename:
        import json
        with open(dbg_output_filename, 'w') as fp:
            json.dump(docstrings_dict, fp)

    # Go through the python/bindings directory and fill in doc()doc with the docstring
    # This file lives at ./docs/doxygen/
    # Pydocs live at ../../python/bindings/
    # bindings_path = os.path.join(os.path.dirname(__file__),'..','..','python','bindings')
    pydoc_files = glob.glob(os.path.join(bindings_dir,'*_pydoc_template.h'))

    sub_docstring_in_pydoc_h(pydoc_files, docstrings_dict, output_dir)