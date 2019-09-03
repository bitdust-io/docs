# Makefile
#
# Copyright (C) 2008-2018 Veselin Penev  https://bitdust.io
#
# This file (Makefile) is part of BitDust Software.
#
# BitDust is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BitDust Software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with BitDust Software.  If not, see <http://www.gnu.org/licenses/>.
#
# Please contact us if you have any questions at bitdust.io@gmail.com


api:
	@echo "API"
	@python build_api.py ../bitdust.devel/interface/api.py api.md
    
settings:
	@echo "settings"
	@python build_settings.py ../bitdust.devel/ settings.md

sphinx:
	@echo "sphinx-build"
	@cp -R sphinx_conf/* _rst/
	@sphinx-build -b html _rst _rst/_build/html

sphinxrst:
	@echo "sphinx-apidoc"
	@rm -rf _rst/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/automats/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/contacts/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/chat/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/crypt/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/customer/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/dht/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/interface/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/lib/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/logs/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/main/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/p2p/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/parallelp/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/raid/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/services/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/storage/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/stun/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/supplier/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/system/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/transport/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/updates/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/userid/
	@sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/web/
	# @sphinx-apidoc -e -P -H BitDust -o _rst/ ../bitdust.devel/

build: api settings