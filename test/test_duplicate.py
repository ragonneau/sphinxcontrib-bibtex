"""Test warnings on duplicate labels/keys."""

import docutils.utils
import common
import pytest


@pytest.mark.sphinx('html', testroot='duplicate_label')
def test_duplicate_label(app, warning):
    # see github issue 14
    app.builder.build_all()
    assert "duplicate label 1 for keys Test,Test2" in warning.getvalue()
    output = (app.outdir / "doc1.html").read_text()
    output2 = (app.outdir / "doc2.html").read_text()
    assert common.html_citations(
        id_="bibtex-citation-test", label="1").search(output)
    assert common.html_citations(
        id_="bibtex-citation-test2", label="1").search(output2)


@pytest.mark.sphinx('html', testroot='duplicate_citation')
def test_duplicate_citation(app, warning):
    app.builder.build_all()
    warning.seek(0)
    warnings = list(warning.readlines())
    assert len(warnings) == 1
    assert "duplicate citation for key Test" in warnings[0]
    # assure there's only one id for this citation
    output = (app.outdir / "index.html").read_text()
    assert output.count('id="bibtex-citation-test"') == 1


@pytest.mark.sphinx('html', testroot='duplicate_nearly_identical_keys')
def test_duplicate_nearly_identical_keys(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    # assure both citations and citation references are present
    assert common.html_citation_refs(label='Smi').search(output)
    assert common.html_citation_refs(label='Pop').search(output)
    assert common.html_citation_refs(label='Ein').search(output)
    assert common.html_citations(label='Smi').search(output)
    assert common.html_citations(label='Pop').search(output)
    assert common.html_citations(label='Ein').search(output)
    # assure distinct ids for citations
    assert len(common.html_citations(
        id_='bibtex-citation-test').findall(output)) == 1
    assert len(common.html_citations(
        id_='bibtex-citation-test1').findall(output)) == 1
    assert len(common.html_citations(
        id_='bibtex-citation-test2').findall(output)) == 1


# this test "accidentally" includes a user provided id which
# clashes with a bibtex generated citation id
# TODO is there a way for us to avoid such clash?
@pytest.mark.sphinx('html', testroot='duplicate_citation_id')
def test_duplicate_citation_id(app, warning):
    with pytest.raises(docutils.utils.SystemMessage) as exc_info:
        app.build()
    assert 'Duplicate ID: "bibtex-citation-test"' in str(exc_info.value)
