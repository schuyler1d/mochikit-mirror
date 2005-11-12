#!/usr/bin/env python
import os
import sys
from docutils import nodes, utils
from docutils.core import publish_file
from docutils.parsers.rst import roles

def mochi_name(text):
    name = text.split('(', 1)[0].split()[0]
    base = ''
    if name.startswith('MochiKit.'):
        # cross-reference
        parts = name.split('.', 2)
        base = parts[1] + '.html'
        name = '.'.join(parts[2:])
    return base, name

def role_mochiref(role, rawtext, text, lineno, inliner, options=None, content=[]):
    if options is None:
        options = {}
    base, name = mochi_name(text)
    ref = base
    if name:
        ref += '#fn-' + name
    roles.set_classes(options)
    options.setdefault('classes', []).append('mochiref')
    node = nodes.reference(
        text, utils.unescape(text), refuri=ref, **options)
    return [node], []

roles.register_canonical_role('mochiref', role_mochiref)

def role_mochidef(role, rawtext, text, lineno, inliner, options=None, content=[]):
    if options is None:
        options = {}
    base, name = mochi_name(text)
    assert base == ''
    anchor = nodes.raw('', '<a name="fn-%s"></a>' % (utils.unescape(name),),
        format='html')
    roles.set_classes(options)
    options.setdefault('classes', []).append('mochidef')
    node = nodes.literal(text, text, **options)
    return [anchor, node], []

roles.register_canonical_role('mochidef', role_mochidef)
        


def main():
    basepath = os.path.join('doc/rst', '')
    destpath = os.path.join('doc/html', '')
    for root, dirs, files in os.walk(basepath):
        if '.svn' in dirs:
            dirs.remove('.svn')
        destroot = destpath + root[len(basepath):]
        if not os.path.exists(destroot):
            os.makedirs(destroot)
        for fn in files:
            basefn, ext = os.path.splitext(fn)
            if ext == '.rst':
                srcfn = os.path.join(root, fn)
                dest = os.path.join(destroot, basefn + '.html')
                if basefn != "index":
                    try:
                        if os.path.getmtime(dest) >= os.path.getmtime(srcfn):
                            print srcfn, "not changed"
                            continue
                    except OSError:
                        pass
                print srcfn
                res = publish_file(
                    source_path=srcfn,
                    destination_path=dest,
                    writer_name='html',
                    settings_overrides=dict(
                        input_encoding='utf8',
                        output_encoding='utf8',
                        embed_stylesheet=False,
                        stylesheet_path='include/css/documentation.css',
                    ),
                )

if __name__ == '__main__':
    main()
