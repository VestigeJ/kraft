# SPDX-License-Identifier: BSD-3-Clause
#
# Authors: Alexander Jung <alexander.jung@neclab.eu>
#
# Copyright (c) 2020, NEC Europe Ltd., NEC Corporation. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
from __future__ import absolute_import
from __future__ import unicode_literals

import os

import six
from fcache.cache import FileCache

from kraft import __program__
from kraft.logger import logger


class Cache(object):
    _cache = {}
    _cachedir = []

    def __init__(self, environment):
        """Initializes the cache so that kraft does not have to constantly
        retrieve informational lists about unikraft, its available
        architectures, platforms, libraries and supported applications."""

        self._cachedir = os.path.join(environment.get('UK_WORKDIR'), 'kraft.cache')

        # Initiaize a cache instance
        self._cache = FileCache(
            app_cache_dir=self._cachedir,
            appname=__program__,
            flag='cs'
        )

    @property
    def cache(self):
        return self._cache

    def get(self, source=None):
        if isinstance(source, six.string_types) and source in self._cache:
            logger.debug("Retrieving %s from cache..." % source)
            return self._cache[source]

        return None

    def find_by_name(self, name=None):
        for source in self._cache:
            if self._cache[source].name == name:
                return self._cache[source]

        return None

    def all(self):
        return self._cache

    def set(self, source, repository):
        if isinstance(source, six.string_types):
            logger.debug("Saving %s into cache..." % repository)
            self._cache[source] = repository

    def sync(self):
        logger.debug("Synchronizing cache with filesystem...")
        pass

    def is_stale(self):
        """Determine if the list of remote repositories is stale.  Return a
        boolean value if at least one repository is marked as stale."""

        logger.debug("Checking cache for staleness...")

        if len(self.all()) == 0:
            return True

        return False
