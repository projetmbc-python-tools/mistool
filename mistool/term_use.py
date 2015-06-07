#!/usr/bin/env python3

"""
prototype::
    date = 2015-06-05


This module contains mainly classes and functions producing strings useful to be
printed in a terminal.
"""

from mistool.os_use import PPath, \
                           _XTRA, _FILE, _DIR, \
                           _FILE_DIR_QUERIES, \
                           OTHER_FILES_TAG, EMPTY_DIR_TAG

from mistool.latex_use import escape as latex_escape

from mistool.config.frame import FRAMES_FORMATS, _ABREVS_FRAMES, _KEYS_FRAME


# ------------------- #
# -- DECORATE TEXT -- #
# ------------------- #

DEFAULT_FRAME = FRAMES_FORMATS['python_basic']

def _draw_hrule(
    rule,
    left,
    right,
    lenght,
    nbspace
):
    """
    prototype::
            arg    = str: lang = DEFAULT_LANG ;
                     ????
            return = str ;
                     ????





-----------------
Small description
-----------------

This function is used to draw the horizontal rules of a frame around one text.


-------------
The arguments
-------------

This function uses the following variables.

    1) ``rule`` is the character used to draw the rule.

    2) `left``�and ``right`` are the first and last additional texts used around
    the rule.

    3) ``lenght`` is an integer giving the lenght of the rule.

    4) ``nbspace`` is the number of spaces to add before the first additional
    text (this is for cases when left corners have different lenghts).
    """
    if rule:
        return [
            ' '*(nbspace - len(left))
            + left
            + rule*lenght
            + right
        ]

    elif left:
        return [
            left
            + ' '*lenght
            + right
        ]

    elif right:
        return [
            ' '*(nbspace + lenght)
            + right
        ]

    else:
        return []

def frame(
    text,
    format = DEFAULT_FRAME,
    center = True
):
    """

    prototype::
        arg    = str: lang = DEFAULT_LANG ;
                 ????
        return = str ;
                 ????




--------------
Default frames
--------------

This function makes it possible to put one text into one frame materialized by
ASCII characters. This can be usefull for console outputs or for pretty comments
in listings like the following python comment.

python::
    #############
    # one       #
    # comment   #
    # easily    #
    # formatted #
    #############


This text has been produced using the following lines.

python::
    from mistool import string_use

    oneText = '''one
    comment
    easily
    formatted'''

    print(
        string_use.frame(
            text   = oneText,
            center = False
        )
    )


By default, ``center`` is equal ``True`` which asks to merely center the content
of the frame. Here we use the default frame ``DEFAULT_FRAME`` which is equal to
``FRAMES_FORMATS['python_basic']``. The dictionary ``FRAMES_FORMATS`` contains all
the default formats. For example, in the following code we use another default
formats.

python::
    from mistool import string_use

    oneText = '''one
    comment
    with C-like
    style'''

    print(
        string_use.frame(
            text   = oneText,
            format = string_use.FRAMES_FORMATS['c_basic'],
            center = False
        )
    )


This will give the following output.

code_c::
    /***************
     * one         *
     * comment     *
     * with C-like *
     * style       *
     ***************/


---------------
Homemade frames
---------------

The following frame can be obtained by using the default format
``string_use.FRAMES_FORMATS['python_pretty']``.

python::
    # ------------- #
    # -- one     -- #
    # -- pretty  -- #
    # -- comment -- #
    # ------------- #


Let see the definition ``FRAMES_FORMATS['python_pretty']``.

python::
    {
        'rule': {
            'down': '-',
            'left': '--',
            'right': '--',
            'up': '-'
        },
        'extra': {
            'rule': {
                'left': '#',
                'right': '#'
            }
        }
    }


In this dictionary, we define a frame and then an extra frame. Indeed, you can
use a dictionary looking like the one above. A missing key is a shortcut to
indicate an empty string.

python::
    {
        'rule' : {
            'up'   : "Single character",
            'down' : "Single character",
            'left' : "Some characters",
            'right': "Some characters"
        },
        'corner': {
            'leftup'   : "Some characters",
            'leftdown' : "Some characters",
            'rightup'  : "Some characters",
            'rightdown': "Some characters"
        },
        'extra': {
            'rule' : {
                'up'   : "Single character",
                'down' : "Single character",
                'left' : "Some characters",
                'right': "Some characters"
            },
            'corner': {
                'leftup'   : "Some characters",
                'leftdown' : "Some characters",
                'rightup'  : "Some characters",
                'rightdown': "Some characters"
            },
        }
    }


You can use the following abreviations for the positional keys.

    * ``u``, ``d``, ``l`` and ``r`` are abreviations for ``up``, ``down``,
    ``left`` and ``right`` respectively.

    * ``lu``, ``ld``, ``ru`` and ``rd`` are abreviations for ``leftup``,
    ``leftdown``, ``rightup`` and ``rightdown`` respectively.


-------------
The arguments
-------------

This function uses the following variables.

    1) ``text`` is a string value corresponding to the text to put in a frame.

    2) ``center`` is a boolean variable to center or not the text inside the
    frame. By default, ``center = True``.

    3) ``format`` is an optional dictionary defining the frame. By default,
    ``format = DEFAULT_FRAME`` which is equal to
    ``FRAMES_FORMATS['python_basic']``.

    info::
        All the default formats are in the dictionary ``FRAMES_FORMATS``.


    The general structure of a dictionary to use with ``format`` is the following
    one.
    """
# Default values must be chosen if nothing is given.
    if not set(format.keys()) <= {'rule', 'corner', 'extra'}:
        raise ValueError("illegal key for the dictionary << format >>.")

    for kind in ['rule', 'corner', 'extra']:
        if kind not in format:
            format[kind] = {}


    for kind in ['rule', 'corner']:
        if not set(format[kind].keys()) <= _KEYS_FRAME[kind]:
            raise ValueError(
                "illegal key for the dictionary << format >>. "
                "See the kind << {0} >>.".format(kind)
            )

        for key, abrev in _ABREVS_FRAMES[kind].items():
            if abrev in format[kind] and key in format[kind]:
                message = "use of the key << {0} >> and its abreviation " \
                        + "<< {1} >> for the dictionary << format >>."

                raise ValueError(message.format(key, abrev))

            if abrev in format[kind]:
                format[kind][key] = format[kind][abrev]

            elif key not in format[kind]:
                format[kind][key] = ""

# Horizontal rules can only use one single character.
    for loc in ['up', 'down']:
        if len(format['rule'][loc]) > 1:
            message = "You can only use nothing or one single character " \
                    + "for rules.\nSee << {0} >> for the {1} rule."

            raise ValueError(
                message.format(format['rule'][loc], loc)
            )

# Infos about the lines of the text.
    lines     = [oneline.rstrip() for oneline in text.splitlines()]
    nbmaxchar = max([len(oneline) for oneline in lines])

# Space to add before vertical rules.
    nbspace = max(
        len(format['corner']['leftup']),
        len(format['corner']['leftdown'])
    )

    spacetoadd = ' '*nbspace

# Text decoration for vertical rules
    if format['rule']['left']:
        leftrule = format['rule']['left'] + ' '
    else:
        leftrule = ''

    if format['rule']['right']:
        rightrule = ' ' + format['rule']['right']
    else:
        rightrule = ''

# Length of the rule without the corners
    lenght = nbmaxchar + len(leftrule) + len(rightrule)

# First line of the frame
    answer = _draw_hrule(
        rule    = format['rule']['up'],
        left    = format['corner']['leftup'],
        right   = format['corner']['rightup'],
        lenght  = lenght,
        nbspace = nbspace
    )

# Management of the lines of the text
    for oneline in lines:
        nbmissingspaces = nbmaxchar - len(oneline)

# Space before and after one line of text.
        if center:
            if nbmissingspaces % 2 == 1:
                spaceafter = ' '
            else:
                spaceafter = ''

            nbmissingspaces = nbmissingspaces // 2

            spacebefore = ' '*nbmissingspaces
            spaceafter += spacebefore

        else:
            spacebefore = ''
            spaceafter = ' '*nbmissingspaces

        answer.append(
            spacetoadd
            +
            '{0}{1}{2}{3}{4}'.format(
                leftrule,
                spacebefore,
                oneline,
                spaceafter,
                rightrule
            )
        )

# Last line of the frame
    answer += _draw_hrule(
        rule    = format['rule']['down'],
        left    = format['corner']['leftdown'],
        right   = format['corner']['rightdown'],
        lenght  = lenght,
        nbspace = nbspace
    )

    answer = '\n'.join([x.rstrip() for x in answer])

# Does we have an extra frame ?
    if format['extra']:
        try:
            answer = frame(
                text   = answer,
                format = format['extra'],
                center = center
            )

        except ValueError as e:
            raise ValueError(
                str(e)[:-1] + " in the definition of the extra frame."
            )

# All the job has been done.
    return answer





# ------------------ #
# -- STEP BY STEP -- #
# ------------------ #

class Step:
    """

    prototype::
        arg    = str: lang = DEFAULT_LANG ;
                 ????
        return = str ;
                 ????





-----------------
Small description
-----------------

This class displays texts for step by step actions. The numbering of the steps
is automatically updated and displayed.


-------------
The arguments
-------------

There are two optional variables.

    1) ``nb`` is the number of the current step. When the class is instanciated,
    the default value is ``1``.

    2) ``deco`` indicates how to display the numbers. When the class is
    instanciated, the default value is ``""1)""`` where ``1`` symbolises the
    numbers.
    """
    def __init__(
        self,
        nb   = 1,
        deco = "1)"
    ):
        self.nb   = nb
        self.deco = deco.replace('1', '{0}')

    def print(
        self,
        text,
        deco
    ):
        """
            prototype::
                arg    = str: lang = DEFAULT_LANG ;
                         ????
                return = str ;
                         ????




-----------------
Small description
-----------------

This method simply prints ``deco`` the text of the actual numbering, and then
``text`` the content of the actual step.

You can redefine this method for finer features.


-------------
The arguments
-------------

This method uses the following variables.

    1) ``text`` is simply the text of the actual step.

    2) ``deco`` is a string corresponding to the text indicated what is the
    actual step number.
        """
        print(
            deco,
            text,
            sep = " "
        )

    def display(
        self,
        text
    ):
        """

            prototype::
                arg    = str: lang = DEFAULT_LANG ;
                         ????
                return = str ;
                         ????



-----------------
Small description
-----------------

This method simply calls the method ``self.print`` so as to print the
informations contained in the variable ``text``, and then ``self.nb`` is
augmented by one unit.

You can redefine the method ``self.print`` for finer features.


-------------
The arguments
-------------

This method uses one variable ``text`` which is the text of the actual step.
        """
        self.print(
            text = text,
            deco = self.deco.format(self.nb)
        )

        self.nb += 1











# ----------------------- #
# -- VIEWS OF A FOLDER -- #
# ----------------------- #

class DirView:
    r"""
prototype::
    type = cls ;
           this class allows to display in different formats the tree structure
           of one directory with the extra possibility to keep and show only
           some informations, and also to set a little the format of the output
    see  = os_use._ppath_regpath2meta, os_use._ppath_walk

    arg-attr = os_use.PPath: ppath ;
               this argument is the path of the directory to analyze
    arg-attr = str: regpath = "**" ;
               this argument follows some rules named "regpath" rules so as to
               choose the files and the directories that must be kept (see the
               documentation of ``os_use._ppath_regpath2meta``)
    arg-attr = str: display = "main short" in self._FORMATS;
               this argument gives informations about the output to produce (you
               can just use the initials of the options)
    arg-attr = str: sorting = "alpha" in [x[0] for x in cls.LAMBDA_SORT]
                                      or in [x[1] for x in cls.LAMBDA_SORT];
               this argument inidcates the way to sort the paths found

    clsattr = {(str, str): (lambda, ?)}: LAMBDA_SORT ;
              this attribut of class, and not of one of its instance, defines
              how to sort the paths (see the end of the documentation above)


===================================
The directory used for the examples
===================================

All of the following examples will use a folder with the structure above and
having the whole path path::``/Users/projetmbc/dir``.

dir::
    + dir
        * code_1.py
        * code_2.py
        * file_1.txt
        * file_2.txt
        + doc
            * code_A.py
            * code_B.py
            * slide_A.pdf
            * slide_B.pdf
            + licence
                * doc.pdf
        + emptydir


==============
The ascii tree
==============

Let's start with the default output for the ¨ascii tree. In the following code,
in the text printed, the files and the folders are sorting regarding their names
(this text follows the syntax used to generate the view of the folders used in
the documentation that you are reading).

pyterm::
    >>> from mistool.term_use import DirView, PPath
    >>> dir     = PPath("/Users/projetmbc/dir")
    >>> dirview = DirView(dir)
    >>> print(dirview.ascii)
    + dir
        * code_1.py
        * code_2.py
        + doc
            * code_A.py
            * code_B.py
            + licence
                * doc.pdf
            * slide_A.pdf
            * slide_B.pdf
        + emptydir
        * file_1.txt
        * file_2.txt


You can ask to have the files before the folders and also to have the relative
paths instead of the names. This needs to use the arguments ``display`` and
``sorting``. Here is an example of use where we must add the option ``"main"``
for ``display`` so as to see the main folder.

pyterm::
    >>> from mistool.term_use import DirView, PPath
    >>> dir     = PPath("/Users/projetmbc/dir")
    >>> dirview = DirView(
    ...     ppath   = dir,
    ...     display = "main relative",
    ...     sorting = "filefirst"
    ... )
    >>> print(dirview.ascii)
    + dir
        * code_1.py
        * code_2.py
        * file_1.txt
        * file_2.txt
        + doc
            * doc/code_A.py
            * doc/code_B.py
            * doc/slide_A.pdf
            * doc/slide_B.pdf
            + doc/licence
                * doc/licence/doc.pdf
        + emptydir


info::
    All the available formattings are given later in this section of the
    documentation.


Let's see a last example using the argument ``regpath``. The following code
asks to keep only the files with the extension path::``py``. You can see that
the empty folders are given, and that the other files than the ones wanted are
indicated by ellipsis, this ones being always sorted at the end of the files.

pyterm::
    >>> from mistool.term_use import DirView, PPath
    >>> dir     = PPath("/Users/projetmbc/dir")
    >>> dirview = DirView(
    ...     ppath   = dir,
    ...     regpath = "file::**.py"
    ... )
    >>> print(dirview.ascii)
    + dir
        * code_1.py
        * code_2.py
        + doc
            * code_A.py
            * code_B.py
            + licence
                * ...
            * ...
        + emptydir
        * ...


If you use the option ``display = "main short found"`` instead of the default
one ``display = "main short"``, then the output will only show the files found
as above, and the empty folders will not be given.

pyterm::
    >>> from mistool.term_use import DirView, PPath
    >>> dir     = PPath("/Users/projetmbc/dir")
    >>> dirview = DirView(
    ...     ppath   = dir,
    ...     regpath = "file::**.py",
    ...     display = "main short found"
    ... )
    >>> print(dirview.ascii)
    + dir
        * code_1.py
        * code_2.py
        + doc
            * code_A.py
            * code_B.py


info::
    The documentation of the function ``_ppath_regpath2meta`` gives all the
    ¨infos needed to use the regpaths.


=======================
The "ruled" tree output
=======================

By default, ``DirView.tree`` give a tree view using rules similar to the ones
you can see in ¨gui applications displaying tree structure of a folder. Here we
use only ¨utf8 characters.

term::
    ╸dir
     ┣━ ╸code_1.py
     ┣━ ╸code_2.py
     ┣━ ╸file_1.txt
     ┣━ ╸file_2.txt
     ┣━ ╸doc
     ┃   ┣━ ╸code_A.py
     ┃   ┣━ ╸code_B.py
     ┃   ┣━ ╸slide_A.pdf
     ┃   ┣━ ╸slide_B.pdf
     ┃   ┗━ ╸licence
     ┃       ┗━ ╸doc.pdf
     ┗━ ╸emptydir


=====================
The "toc" like output
=====================

Using ``DirView.toc`` with the sorting option ``sorting = "filefirst"``, this is
the better sorting option here, you will obtain the following output which looks
like a kind of table of contents with sections for folders, and subsections for
files.

term::
    + dir
        * code_1.py
        * code_2.py
        * file_1.txt
        * file_2.txt

    + dir/doc
        * code_A.py
        * code_B.py

    + dir/doc/licence
        * doc.pdf
        * slide_A.pdf
        * slide_B.pdf

    + dir/emptydir


warning::
    Here all the paths for the folders will be always displayed as relative
    ones to the parent directory of the folder analyzed, and not to the folder
    analyzed. Paths formatting options apply only to files.


===================================================
A ¨latex version for the package latex::``dirtree``
===================================================

By default, using ``DirView.latex`` you will have the following ¨latex code
than can be formated by the ¨latex package latex::``dirtree``.

latex::
    \dirtree{%
      .1 {dir}.
        .2 {code\_1.py}.
        .2 {code\_2.py}.
        .2 {doc}.
          .3 {code\_A.py}.
          .3 {code\_B.py}.
          .3 {licence}.
            .4 {doc.pdf}.
          .3 {slide\_A.pdf}.
          .3 {slide\_B.pdf}.
        .2 {emptydir}.
        .2 {file\_1.txt}.
        .2 {file\_2.txt}.
    }


info::
    As you can see, special ¨latex characters are managed by the class
    ``DirView``. In our example, ``_`` becomes latex::``\_``.


=======================
All the display options
=======================

The optional string argument ``display``, or the attribut with the same name
``display``, can be made of one or several of the following values separated by
spaces where each name can be replaced by its initial.

    a) ``long`` asks to display the whole paths of the files and directories
    found.

    b) ``relative`` asks to display relative paths comparing to the main
    directory analysed.

    c) ``short`` asks to only display names of directories found, and of the
    files found with their extensions.

    d) ``main`` asks to display the main directory which is analyzed.

    e) ``found`` asks to only display directories and files with a path matching
    the pattern ``regpath``. If ``found`` is not given, then ellipsis will be
    used to indicate unmatching files and the empty directory will be always
    given.


=======================
All the sorting options
=======================

The optional string argument ``sorting``, or the attribut with the same name
``sorting``, can be one of the following values (each name can be replaced by
its initial).

    a) ``alpha`` is the alphabetic sorting on the strings representing the paths.

    b) ``filefirst`` gathers first the files and then the folders, and in each
    of this category an alphabetic sorting is applied.

    c) ``name`` first sorts the objects regarding only their name without the
    extension, and if a file and a folder have the same position, then the file
    will be put before the directory.

    d) ``date`` simply used the date of the last physical changes.


info::
    For all the options above, the unmatching files indicated with "..." are
    always sorted at the end.


info::
    You can add sortings by redefining the attribut of class ``LAMBDA_SORT``
    which by default is the following dictionary.

    python::
        LAMBDA_SORT = {
            ("alpha", "a"): [
                lambda x: str(x['ppath']),
                'z'*500
            ],
            ("name", "n"): [
                lambda x: (
                    str(x['ppath'].stem),
                    int("dir" in x['kind'])
                ),
                ('z'*500, 0)
            ],
            ("filefirst", "f"): [
                lambda x: (
                    int("dir" in x['kind']),
                    str(x['ppath'])
                ),
                (0, 'z'*500)
            ],
            ("date", "d"): [
                lambda x: -x['ppath'].stat().st_mtime,
                float('inf')
            ],
        }

     This dictionary uses the following conventions.

        1) The keys are tuples ``(name, shortcut)`` of two strings.

        2) The values are lists of two elements.

            a) The ¨1ST element is a lambda function that will give the values
            used for the sorting.
            Here ``x`` is a dictionary stored in ``self.listview`` (see the
            documentation of the method ``self.buildviews``).

            b) The ¨2ND element is the special value used for the sorting when
            special ellipsis ``"..."`` is met (ellipsis are used to indicate
            unmatching files).
    """
    FILE_KINDS = ['file', 'other_files']
    DIR_KINDS  = ['dir', 'content_dir', 'empty_dir']

    ASCII_DECOS = {
        k: v
        for v, keys in {
            "+"  : DIR_KINDS,
            "*"  : FILE_KINDS,
            " "*4: ['tab'],
        }.items()
        for k in keys
    }

# Source for the rules:
#     * http://en.wikipedia.org/wiki/Box-drawing_character#Unicode

    UTF8_DECOS = {
# Horizontal and vertical rules
        'hrule': "\u2501", #--->  ━
        'vrule': "\u2503", #--->  ┃
# First, last, horizontal and vertical nodes
        'fnode': "\u250F", #--->  ┏
        'lnode': "\u2517", #--->  ┗
        'vnode': "\u2523", #--->  ┣
# Decorations
        'deco': "\u2578",  #--->  ╸
    }

    LAMBDA_SORT = {
        ("alpha", "a"): [
            lambda x: str(x['ppath']),
            'z'*500
        ],
        ("name", "n"): [
            lambda x: (
                str(x['ppath'].stem),
                int("dir" in x['kind'])
            ),
            ('z'*500, 0)
        ],
        ("filefirst", "f"): [
            lambda x: (
                int("dir" in x['kind']),
                str(x['ppath'])
            ),
            (0, 'z'*500)
        ],
        ("date", "d"): [
            lambda x: -x['ppath'].stat().st_mtime,
            float('inf')
        ],
    }

# Additional paths
    _ONLY_FOUND_PATHS, _MAIN_PATH = "found", "main"

# Formattings of the paths
    _LONG_PATH, _REL_PATH, _SHORT_PATH = "long", "relative", "short"
    _FORMATS = set([
        _LONG_PATH, _MAIN_PATH, _ONLY_FOUND_PATHS, _REL_PATH, _SHORT_PATH
    ])
    _PATH_FORMATS = set([_LONG_PATH, _REL_PATH, _SHORT_PATH])

# Special query
    _INTERNAL_QUERIES = set([_XTRA, _FILE, _DIR])

    def __init__(
        self,
        ppath,
        regpath = "**",
        display = "main short",
        sorting = "alpha"
    ):
# General settings
        self._mustberebuilt = True

        self._LAMBDA_SORT_LONGNAMES = {
            k[0]: v for k, v in self.LAMBDA_SORT.items()
        }

        self._sorting_long_names = {x[1]: x[0] for x in self.LAMBDA_SORT}

        self._display_long_names = {x[0]: x for x in self._FORMATS}

# Verifications are done by the build method !
        self.ppath   = ppath
        self.regpath = regpath
        self.display = display
        self.sorting = sorting


# --------------------- #
# -- SPECIAL SETTERS -- #
# --------------------- #

    @property
    def ppath(self):
        return self._ppath

    @ppath.setter
    def ppath(self, value):
# Do we have a folder ?
        if not value.is_dir():
            raise OSError("``ppath`` doesn't point to a directory.")

        self._ppath         = value
        self._mustberebuilt = True


    @property
    def regpath(self):
        return self._regpath

    @regpath.setter
    def regpath(self, value):
        self._regpath       = value
        self._mustberebuilt = True


    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, value):
        self._display = set(
            self._display_long_names.get(x.strip(), x.strip())
            for x in value.split(" ")
            if x.strip()
        )

        if not self._display <= self._FORMATS:
            raise ValueError("illegal formatting rule (see ``display``).")

        nb_path_formats = len(self._display & self._PATH_FORMATS)

        if nb_path_formats == 0:
            self._display.add(_SHORT_PATH)

        elif nb_path_formats != 1:
            raise ValueError(
                "several path formatting rules (see ``display``)."
            )

        self._mustberebuilt = True


    @property
    def sorting(self):
        return self._sorting

    @sorting.setter
    def sorting(self, value):
        self._sorting = self._sorting_long_names.get(value, value)

        if self._sorting not in self._LAMBDA_SORT_LONGNAMES:
            raise ValueError("unknown sorting rule.")

        self._mustberebuilt = True

# -------------------- #
# -- INTERNAL VIEWS -- #
# -------------------- #

    def buildviews(self):
        """
prototype::
    see    = self.sort , self.ascii , self.latex , self.toc , self.tree
    action = this method builds one flat list ``self.listview`` of dictionaries,
             that store all the informations about the directory even the empty
             folders and the unmatching files,
             and also ``self.treeview`` another list of dictionaries which is
             like the natural tree structure of the folder analyzed
             (both of this objects are sorted regarding to the value of the
             attribut ``self.sorting``)


======================================
Dictionaries used in ``self.listview``
======================================

The dictionaries look like the following one. You must know this structure if
you want to define your own kind of sorting for the output.

python::
    {
        'kind' : "dir" or "file",
        'depth': relative depth,
        'ppath': the whole path of one directory or file found
                 (this can also be an extra path)
    }


info::
    The property like method ``self.ascii`` works iteratively with the
    argument ``self.listview``.


==================================
The structure of ``self.treeview``
==================================

This list contains the dictionnaries of the only first level object but for
folder a key ``'content'`` is added whose value is a list of dictionnaries
associated to its content and so on...


info::
    The property like method ``self.tree`` works recursively with the argument
    ``self.treeview``.
        """
# Regpath infos
        queries, pattern = self.ppath.regpath2meta(
            self.regpath,
            regexit = False
        )

        allqueries = queries | self._INTERNAL_QUERIES
        allregpath = "{0}::{1}".format(" ".join(allqueries), pattern)

        self._extradepth = int(self._MAIN_PATH in self._display)

        self._all_listview = [
            self._metadatas(x)
            for x in self.ppath.walk(allregpath)
        ]

        self._filedir_queries = queries & _FILE_DIR_QUERIES

# We can now do the job.
        self._build_listview()
        self._build_treeview()

        self.sort()

        self._mustberebuilt = False


    def _metadatas(self, ppath):
        """
prototype::
    return = dict ;
             the dictionnary stores the path, its depth and the kind of object
             pointed by the path
             (this is for the elements in ``self.listview`` and partially for
             ``self.treeview``)
        """
        if ppath.name == EMPTY_DIR_TAG:
            kind  = "empty_dir"
            ppath = ppath.parent

        elif ppath.name == OTHER_FILES_TAG:
            kind  = "other_files"
            ppath = ppath.parent / "..."

        elif ppath.is_dir():
            kind = "dir"

        else:
            kind = "file"

        metadatas = {
            'kind' : kind,
            'depth': ppath.depth_in(self.ppath) + self._extradepth,
            'ppath': ppath
        }

        return metadatas


    def _build_listview(self):
        """
prototype::
    see    = self.buildviews
    action = the attribut ``self.listview`` is build using the attribut
             ``self._all_listview``
        """
# Sub fles and folders found
        addall    = bool(self._ONLY_FOUND_PATHS not in self._display)
        _listview = []

        for metadatas in self._all_listview:
            if metadatas['kind'] in ["empty_dir", "other_files"]:
                if addall:
                    _listview.append(metadatas)

            elif metadatas['kind'] in self._filedir_queries:
                _listview.append(metadatas)

        _listview.sort(key = lambda x: str(x['ppath']))

# We have to find folders with only unmacthing files or with matching and
# unmacthing files, and also all the parent directories.
#
# Main or not main, that is the question.
        if self._MAIN_PATH in self._display:
            self.listview = [{
                'kind' : 'dir',
                'depth': 0,
                'ppath': self.ppath
            }]
            lastreldirs   = [PPath('.')]

        else:
            self.listview = []
            lastreldirs   = []

        for i, metadatas in enumerate(_listview):
            relpath = metadatas['ppath'].relative_to(self.ppath)
            parents = relpath.parents

# We have to add all the parent directories !
            if "dir" in metadatas['kind']:
                lastreldirs.append(metadatas['ppath'].relative_to(self.ppath))

            else:
                for parent in reversed(parents):
                    if parent not in lastreldirs:
                        ppath = self.ppath / parent

                        self.listview.append({
                            'kind' : 'dir',
                            'depth': ppath.depth_in(self.ppath) \
                                     + self._extradepth,
                            'ppath': ppath
                        })

                        lastreldirs.append(parent)

            self.listview.append(metadatas)


    def _build_treeview(self):
        """
prototype::
    see    = self.buildviews , self._rbuild_treeview
    action = this method returns the attribut ``self.treeview`` but all the
             job is done recursively by the method ``self._rbuild_treeview``
        """
        self.treeview = self._rbuild_treeview(self.listview)


    def _rbuild_treeview(self, listview):
        """
prototype::
    action = the attribut ``self.treeview`` is build recursively using first
             the attribut ``self.listview``
        """
        i    = 0
        imax = len(listview)

        treeview = []

        while(i < imax):
            metadatas = listview[i]

# Simply a file.
            if 'file' in metadatas['kind']:
                treeview.append(metadatas)
                i += 1

# For a directory, we have to catch its content that will be analyzed
# recursively.
            else:
                depth   = metadatas['depth']
                content = []
                i += 1

                while(i < imax):
                    submetadatas = listview[i]
                    subdepth     = submetadatas['depth']

                    if subdepth > depth:
                        content.append(submetadatas)
                        i += 1

                    else:
                        break

                if content:
                    metadatas['content'] = self._rbuild_treeview(content)

                else:
                    metadatas['content'] = []

                treeview.append(metadatas)

        return treeview


# ------------- #
# -- SORTING -- #
# ------------- #

    def _ellipsis_sort(self, metadatas):
        """
prototype::
    arg    = dict: metadatas
    see    = self.buildviews , self._metadatas
    return = str ;
             the value to use for the sorting
        """
        if metadatas['ppath'].name == "...":
            return self._ellipsi_sort_value

        else:
            return self._lambda_sort(metadatas)


    def sort(self):
        """
prototype::
    see    = self._rsort
    action = this method sorts the attribut ``self.treeview`` regarding to the
             value of the attribut ``self._sorting``, this job being done
             recursively by the method ``self._rsort``, and then the list
             ``self.listview`` is rebuild using the new ``self.treeview``
             (this is uggly but this allows to easily defined the methods of
             sorting, and this is easy to code)
        """
        self._lambda_sort        = self._LAMBDA_SORT_LONGNAMES[self.sorting][0]
        self._ellipsi_sort_value = self._LAMBDA_SORT_LONGNAMES[self.sorting][1]

# Each new sorting
        self.outputs = {}

# We sort ifirst the treeview (that allows to define natural sorintgs).
        self.treeview = self._rsort(self.treeview)

# We have to go back to ``self.listview`` !
        self.listview = self._rtree_to_list_view(self.treeview)


    def _rsort(self, treeview):
        """
prototype::
    arg    = list(dict): treeview
    see    = self.buildviews , self._metadatas , self._ellipsis_sort
    return = list(dict) ;
             the treeview sorting regarding to the value of ``self._sorting``
             (the job is done recursively)
        """
        treeview.sort(key = self._ellipsis_sort)

        for i, metadatas in enumerate(treeview):
            if 'content' in metadatas:
                metadatas['content'] = self._rsort(metadatas['content'])
                treeview[i] = metadatas

        return treeview


    def _rtree_to_list_view(self, treeview):
        """
prototype::
    see    = self.sort
    arg    = list(dict): treeview
    return = list(dict) ;
             the listview associated to ``self.treeview`` (the job is done
             recursively)
        """
        listview = []

        for metadatas in treeview:
            if 'content' in metadatas:
                content = metadatas['content']

# << Warning ! >> We can't use ``del metadatas['content']`` because this will
# always change self.treeview (we could have used a deepcopy but this  would
# be not efficient).
                newmetadatas = {}

                for k, v in metadatas.items():
                    if k != "content":
                        newmetadatas[k] = v

                listview.append(newmetadatas)
                listview += self._rtree_to_list_view(content)

            else:
                listview.append(metadatas)

        return listview


# ------------ #
# -- OUPUTS -- #
# ------------ #

    def havetobuild(self, kind):
        """
prototype::
    return = bool ;
             ``True`` only if the output have to be remade (in that case the
             method ``self.buildviews`` is called if it is necessary)
        """
        if self._mustberebuilt:
            self.buildviews()

        return kind not in self.outputs


    def pathtoprint(self, metadatas):
        """
prototype::
    arg    = dict: metadatas
    return = str ;
             the string to print for a path
        """
# << Warning ! >> The paths are whole ones by default !
        kind  = metadatas["kind"]
        ppath = metadatas["ppath"]
        name  = ppath.name

        if name == "..." or self._SHORT_PATH in self._display:
            strpath = name

        elif self._REL_PATH in self._display:
            if ppath == self.ppath:
                strpath = name

            else:
                strpath = str(ppath.relative_to(self.ppath))

        else:
            strpath = str(ppath)

        return strpath


    @property
    def ascii(self):
        """
prototype::
    type   = property
    return = str ;
             a basic tree using only ¨ascii characters
        """
# The job has to be done.
        if self.havetobuild('ascii'):
            text = []

            for metadatas in self.listview:
                depth = metadatas["depth"]
                tab   = self.ASCII_DECOS['tab']*depth

                decokind    = self.ASCII_DECOS[metadatas["kind"]]
                pathtoprint = self.pathtoprint(metadatas)

                text.append(
                    "{0}{1} {2}".format(tab, decokind, pathtoprint)
                )

            self.outputs['ascii'] = '\n'.join(text)

# The job has been done.
        return self.outputs['ascii']


    @property
    def tree(self):
        """
prototype::
    see    = self._rtree
    type   = property
    return = str ;
             a tree using special ¨unicode characters such as to draw some
             additional rules
        """
# The job has to be done.
        if self.havetobuild('tree'):
# One dir or file alone (extra prossibilty)
            if len(self.listview) == 1:
                self.outputs['tree'] = "{0} {1}".format(
                    self.UTF8_DECOS['hrule'],
                    self.pathtoprint(self.listview[0])
                )

            else:
# Ugly patch !!!
                self.outputs['tree'] = "\n".join([
                    x[4:]
                    for x in self._rtree(self.treeview)
                ])

# The job has been done.
        return self.outputs['tree']


    def _rtree(self, treeview):
        """
prototype::
    return = str ;
             the lines of the tree that uses ¨unicode characters to draw some
             additional rules
        """
        lines       = []
        imax        = len(treeview) - 1
        thisdepth   = treeview[0]['depth']

        if thisdepth <= 3:
            subtabdepth = 0

        else:
            subtabdepth = thisdepth - 2

        for i, metadatas in enumerate(treeview):
# Rule regarding the kind of object.
            isdir = 'dir' in metadatas['kind']

# Rule before any kind of rule.
            if thisdepth == 0:
                addvrule = False
# Ugly patch !!!
                before   = "  "

            elif i == imax:
                addvrule = False
                before   = " " + self.UTF8_DECOS['lnode']

            else:
                addvrule = True
                before   = " " + self.UTF8_DECOS['vnode']

# Just add the object.
            lines.append(
                "{0}{1} {2}{3}".format(
                    before,
                    self.UTF8_DECOS['hrule'],
                    self.UTF8_DECOS['deco'],
                    self.pathtoprint(metadatas)
                )
            )

# A new not empty directory
            if isdir and metadatas['content']:
                subbefore = " "*subtabdepth

                if addvrule:
                    subbefore += " " + self.UTF8_DECOS['vrule'] + "  "

                else:
                    subbefore += "    "

                lines += [
                    subbefore + x
                    for x in self._rtree(metadatas['content'])
                ]

        return lines


    @property
    def toc(self):
        """
prototype::
    type   = property
    return = str ;
             the content only shows files and their direct parent folder like in
             a table of content where the section are always relative paths of
             parent directories and subsection are path of files
        """
# The job has to be done.
        if self.havetobuild('toc'):
            text       = []
            lastparent = ""
            tab        = self.ASCII_DECOS["tab"]
            decodir    = self.ASCII_DECOS["dir"]
            decofile   = self.ASCII_DECOS["file"]
            mainname   = self.ppath.name

            for metadatas in self.listview:
# One file
                if "file" in metadatas["kind"]:
                    thisparent = str(
                        metadatas["ppath"].parent.relative_to(self.ppath)
                    )

                    if lastparent != thisparent:
                        dirpath \
                        = mainname / metadatas["ppath"].parent.relative_to(self.ppath)

                        text.append("")
                        text.append("{0} {1}".format(decodir, dirpath))

                        lastparent = thisparent

                    text.append(
                        "{0}{1} {2}".format(
                            tab,
                            decofile,
                            self.pathtoprint(metadatas)
                        )
                    )

# One empty directory
                elif metadatas["kind"] == "empty_dir":
                    dirpath = mainname / metadatas["ppath"].relative_to(
                        self.ppath
                    )

                    text.append("")
                    text.append("{0} {1}".format(decodir, dirpath))

# "Lines to text" transformation can be done
            self.outputs['toc'] = '\n'.join(text[1:])


# The job has been done.
        return self.outputs['toc']


    @property
    def latex(self):
        """
prototype::
    type   = property
    return = str ;
             a ¨latex code that can be used by the ¨latex package 
             ¨latex::``dirtree``
        """
# The job has to be done.
        if self.havetobuild('latex'):
            text = []

            for metadatas in self.listview:
                depth = metadatas["depth"] + 1
                pathtoprint = latex_escape(self.pathtoprint(metadatas))

                text.append(
                    "{0}.{1} <{2}>.".format(
                        "  "* depth,
                        depth,
                        pathtoprint
                    ).replace('<', '{').replace('>', '}')
                )

            self.outputs['latex'] = "\dirtree{%\n" + '\n'.join(text) + "\n}"

# The job has been done.
        return self.outputs['latex']
