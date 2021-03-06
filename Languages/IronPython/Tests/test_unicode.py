# -*- coding: utf-8 -*-
#####################################################################################
#
#  Copyright (c) Microsoft Corporation. All rights reserved.
#
# This source code is subject to terms and conditions of the Apache License, Version 2.0. A
# copy of the license can be found in the License.html file at the root of this distribution. If
# you cannot locate the  Apache License, Version 2.0, please send an email to
# ironpy@microsoft.com. By using this source code in any fashion, you are agreeing to be bound
# by the terms of the Apache License, Version 2.0.
#
# You must not remove this notice, or any other, from this software.
#
#
#####################################################################################

from iptest.assert_util import *
from iptest.misc_util import ip_supported_encodings

def test_constructor():
    AreEqual('', unicode())
    AreEqual('None', unicode(None))
    AreEqual('ä', unicode('ä'))
    AreEqual('ä', unicode(b'\xc3\xa4', 'utf-8')) # TODO kunom: reasonable?

def test_raw_unicode_escape():
    for raw_unicode_escape in ['raw-unicode-escape', 'raw unicode escape']:
        s = unicode('\u0663\u0661\u0664 ', raw_unicode_escape)
        AreEqual(len(s), 4)
        AreEqual(int(s), 314)
        s = unicode('\u0663.\u0661\u0664 ',raw_unicode_escape)
        AreEqual(float(s), 3.14)

def test_raw_unicode_escape_noescape_lowchars():
    for raw_unicode_escape in ['raw-unicode-escape', 'raw unicode escape']:
        for i in range(0x100):
            AreEqual(unichr(i).encode(raw_unicode_escape), chr(i))
    
        AreEqual(unichr(0x100).encode(raw_unicode_escape), r'\u0100')

def test_raw_unicode_escape_dashes():
    """Make sure that either dashes or underscores work in raw encoding name"""
    ok = True
    try:
        unicode('hey', 'raw_unicode-escape')
    except LookupError:
        ok = False

    Assert(ok, "dashes and underscores should be interchangable")

def test_raw_unicode_escape_trailing_backslash():
    AreEqual(unicode('\\', 'raw_unicode_escape'), u'\\')

@skip("silverlight")
def test_unicode_error():
    
    from _codecs import register_error
    def handler(ex):
        AreEqual(ex.object, u'\uac00')
        return (u"", ex.end)
    register_error("test_unicode_error", handler)
                        
    for mode in ip_supported_encodings:  unichr(0xac00).encode(mode, "test_unicode_error")


@skip("silverlight") # only UTF8, no encoding fallbacks...
def test_ignore():
    AreEqual(unicode('', 'ascii', 'ignore'), '')
    AreEqual(unicode('\xff', 'ascii', 'ignore'), '')
    AreEqual(unicode('a\xffb\xffc\xff', 'ascii', 'ignore'), 'abc')

def test_cp19005():
    foo = u'\xef\xbb\xbf'
    AreEqual(repr(foo), r"u'\xef\xbb\xbf'")

@disabled('Conflicts with test_str.test_constructor. There is no reliable way to decide whether the client anticipates decoding or not.')
def test_cp34689():
    xx_full_width_a = u'xx\uff21'
    caught = False
    try:
        dummy = str(xx_full_width_a)
    except UnicodeEncodeError as ex:
        caught = True
        AreEqual(ex.encoding, 'ascii')
        AreEqual(ex.start, 2)
        AreEqual(ex.end, 3)
        AreEqual(ex.object, u'\uff21')
        Assert(ex.reason != None)
        Assert(len(ex.reason) > 0)

    Assert(caught)

def test_gh590():
    AreEqual(unicode(''.join(chr(i) for i in range(0x80, 0x100)), 'ascii', 'replace'), u'\ufffd'*0x80)

#--MAIN------------------------------------------------------------------------
run_test(__name__)
