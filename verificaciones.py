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

    def getLogo(self, cr, uid, ids, context=None):
        img = self.pool.get('ir.header_img');
        ids = img.search(cr, uid, [('name', '=', 'banamex')], limit=1)
        logo = img.read(cr, uid, ids, ['img', 'type'], context=context)[0]
        image = '<img width="184" height="42" src="data:image/%s;base64,%s" />'%( logo['type'], str(logo['img']))
        return image;
    
    def getImage1(self, cr, uid, ids, context=None):
        img = self.read(cr, uid, ids, ['placa'], context=context)[0]
        image = '<img width="430" height="385" src="data:image/jpg;base64,%s" />'%(str(img['placa']))
        return image;
    
    def getImage2(self, cr, uid, ids, context=None):
        img = self.read(cr, uid, ids, ['num_ext'], context=context)[0]
        image = '<img width="410" height="385" src="data:image/jpg;base64,%s" />'%(str(img['num_ext']))
        return image;
    
    def getImage3(self, cr, uid, ids, context=None):
        img = self.read(cr, uid, ids, ['fachada'], context=context)[0]
        image = '<img width="430" height="385" src="data:image/jpg;base64,%s" />'%(str(img['fachada']))
        return image;
        
    def getImage4(self, cr, uid, ids, context=None):
        img = self.read(cr, uid, ids, ['investigador'], context=context)[0]
        image = '<img width="410" height="385" src="data:image/jpg;base64,%s" />'%(str(img['investigador']))
        return image;

    def day1(self, cr, uid, ids, context=None):
        fecha = self.read(cr, uid, ids, ['fecha_1a'], context=context)[0]
        return fecha['fecha_1a'].split('-')[2]

    def month1(self, cr, uid, ids, context=None):
        fecha = self.read(cr, uid, ids, ['fecha_1a'], context=context)[0]
        return fecha['fecha_1a'].split('-')[1]

    def year1(self, cr, uid, ids, context=None):
        fecha = self.read(cr, uid, ids, ['fecha_1a'], context=context)[0]
        return fecha['fecha_1a'].split('-')[0]

    def day2(self, cr, uid, ids, context=None):
        fecha = self.read(cr, uid, ids, ['fecha_2a'], context=context)[0]
        return fecha['fecha_2a'].split('-')[2]

    def month2(self, cr, uid, ids, context=None):
        fecha = self.read(cr, uid, ids, ['fecha_2a'], context=context)[0]
        return fecha['fecha_2a'].split('-')[1]

    def year2(self, cr, uid, ids, context=None):
        fecha = self.read(cr, uid, ids, ['fecha_2a'], context=context)[0]
        return fecha['fecha_2a'].split('-')[0]

    def write(self, cr, uid, ids, defaults=None, context=None):
        super(verificaciones, self).write(cr, uid, ids, defaults, context=context)
        ver = self.read(cr, uid, ids, ['aceptada', 'declinada'], context=context)
        if (ver[0]['aceptada'] and ver[0]['declinada']):
            raise osv.except_osv("Error", "La verificación debe de ser marcada como aceptada o declinada, solo una de las dos.")
        cont = 0
        v = self.read(cr, uid, ids, ['a', 'b', 'c', 'd', 'e', 'f'], context=context)[0]
        if v['a']: 
            cont+=1
        if v['b']: 
            cont+=1
        if v['c']:
            cont+=1
        if v['d']:
            cont+=1
        if v['e']:
            cont+=1
        if v['f']:
            cont+=1
        if cont > 1:
            raise osv.except_osv("Error!", "Solo se puede seleccionar una causa por la cual se declino la visita!")
        if cont == 1 and ver[0]['aceptada']:
            raise osv.except_osv("Error!", "La verificación se marco como aceptada y al mismo tiempo se marco una causa de declinación.")
        if cont == 0 and ver[0]['declinada']:
            raise osv.except_osv("Error!", "La verificación se marco como declinada y no se marco una causa de declinación.")
        return True

    """def copy(self, cr, uid, id, defaults=None, context=None):
        raise osv.except_osv("Error", "La duplicación de registros esta desactivada, en su lugar crea un registro nuevo.")
        return False
"""
    def _get_company(self, cr, uid, context=None):
        cmp_obj = self.pool.get('res.company')
        ids = cmp_obj.search(cr, uid, [], limit=1)
        id = ids and ids[0] or False
        return id

    def _get_user(self, cr, uid, context=None):
        return uid

    def unlink(self, cr, uid, ids, context=None):
        verificaciones = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for s in verificaciones:
            if s['state'] in ['borrador']:
                unlink_ids.append(s['id'])
            else:
                raise osv.except_osv(('Acción Invalida !'), ('Solo pueden ser eliminadas las verificaciones en borrador.'))
        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)

    def button_cancelar(self, cr, uid, ids, context=None):
        vals = {'state': 'cancelada'}
        return self.write(cr, uid, ids, vals)

    def button_entregar(self, cr, uid, ids, context=None):
        fecha = datetime.today()
        vals = {'state': 'entregada', 'fecha_entrega': fecha}
        return self.write(cr, uid, ids, vals)

    def button_entregar2(self, cr, uid, ids, context=None):
        verificaciones = self.read(cr, uid, ids, ['aceptada', 'declinada'], context=context)
        cont = 0
        v = self.read(cr, uid, ids, ['a', 'b', 'c', 'd', 'e', 'f'], context=context)[0]
        if v['a']: 
            cont+=1
        if v['b']: 
            cont+=1
        if v['c']:
            cont+=1
        if v['d']:
            cont+=1
        if v['e']:
            cont+=1
        if v['f']:
            cont+=1
        if cont > 1:
            raise osv.except_osv("Error!", "Solo se puede seleccionar más de una causa por la cual se declino la visita!")
        vals = {}
        if (verificaciones[0]['aceptada'] and verificaciones[0]['declinada']):
            raise osv.except_osv("Error", "La verificación debe de ser marcada como aceptada o declinada, solo una de las dos.")
        elif (verificaciones[0]['aceptada']):
            vals = {'state': 'aceptada'}
        elif (verificaciones[0]['declinada']):
            vals = {'state': 'declinada'}
        else: raise osv.except_osv("Error", "La verificación debe de ser marcada como aceptada o declinada, solo una de las dos.")
        return self.write(cr, uid, ids, vals)
        
    def button_regresar(self, cr, uid, ids, context=None):
        vals = {'state': 'asignada'}
        return self.write(cr, uid, ids, vals)

    def button_reasignar(self, cr, uid, ids, context=None):
        vals = {'state': 'borrador'}
        return self.write(cr, uid, ids, vals)

    def button_asignar(self, cr, uid, ids, context=None):
        fecha = datetime.today()
        vals = {'state': 'asignada', 'fecha_asignacion': fecha}
        return self.write(cr, uid, ids, vals)

    _name="verificaciones"
    _columns={
        'tipo_persona': fields.selection((
            ("fisica","FÍSICAS"),
            ("fisicas_ae","FÍSICAS CON ACTIVIDAD EMPRESARIAL"),
            ("moral", "MORAL")
        ), "Tipo de Persona", required=True, readonly=True, states={'borrador': [('readonly', False)]}, help="Tipo de persona para la que se solicita la verificación de domicilio."),#
        'primera': fields.boolean("1a", states={'entregada': [('readonly', True)]}),#
        'segunda': fields.boolean("2a", states={'entregada': [('readonly', True)]}),#
        'fecha_1a': fields.date("Fecha de Visita", help="Fecha en la que se realizó la primera visita.", states={'entregada': [('readonly', True)]}),#
        'fecha_2a': fields.date("Fecha de Visita", help="Fecha en la que se realizó la segunda visita.", states={'entregada': [('readonly', True)]}),#
        'no_cliente': fields.char("Número de Cliente", size=15, required=True, readonly=True, states={'borrador': [('readonly', False)]}),#
        'name': fields.char("Nombre del Cliente", size=100, required=True, readonly=True, states={'borrador': [('readonly', False)]}, help="Nombre del cliente investigado o Denominación/Razón Social."),#
        'no_sucursal': fields.char("Número de Sucursal", size=10, required=True, readonly=True, states={'borrador': [('readonly', False)]}),#
        'sucursal': fields.char("Nombre de Sucursal", size=100, required=True, readonly=True, states={'borrador': [('readonly', False)]}),#
        'domicilio': fields.text("Domicilio Principal", required=True, readonly=True, states={'borrador': [('readonly', False)]}, help="Calle y Número del Domicilio Principal."),#
        'telefono': fields.char("Número Telefónico", size=30, required=True, readonly=True, states={'borrador': [('readonly', False)]}),#
        'colonia': fields.char("Colonia", size=100, required=True, readonly=True, states={'borrador': [('readonly', False)]}),#
        'cp': fields.char("Código Postal", size=5, required=True, readonly=True, states={'borrador': [('readonly', False)]}),#
        'municipio': fields.char("Municipio", size=100, required=True, readonly=True, states={'borrador': [('readonly', False)]}),#
        'estado': fields.char("Estado", size=100, required=True, readonly=True, states={'borrador': [('readonly', False)]}, help="Nombre del Estado."),#
        #DATOS RECABADOS POR LA COMPAÑIA VERIFICADORA O LA SUCURSAL
        'visitador': fields.char("Visitador", size=500, states={'entregada': [('readonly', True)]}),
        'actividad': fields.char("Actividad o Giro", size=50, help="Confirmar actividad o giro.", states={'entregada': [('readonly', True)]}),#
        'anuncio': fields.boolean("Anuncio exterior", help="Marque la casilla si tiene anuncio exterior con nombre del negocio", states={'entregada': [('readonly', True)]}),#
        'zona': fields.selection((
            ("colonia", "Colonia"),
            ("comercial", "Comercial"),
            ("residencial","Residencial"),
            ("u_habitacion"," Unidad Habitación"),
            ("cond_horiz","Cond. Horiz."),
            ("fracc","Fraccionamiento")
        ), "Zona", states={'entregada': [('readonly', True)]}, help="Selecciona la zona en la que se encuentra el domicilio."),#
        'tipo_inmueble': fields.selection((
            ("casa","CASA"),
            ("departamento","DEPARTAMENTO"),
            ("edificio","EDIFICIO"),
            ("taller","TALLER/FABRICA"),
            ("local","LOCAL COMERCIAL"),
            ("completo","COMPLEJO IND"),
            ("oficina","OF. EN CASA HAB.")
        ), "Tipo de Inmueble", states={'entregada': [('readonly', True)]}, help="Seleccione el tipo de inmueble."),#
        'num_pisos': fields.integer("No. Pisos", help="Escriba el número de pisos que se ven desde la fachada.", states={'entregada': [('readonly', True)]}),#
        'num_ventanas': fields.integer("No. Ventanas", help="Escriba el número de ventanas exteriores que se ven desde la fachada.", states={'entregada': [('readonly', True)]}),#
        'color': fields.char("Color", size=50, help="Escriba el color de la fachada. Ej. BLANCO, CAFE/ROJO, VERDE, etc.", states={'entregada': [('readonly', True)]}),#
        'entrevistado': fields.char("Entrevistado", size=100, help="Nombre completo del representante legal o aprovado / entrevistado. Debe de ser mayor de 18 años.", states={'entregada': [('readonly', True)]}),#
        'parentesco': fields.char("Parentesco", size=50, help="Ponga el parentesco del entrevistado con el investigado.", states={'entregada': [('readonly', True)]}),#
        'aceptada': fields.boolean("Aceptada", states={'entregada': [('readonly', True)]}),#
        'declinada': fields.boolean("Declinada", states={'entregada': [('readonly', True)]}),#
        'comentarios': fields.text("Comentarios del Visitador", states={'entregada': [('readonly', True)]}),#
        ##CAUSAS DE DECLINACIÓN
        'a': fields.boolean("(A) No se localiza el domicilio o es inexistente.", states={'entregada': [('readonly', True)]}),
        'b': fields.boolean("(B) Domicilio vacío, en construcción, cambio o rentaba.", states={'entregada': [('readonly', True)]}),
        'c': fields.boolean("(C) En el domicilio no hay señales que corroboren que el cliente se dedique al giro manifestado", states={'entregada': [('readonly', True)]}, help="En el domicilio no hay señales que corroboren que el cliente se dedique al giro manifestado o que la empresa esté ubicada en el domicilio (aplica solo cuando no confirmen el giro y en caso de no entrevista)"),
        'd': fields.boolean("(D) Se encuentra el domicilio, no hay quién o no proporcionan informaciión relacionada con el cliente o no lo conocen.", states={'entregada': [('readonly', True)]}),
        'e': fields.boolean("(E) El cliente o su representante legal no se hubican en el domicilio.", help="Este caso se considera, solo aplicará para clientes sujetos a revisiones adicionales o de alto riesgo.", states={'entregada': [('readonly', True)]}),
        'f': fields.boolean("(F) Otro", states={'entregada': [('readonly', True)]}),
        'especificar': fields.text("Especificar", states={'entregada': [('readonly', True)]}),
        'latitud': fields.char("Latitud", size=20, states={'entregada': [('readonly', True)]}),
        'longitud': fields.char("Longitud", size=20, states={'entregada': [('readonly', True)]}),
        ##Pruebas fotograficas
        'placa': fields.binary("Placa de calle", states={'entregada': [('readonly', True)]}),
        'num_ext': fields.binary("Número exterior", states={'entregada': [('readonly', True)]}),
        'fachada': fields.binary("Fachada", states={'entregada': [('readonly', True)]}),
        'investigador': fields.binary("Investigador", states={'entregada': [('readonly', True)]}),
        ##DATOS DE CONTROL CORPORATIVO SERCA
        'fecha_solicitud': fields.date("Fecha de Solicitud", required=True, readonly=True, states={'borrador': [('readonly', False)]}),#
        'verificador': fields.many2one("res.users", "Verificador Asignado", readonly=True, states={'borrador': [('readonly', False)]}),#
        'user_id': fields.many2one("res.users", "Ejecutivo", required=True, readonly=True),#
        'fecha_asignacion': fields.datetime("Fecha y Hora de asignación", readonly=True),#
        'compania': fields.many2one("res.company", "Compañia verificadora", required=True, readonly=True, states={'borrador': [('readonly', False)]}),#
        'folio': fields.char("Folio", size=50, required=True, readonly=True, states={'borrador': [('readonly', False)]}),#
        'fecha_entrega': fields.datetime("Fecha de Entrega", readonly=True),#
        'state': fields.selection((
            ("borrador", "Borrador"),
            ("asignada", "Asignada"),
            ("aceptada", "Verificación Realizada"),
            ("declinada", "Verificación Declinada"),
            ("entregada", "Entregada"),
            ("cancelada", "Cancelada")
        ), "Estatus", required=True),#
        #Cobranza
        'cobertura': fields.selection((
            ("local", "LOCAL"),
            ("foraneo", "FORANEO"),
            ("dispercion", "DISPERCION")
        ), "Cobertura"),
        'costo': fields.float("Costo", digits=(5,2)),
        'viaticos': fields.float("Viaticos", digits=(5,2)),
        'penalizada': fields.boolean("Penalizada"),
        'penalizada_causas': fields.text("Causas de penalización"),
    }
    _defaults={
        'compania': _get_company,
        'folio': "NO APLICA",
        'state': "borrador",
        'user_id': _get_user,
    }
verificaciones()
