#!/usr/bin/python

# -*- coding: utf-8 -*-

# Copyright (C) 2009-2014:
#    Guillaume Subiron, maethor@subiron.org
#
# This file is part of Shinken.
#
# Shinken is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Shinken is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Shinken.  If not, see <http://www.gnu.org/licenses/>.

import time
import urllib

from collections import Counter

### Will be populated by the UI with it's own value
app = None


def get_global_stats():
    user = app.bottle.request.environ['USER']
    user.is_administrator() or app.redirect403()

    range_end = int(time.time())
    range_start = int(app.request.GET.get('range_start', range_end - 2592000))

    logs = list(app.logs_module.get_ui_logs(range_start=range_start, range_end=range_end, filters={'type': 'SERVICE NOTIFICATION', 'command_name': 'notify-service-by-hubot'}, limit=None))
    hosts = Counter()
    services = Counter()
    hostsservices = Counter()
    for l in logs:
        hosts[l['host_name']] += 1
        services[l['service_description']] += 1
        hostsservices[l['host_name'] + '/' + l['service_description']] += 1
    return {'hosts': hosts, 'services': services, 'hostsservices': hostsservices}

def get_service_stats(name):
    user = app.bottle.request.environ['USER']
    user.is_administrator() or app.redirect403()

    range_end = int(time.time())
    range_start = int(app.request.GET.get('range_start', range_end - 2592000))

    logs = list(app.logs_module.get_ui_logs(range_start=range_start, range_end=range_end, filters={'type': 'SERVICE NOTIFICATION', 'command_name': 'notify-service-by-hubot', 'service_description': name}, limit=None))
    hosts = Counter()
    for l in logs:
        hosts[l['host_name']] += 1
    return {'service': name, 'hosts': hosts}

def get_host_stats(name):
    user = app.bottle.request.environ['USER']
    user.is_administrator() or app.redirect403()

    range_end = int(time.time())
    range_start = int(app.request.GET.get('range_start', range_end - 2592000))

    logs = list(app.logs_module.get_ui_logs(range_start=range_start, range_end=range_end, filters={'type': 'SERVICE NOTIFICATION', 'command_name': 'notify-service-by-hubot', 'host_name': name}, limit=None))
    services = Counter()
    for l in logs:
        services[l['service_description']] += 1
    return {'host': name, 'services': services}


pages = {
    get_global_stats: {
        'name': 'GlobalStats', 'route': '/stats', 'view': 'stats'
    },

    get_service_stats: {
        'name': 'Stats', 'route': '/stats/service/<name:path>', 'view': 'stats_service'
    },

    get_host_stats: {
        'name': 'Stats', 'route': '/stats/host/<name:path>', 'view': 'stats_host'
    }
}
