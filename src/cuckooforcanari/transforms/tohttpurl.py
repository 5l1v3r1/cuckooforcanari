#!/usr/bin/env python

from canari.framework import configure
from canari.maltego.entities import Website
from common.entities import CuckooTaskID, NetworkAnalysis, CuckooMalwareFilename
from common.cuckooapi import report
from common.cuckooparse import network

__author__ = 'bostonlink'
__copyright__ = 'Copyright 2014, Cuckooforcanari Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '1.1'
__maintainer__ = 'bostonlink'
__email__ = 'bostonlink@pentest-labs.org'
__status__ = 'Development'

__all__ = [
    'dotransform'
]


@configure(
    label='To HTTP Request URL [Cuckoo Sandbox]',
    description='Returns URLs communicated with at the time of the Cuckoo file analysis.',
    uuids=[ 'cuckooforcanari.v2.IDToURL_Cuckoo',
            'cuckooforcanari.v2.FileToURL_Cuckoo',
            'cuckooforcanari.v2.SectionToURL_Cuckoo' ],
    inputs=[ ( 'Cuckoo Sandbox', CuckooTaskID ),
        ( 'Cuckoo Sandbox', CuckooMalwareFilename ),
        ( 'Cuckoo Sandbox', NetworkAnalysis) ],
    remote=False,
    debug=False
)
def dotransform(request, response, config):

    if 'taskid' in request.fields:
        task = request.fields['taskid']
    else:
        task = request.value

    netw = network(report(task))
    for d in netw['http']:
            response += Website(
                d['uri'].decode('ascii'),
                taskid=task)

    return response
