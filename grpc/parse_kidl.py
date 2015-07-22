"""
Parse KIDL down to a reasonable object.
"""
__author__ = 'Dan Gunter <dkgunter@lbl.gov>'
__date__ = '7/17/15'

from pyparsing import Literal, CaselessLiteral, Word, Upcase, OneOrMore, ZeroOrMore, \
    Forward, NotAny, delimitedList, oneOf, Group, Optional, Combine, alphas, \
    nums, restOfLine, cStyleComment, \
    alphanums, empty, quotedString, ParseException, ParseResults, \
    Keyword, Suppress
import re

## Example data

__test_data = ('''
module Foo {
typedef int bar;
typedef ud1 baz;
typedef structure { string bar; int ggg; } fooz;
}
''',
'''
/*
  API Access to the Genome Annotation Service.

  Provides support for gene calling, functional annotation, re-annotation. Use to extract annotation in
formation about an existing genome, or to create new annotations.

 */
module GenomeAnnotation
{
/* A feature object represents a feature on the genome. It contains
       the location on the contig with a type, the translation if it
       represents a protein, associated aliases, etc. It also contains
       information gathered during the annotation process that is involved
       in stages that perform overlap removal, quality testing, etc.
    */
    typedef structure {
	feature_id id;
	location location;
	feature_type type;
	string function;
	/*
	 * The function_id refers to the particular proposed function that was chosen
	 * for this feature.
	 */
	string function_id;
	string protein_translation;
	list<string> aliases;
	list<tuple<string source, string alias>> alias_pairs;
	list<annotation> annotations;
	feature_quality_measure quality;
	analysis_event_id feature_creation_event;
	list<protein_family_assignment> family_assignments;
	list<similarity_association> similarity_associations;
	list<proposed_function> proposed_functions;

	string genbank_type;
	genbank_feature genbank_feature;
    } feature;
}
''',
'''
module foo {
    funcdef query_classifier_taxonomies(string classifier) returns(list<string group_id>);
    funcdef query_classifier_taxonomies(string classifier) returns(mapping<string group_id, string taxonomy>);
    funcdef query_classifier_taxonomies(string classifier) returns(mapping<string group_id, string taxonomy>) authentication required;
}
''')
class Specification(object):
    _bnf = None

    def __init__(self, module_spec):
        if self._bnf is None:
            self._create_bnf()
        self._r = self._bnf.parseString(module_spec)
        self.definitions = []
        for module in self._r:
            for x in module:
                if hasattr(x, 'extend'):
                    self.definitions.append(Definition(module['name'], x))

    def __str__(self):
        return str(self._r)

    def _create_bnf(self):
        # punctuation
        colon  = Literal(':')
        lbrace = Literal('{')
        rbrace = Literal('}')
        lbrack = Literal('[')
        rbrack = Literal(']')
        lparen = Literal('(')
        rparen = Literal(')')
        equals = Literal('=')
        comma  = Literal(',')
        dot    = Literal('.')
        slash  = Literal('/')
        bslash = Literal('\\')
        star   = Literal('*')
        semi   = Literal(';')
        langle = Literal('<')
        rangle = Literal('>')

        # keywords
        any_       = Keyword('any')
        auth_      = Keyword('authentication')
        attribute_ = Keyword('attribute')
        boolean_   = Keyword('boolean')
        case_      = Keyword('case')
        char_      = Keyword('char')
        const_     = Keyword('const')
        context_   = Keyword('context')
        default_   = Keyword('default')
        double_    = Keyword('double')
        enum_      = Keyword('enum')
        exception_ = Keyword('exception')
        false_     = Keyword('FALSE')
        fixed_     = Keyword('fixed')
        float_     = Keyword('float')
        func_      = Keyword('funcdef')
        int_       = Keyword('int')
        long_      = Keyword('long')
        module_    = Keyword('module')
        object_    = Keyword('Object')
        octet_     = Keyword('octet')
        req_       = Keyword('required')
        return_    = Keyword('returns')
        oneway_    = Keyword('oneway')
        out_       = Keyword('out')
        raises_    = Keyword('raises')
        readonly_  = Keyword('readonly')
        sequence_  = Keyword('list')
        string_    = Keyword('string')
        struct_    = Keyword('structure')
        switch_    = Keyword('switch')
        true_      = Keyword('TRUE')
        typedef_   = Keyword('typedef')
        unsigned_  = Keyword('unsigned')
        union_     = Keyword('union')
        void_      = Keyword('void')
        wchar_     = Keyword('wchar')
        wstring_   = Keyword('wstring')

        # suppress (ignore) some punctuation
        ssemi   = Suppress(semi)
        slbrace, srbrace = Suppress(lbrace), Suppress(rbrace)
        slangle, srangle = Suppress(langle), Suppress(rangle)

        # optional c-style comment blocks
        comment_opt = Optional(cStyleComment).setName('comment')

        # identifier
        identifier = Word(alphas, alphanums + '_').setName('identifier')

        # -- Type definitions --
        # numeric types
        real = Combine( Word(nums+'+-', nums) + dot + Optional( Word(nums) )
                        + Optional( CaselessLiteral('E') + Word(nums+'+-',nums) ) )
        integer = ( Combine( CaselessLiteral('0x') + Word( nums+'abcdefABCDEF' ) ) |
                    Word( nums+'+-', nums ) ).setName('int')
        # user-defined type
        ud_type_name = identifier.setName('udType')  # user-defined type
        # user + builtin types.
        # Note: have to use longest match for type, in case a user-defined type
        # name starts with a keyword type, like 'stringSeq' or 'longArray'
        type_name = (any_ ^ boolean_ ^ char_ ^ double_ ^ fixed_ ^ float_ ^
                     int_ ^ long_ ^ octet_ ^ string_ ^ wchar_ ^
                     wstring_ ^ ud_type_name).setName('type')
        # variable name
        var_name = identifier.setName('variable')
        # optionally-var type, e.g. 'string foo' or 'string'
        type_ov = Group(type_name + Optional(var_name))
        # recursive list<list<name type, name type>>, etc.
        seq_list = Forward().setName('list')
        seq_tuple = Forward().setName('tuple')
        mapping = Forward().setName('map')
        seq_any = seq_list | seq_tuple | mapping
        simple_type = comment_opt + (seq_list ^ seq_tuple ^ mapping ^ type_name)
        opt_id = Optional(identifier)
        seq_list << Keyword('list') + slangle + \
                          Group(simple_type + opt_id) + srangle
        seq_tuple << Keyword('tuple') + slangle + \
                     delimitedList(Group(simple_type + opt_id)) + srangle
        mapping << Keyword('mapping') + slangle + \
                          delimitedList(Group(simple_type + opt_id)) + srangle

        struct_item = Group(simple_type + identifier + ssemi)
        type_struct = comment_opt + struct_ + slbrace + \
                      OneOrMore(struct_item) + srbrace
        # Full 'typedef' grammar
        full_typedef = Group(simple_type ^ type_struct).setResultsName(
            'typedef')
        typedef_name = identifier.setResultsName('name')
        typedef_def = Group(comment_opt + typedef_ + full_typedef +
                            typedef_name + ssemi)

        # -- Function definitions --
        params = Group(delimitedList(Group(simple_type + opt_id))
                       | empty).setResultsName('params')
        rval = delimitedList(Group(simple_type + opt_id)).setName('rval')
        auth = Group(auth_ + req_).setName('auth')
        func_name = identifier.setResultsName('name')
        func_def = Group(comment_opt + func_ + func_name + lparen + params + rparen +
                         return_ + lparen + rval + rparen + Optional(auth) +
                         ssemi + comment_opt).setResultsName('funcdef')

        # -- Module definition --
        module_item = typedef_def | func_def
        module_name = identifier.setResultsName('name')
        module_def = Group(comment_opt + module_ + module_name + slbrace +
                           ZeroOrMore(module_item) +
                           srbrace)

        # -- Grammar --
        bnf = OneOrMore(module_def)
        singleLineComment = '//' + restOfLine
        bnf.ignore(singleLineComment)
        self._bnf = bnf

def extract_comment(c):
    c = re.sub('^\s*/\*+\s*', '', c)  # leading /**
    c = re.sub('\s*\*+/', '', c)  # trailing */
    c = re.sub('\s*\*\s*', ' ', c)  # linebreak + *
    c = re.sub('\s+', ' ', c)
    return c.strip()

class Definition(object):
    """One definition in a module.

    Common attributes:
        - module (str): Name of module
        - comment (str): Comment for module (may be empty)
        - type (str): Type of definition, see DEF_TYPES
        - name (str): Name of defined function or type
        - is_fn (bool): True iff this is a function definition
    """
    DEF_TYPES = 'funcdef', 'typedef'

    def __init__(self, module, defn):
        """Create new definition.

        Args:
          - module (str): name of containing module
          - defn (list): Parsed definition data
        """
        self.module = module
        self._defn = defn
        self.comment = ''
        offs = 0
        if self._defn[0].startswith('/*'):
            self.comment = extract_comment(self._defn[0])
            offs = 1
        self.type = self._defn[offs]
        self.is_fn = self.type == self.DEF_TYPES[0]
        if self.is_fn and self._defn.get('struct', None):
            self.name = self._defn['struct']['name']
        else:
            self.name = self._defn.get('name','')

        self._get_fn_attrs() if self.is_fn else self._get_type_attrs()

    def _get_fn_attrs(self):
        """Extract additional attributes for function definition."""
        #print("** Get params for {}".format(self.name))
        self.params = []
        for p in self._defn.get('params'):
            ptype = get_ktype(p)
            self.params.append(ptype)

    def _get_type_attrs(self):
        """Extract additional attributes for type definition."""
        tdef = self._defn.get('typedef')
        print("** type: {}".format(tdef))

    def __str__(self):
        if self.is_fn:
            prm = ', '.join([str(p) for p in self.params])
            s = "({}) {} {}({}) -- {}".\
                format(self.module, self.type, self.name, prm, self.comment)
        else:
            s = "({}) {} {} -- {}".format(self.module, self.type,
                                          self.name, self.comment)
        return s

def get_ktype(x):
    if isinstance(x, str):
        return KUser(x)
    t, args = x[0], x[1:]
    if t == 'list':
        return KList(*args)
    elif t == 'mapping':
        return KMapping(*args)
    elif t == 'tuple':
        return KTuple(*args)
    # XXX: other known types here
    else:
        return KPrimitive(*x)
        #raise ValueError('Unknown type: {}'.format(t))

class KType(object):
    def __init__(self, var):
        self.var = var

    def var_str(self):
        return ' ' + self.var if self.var else ''

class KList(KType):
    def __init__(self, subtype, var=''):
        KType.__init__(self, var)
        self.item_type = get_ktype(subtype)

    def __str__(self):
        return 'list<{}>{}'.format(self.item_type, self.var_str())

class KTuple(KType):
    def __init__(self, *subtypes):
        KType.__init__(self, '')
        self.types = map(get_ktype, subtypes)

    def __str__(self):
        tt = ', '.join([str(t) for t in self.types])
        return 'tuple<{}>{}'.format(tt, self.var_str())

class KMapping(KType):
    def __init__(self, key, val, var=''):
        KType.__init__(self, var)
        self.key_type = get_ktype(key)
        self.val_type = get_ktype(val)

    def __str__(self):
        return 'map<{}:{}>{}'.format(self.key_type, self.val_type,
                                     self.var_str())

class KPrimitive(KType):
    def __init__(self, name, var=''):
        KType.__init__(self, var)
        self.name = name

    def __str__(self):
        return '{}{}'.format(self.name, self.var_str())

class KUser(KType):
    def __init__(self, name, var=''):
        KType.__init__(self, var)
        self.name = name

    def __str__(self):
        return '{}{}'.format(self.name, self.var_str())

def main():
    import argparse, os
    prs = argparse.ArgumentParser()
    prs.add_argument('filename')
    args = prs.parse_args()
    #
    path = os.path.expanduser(args.filename)
    s = open(path).read()
    spec = Specification(s)
    #print("Full spec:\n{}\n".format(spec))
    for m in spec.definitions:
        print("{}\n".format(m))

def __test():
    for t in __test_data:
       print("---")
       print(Specification(t))

if __name__ == '__main__':
    try:
        main()
        #__test()
    except ParseException as err:
        print('ERROR: {}\n{}\n{}^'.format(err, err.line, ' ' * (err.col - 1)))