# -*- coding: utf-8 -*-
##############################################################################
#
#    Desarrollado para Corporativo Serca SC
#    Desarrollador: Ing. Salvador Daniel Pelayo Gómez.
#
##############################################################################
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    "name" : "Verificaciones",
    "version" : "0.1",
    "depends": ["base"],
    "author" : "Salvador Daniel Pelayo Gómez",
    "website": "http://www.corporativoserca.com",
    "category" : "Generic Modules/Others",
    "description" : """
Modulo para llevar el control del equipo que hay en el Corporativo.
""",
    "init_xml" : [],
    "update_xml" : ["verificaciones_menu.xml",
                    "security/event_security.xml",
                    "security/ir.model.access.csv",
                    "verificaciones_view.xml",
                    ],
    "demo_xml" : [],
    "installable" : True,
    'auto_install': False,
    'application': True,
}
