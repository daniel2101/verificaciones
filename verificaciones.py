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

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from osv import osv, fields


class verificaciones(osv.osv):

	def _get_default_pais_id(self, cr, uid, context=None):
        country_obj = self.pool.get('res.country')
        ids = country_obj.search(cr, uid, [ ( 'code', '=', 'MX' ), ], limit=1)
        id = ids and ids[0] or False
        return id

    _name="verificaciones"
    _columns={
		'tipo_persona': fields.selection((
			("fisica","FÍSICAS"),
			("fisicas_ae","FÍSICAS CON ACTIVIDAD EMPRESARIAL"),
			("moral", "MORAL")
		), "Tipo de Persona", required=True, help="Tipo de persona para la que se solicita la verificación de domicilio.").
		'primera': fields.boolean("1a"),
		'segunda': fields.boolean("2a"),
		'fecha_1a': fields.date("Fecha de Visita", help="Fecha en la que se realizó la primera visita."),
		'fecha_2a': fields.date("Fecha de Visita", help="Fecha en la que se realizó la segunda visita."),
        'no_cliente': fields.char("Número de Cliente", size=15, required=True),
        'name': fields.char("Nombre del Cliente", size=100, required=True, help="Nombre del cliente investigado o Denominación/Razón Social."),
		'no_sucursal': fields.char("Número de Sucursal", size=10, required=True),
        'sucursal': fields.char("Nombre de Sucursal", size=100),
        'domicilio': fields.text("Domicilio Principal", required=True, help="Calle y Número del Domicilio Principal."),
		'telefono': fields.char("Número Telefónico", size=30, required=True),
		'colonia': fields.char("Colonia", size=100, required=True)
		'cp': fields.char("Código Postal", size=5, required=True),
		'municipio': fields.char("Municipio", size=100, required=True),
		'pais_id': fields.many2one("res.country", "Pais"),
		'estado_id': fields.many2one("res.country.state", "Estado", domain="[('country_id','=',pais_id)]", required=True, help="Seleccione el Estado."),
		#DATOS RECABADOS POR LA COMPAÑIA VERIFICADORA O LA SUCURSAL
		'actividad': fields.char("Actividad o Giro", size=50, help="Confirmar actividad o giro."),
		'anuncio': fields.boolean("Anuncio exterior", help="Marque la casilla si tiene anuncio exterior con nombre del negocio"),
		'zona': fields.selection((
			("colonia", "Colonia"),
			("comercial", "Comercial"),
			("residencial","Residencial"),
			("u_habitacion"," Unidad Habitación"),
			("cond_horiz","Cond. Horiz."),
			("fracc","Fraccionamiento")
		), "Zona", help="Selecciona la zona en la que se encuentra el domicilio."),
		'tipo_inmueble': fields.selection((
			("casa","CASA"),
			("departamento","DEPARTAMENTO"),
			("edificio","EDIFICIO"),
			("taller","TALLER/FABRICA"),
			("local","LOCAL COMERCIAL"),
			("completo","COMPLEJO IND"),
			("oficina","OF. EN CASA HAB.")
		), "Tipo de Inmueble", help="Seleccione el tipo de inmueble."),
		'num_pisos': fields.integer("No. Pisos", help="Escriba el número de pisos que se ven desde la fachada."),
		'num_ventanas': fields.integer("No. Ventanas", help="Escriba el número de ventanas exteriores que se ven desde la fachada."),
		'color': fields.char("Color", size=50, help="Escriba el color de la fachada. Ej. BLANCO, CAFE/ROJO, VERDE, etc."),
		'entrevistado': fields.char("Entrevistado", size=100, help="Nombre completo del representante legal o aprovado / entrevistado. Debe de ser mayor de 18 años."),
		'parentesco': fields.char("Parentesco", size=50, help="Ponga el parentesco del entrevistado con el investigado."),
		'aceptada': fields.boolean("Aceptada"),
		'declinada': fields.boolean("Declinada"),
		##CAUSAS DE DECLINACIÓN
		'a': fields.boolean("(A) No se localiza el domicilio o es inexistente."),
		'b': fields.boolean("(B) Domicilio vacío, en construcción, cambio o rentaba."),
		'c': fields.boolean("(C) En el domicilio no hay señales que corroboren que el cliente se dedique al giro manifestado", help="En el domicilio no hay señales que corroboren que el cliente se dedique al giro manifestado o que la empresa esté ubicada en el domicilio (aplica solo cuando no confirmen el giro y en caso de no entrevista)"),
		'd': fields.boolean("(D) Se encuentra el domicilio, no hay quién o no proporcionan informaciión relacionada con el cliente o no lo conocen."),
		'e': fields.boolean("(E) El cliente o su representante legal no se hubican en el domicilio.", help="Este caso se considera, solo aplicará para clientes sujetos a revisiones adicionales o de alto riesgo."),
		'f': fields.boolean("(F) Otro"),
		'especificar': fields.text("Especificar"),
		'latitud': fields.char("Latitud", size=20),
		'longitud': fields.char("Longitud", size=20),
		##Pruebas fotograficas
		'placa': fields.binary("Placa de calle"),
		'num_ext': fields.binary("Número exterior"),
		'fachada': fields.binary("Fachada"),
		'investigador': fields.binary("Investigador"),
		##DATOS DE CONTROL CORPORATIVO SERCA
		'verificador': fields.many2one("res.users", "Verificador Asignado"),
		'fecha'
        'state': fields.selection((
            ("uso","Equipo en Uso"),
            ("descompuesto","Equipo Descompuesto"),
            ("fuera","Equipo ya no existente")
        ), "Estado", help="Selecciona el estado en el que se encuentra el equipo."),
    }
    _defaults={
        'pais_id': _get_default_pais_id,
    }
	
    _sql_constraints = [
        ('no_inventario_uniq', 'unique(no_inventario)', 'El número de inventario debe de ser unico!'),
    ]
inventario_equipo()
