#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from collections import OrderedDict
from pytest import fixture

from mistool.os_use import PPath
from orpyste.data import ReadBlock as READ


# ------------------- #
# -- MODULE TESTED -- #
# ------------------- #

from mistool import term_use


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR = PPath(__file__).parent

DIRVIEW_CLASS = term_use.DirView


# --------------------------------------- #
# -- THE_DATAS_FOR_TESTING FOR TESTING -- #
# --------------------------------------- #

VIRTUAL_DIR = THIS_DIR

while VIRTUAL_DIR.name != "test":
    VIRTUAL_DIR = VIRTUAL_DIR.parent

VIRTUAL_DIR /= "virtual_dir"

THE_DATAS_FOR_TESTING = OrderedDict()

for ppath in THIS_DIR.walk(regpath = "file::**.txt"):
    THE_DATAS_FOR_TESTING[
        "{0} [{1}]".format(ppath.stem, ppath.parent.stem)
    ] = READ(
        content = ppath,
        mode    = {
            "keyval:: =": "gene",
            "verbatim"  : ["ascii", "latex", "toc", "tree"]
        }
    )

@fixture(scope="module")
def or_datas(request):
    for name, allinfos in THE_DATAS_FOR_TESTING.items():
        allinfos.build()

    def remove():
        for name, allinfos in THE_DATAS_FOR_TESTING.items():
            allinfos.remove()

    request.addfinalizer(remove)


# ------------------- #
# -- CASE VARIANTS -- #
# ------------------- #

def test_dirview(or_datas):
    for name, allinfos in THE_DATAS_FOR_TESTING.items():
        infos = allinfos.flatdict(nosep = True)

        gene    = infos['gene']
        dirname = gene['dirname']
        regpath = gene.get('regpath', "**")
        display = gene.get('display', "main short")
        sorting = gene.get('sorting', "alpha")

        dirview = DIRVIEW_CLASS(
            ppath   = VIRTUAL_DIR / dirname,
            regpath = regpath,
            display = display,
            sorting = sorting
        )

        print("PB ? name =", name)

        if "ascii" in infos:
            ascii_ = "\n".join(infos["ascii"])

            assert dirview.ascii == ascii_

        if "toc" in infos:
            toc = "\n".join(infos["toc"])

            assert dirview.toc == toc
