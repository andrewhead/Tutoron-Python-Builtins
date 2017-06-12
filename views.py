#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context

from tutorons.core.scanner import NodeScanner
from tutorons.core.views import pagescan, snippetexplain
from detect import PythonBuiltInExtractor
from explain import explain as explain_builtin
from render import render
from builtins import explanations


logging.basicConfig(level=logging.INFO, format="%(message)s")


@csrf_exempt
@pagescan
def scan(html_doc):
    builtin_extractor = PythonBuiltInExtractor()
    builtin_scanner = NodeScanner(builtin_extractor, ['code', 'pre'])
    regions = builtin_scanner.scan(html_doc)
    rendered_regions = []
    for r in regions:
        hdr, exp, url = explain_builtin(r.string)
        document = render(r.string, hdr, exp, url)
        rendered_regions.append((r, document))
    return rendered_regions


@csrf_exempt
@snippetexplain
def explain(text, edge_size):

    error_template = get_template('error.html')

    if text in explanations:
        hdr, exp, url = explain_builtin(text)
        explanation = render(text, hdr, exp, url)
    else:
        logging.error("Error processing python built-in %s", text)
        explanation = error_template.render(Context({'text': text, 'type': 'python built-in'}))

    return explanation
