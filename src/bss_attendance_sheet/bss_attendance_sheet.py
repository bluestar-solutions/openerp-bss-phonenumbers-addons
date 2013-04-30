# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Bluestar Solutions Sàrl (<http://www.blues2.ch>).
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
from openerp.osv import fields, osv
from bss_contract_week import DAY_FIELDS
import logging
from bss_utils.logging_template import *
from bss_utils.dateutils import orm_date
from pytz import timezone
import pytz

_logger = logging.getLogger(__name__)

class bss_attendance_sheet(osv.osv):
    _name = "bss_attendance_sheet.sheet"
    _description = "Attendance Sheet"
    
    def init(self, cr):
        cr.execute("""                  
            CREATE OR REPLACE FUNCTION public.empty_agg ( anyelement, anyelement )
            RETURNS anyelement LANGUAGE sql IMMUTABLE STRICT AS $$
                    SELECT 0.0::numeric;
            $$;
             
            DROP AGGREGATE IF EXISTS public.empty(anyelement);
            CREATE AGGREGATE public.empty (
                    sfunc    = public.empty_agg,
                    basetype = anyelement,
                    stype    = anyelement
            );
        """)    
    
    @staticmethod
    def _td2str(td):
        return ':'.join(str(td).split(':')[:2])
    
    def _total(self, cr, uid, ids, name, args, context=None):
        week_obj = self.pool.get('bss_attendance_sheet.contract_week')
        breaks_obj = self.pool.get('bss_attendance_sheet.breaks_settings')
        hol_obj = self.pool.get('hr.holidays')
             
        res = {}
        if not isinstance(ids, list):
            ids = [ids]
        for sheet in self.browse(cr, uid, ids, context=context):
            _logger.debug('Recalculate total for sheet : %s/%s' % (sheet.employee_id.name, sheet.name))
            
            server_tz = pytz.UTC
            employee_tz = timezone(sheet.employee_id.tz)
            
            res.setdefault(sheet.id, {
                'total_attendance': 0.0,
                'total_break': 0.0,
                'total_midday': 0.0,
                'total_recorded': 0.0,
                'expected_time': 0.0,
                'time_difference': 0.0
            })
            
            day_start = employee_tz.localize(datetime.strptime('%s 00:00:00' % sheet.name, '%Y-%m-%d %H:%M:%S'))
            day_end = day_start + timedelta(days=1)

            breaks = {'break_offered': 0.0,
                      'minimum_break': 0.0,
                      'midday_break_from': 0.0,
                      'minimum_midday': 0.0}
            breaks_ids = breaks_obj.search(cr, uid, 
                                           [('company_id', '=', sheet.employee_id.company_id.id),
                                            ('name', '<=', sheet.name)], 
                                           limit=1, order='name desc', context=context)
            if breaks_ids:
                breaks = breaks_obj.read(cr, uid, breaks_ids, 
                                         ['break_offered', 'minimum_break', 'midday_break_from', 'minimum_midday'], 
                                         context)[0]
                                         
            holidays_factor = hol_obj.get_holiday_factor(cr, uid, sheet.employee_id.id, sheet.name)
            
            res[sheet.id]['expected_time'] = 0.0
            for contract in sheet.employee_id.contract_ids:
                if contract.date_start <= sheet.name and (not contract.date_end or contract.date_end >= sheet.name):
                    week_ids = week_obj.search(cr, uid, [('contract_id', '=', contract.id), ('name', '<=', sheet.name)], limit=1, order='name desc', context=context)
                    if week_ids:
                        day_field = DAY_FIELDS[datetime.strptime(sheet.name, '%Y-%m-%d').date().isoweekday()]
                        res[sheet.id]['expected_time'] += week_obj.read(cr, uid, week_ids, [day_field], context=context)[0][day_field]
            res[sheet.id]['holidays_time'] = holidays_factor * res[sheet.id]['expected_time']
            
            if sheet.attendance_ids:  
                last_sign_in = day_start
                last_arrival = day_start
                last_pause_start = day_start
                last_attendance = (None, None)
                
                attendance_time = timedelta(0)
                day_time = timedelta(0)
                break_time = timedelta(0)
                midday_time = timedelta(0)
                for attendance in sorted(sheet.attendance_ids, key=lambda a: a.name):
                    _logger.debug('Process %s attendance : %s/%s' % (attendance.name, attendance.type, attendance.action))
                    if attendance.action == 'sign_in':
                        last_sign_in = server_tz.localize(datetime.strptime(attendance.name, '%Y-%m-%d %H:%M:%S'))
                        
                        if attendance.type == 'std':
                            last_arrival = server_tz.localize(datetime.strptime(attendance.name, '%Y-%m-%d %H:%M:%S'))
                        elif attendance.type == 'break':
                            break_diff = server_tz.localize(datetime.strptime(attendance.name, '%Y-%m-%d %H:%M:%S')) - last_pause_start
                            if break_diff < timedelta(hours=breaks['minimum_break']):
                                break_diff = timedelta(hours=breaks['minimum_break'])
                            break_time += break_diff
                        elif attendance.type == 'midday':
                            midday_time += server_tz.localize(datetime.strptime(attendance.name, '%Y-%m-%d %H:%M:%S')) - last_pause_start
                            
                    elif attendance.action ==  'sign_out':
                        attendance_time += server_tz.localize(datetime.strptime(attendance.name, '%Y-%m-%d %H:%M:%S')) - last_sign_in
                        
                        if attendance.type == 'std':
                            day_time += server_tz.localize(datetime.strptime(attendance.name, '%Y-%m-%d %H:%M:%S')) - last_arrival
                        else:
                            last_pause_start = server_tz.localize(datetime.strptime(attendance.name, '%Y-%m-%d %H:%M:%S'))
                    last_attendance = (attendance.type, attendance.action)
                    
                if last_attendance != ('std', 'sign_out'):
                    if last_attendance[1] == 'sign_in':
                        if sheet.name == datetime.today().date().isoformat():
                            attendance_time += server_tz.localize(datetime.today()) - last_sign_in
                            day_time += server_tz.localize(datetime.today()) - last_arrival
                        else:
                            attendance_time += day_end - last_sign_in
                            day_time += day_end - last_arrival
                    elif last_attendance[0] == 'break':
                        if sheet.name == datetime.today().date().isoformat():
                            break_diff = server_tz.localize(datetime.today()) - last_pause_start
                            if break_diff < timedelta(hours=breaks['minimum_break']):
                                break_diff = timedelta(hours=breaks['minimum_break'])
                            break_time += break_diff
                            day_time += server_tz.localize(datetime.today()) - last_arrival
                        else:
                            break_diff = day_end - last_pause_start
                            if break_diff < timedelta(hours=breaks['minimum_break']):
                                break_diff = timedelta(hours=breaks['minimum_break'])
                            break_time += break_diff
                            day_time += day_end - last_arrival
                    elif last_attendance[0] == 'midday':
                        if sheet.name == datetime.today().date().isoformat():
                            midday_time += server_tz.localize(datetime.today()) - last_pause_start
                            day_time += server_tz.localize(datetime.today()) - last_arrival
                        else:
                            midday_time += day_end - last_pause_start
                            day_time += day_end - last_arrival
                         
                if break_time >= timedelta(hours=breaks['break_offered']):
                    break_time -= timedelta(hours=breaks['break_offered'])
                else:
                    break_time = timedelta(0)
                            
                if midday_time < timedelta(hours=breaks['minimum_midday']) \
                        and attendance_time >= timedelta(hours=breaks['midday_break_from']):
                    midday_time = timedelta(hours=breaks['minimum_midday']) 
                
                res[sheet.id]['total_attendance'] = attendance_time.seconds / 3600.0
                res[sheet.id]['total_break'] = break_time.seconds / 3600.0
                res[sheet.id]['total_midday'] = midday_time.seconds / 3600.0
                recorded_time = day_time - midday_time - break_time
                res[sheet.id]['total_recorded'] = recorded_time.seconds / 3600.0
                
            res[sheet.id]['time_difference'] = res[sheet.id]['total_recorded'] + res[sheet.id]['holidays_time'] - res[sheet.id]['expected_time']
                
        return res
    
    def _cumulative_difference(self, cr, uid, ids, name, args, context=None):
        emp_obj = self.pool.get('hr.employee')
        res = {}
        
        employee_ids = set()
        for values in self.read(cr, uid, ids, ['employee_id'], context):
            employee_ids.add(values['employee_id'][0])
        
        for employee in emp_obj.browse(cr, uid, list(employee_ids), context):
            updated_sheet_ids = self.search(cr, uid, ['&', ('employee_id', '=', employee.id), ('id', 'in', ids)], 
                                            limit=1, order="name asc", context=context)
            if updated_sheet_ids:
                start_date = self.read(cr, uid, updated_sheet_ids[0], ['name'], context)['name']
                sheet_ids = self.search(cr, uid, [('employee_id', '=', employee.id),
                                                  ('name', '>=', start_date)], 
                                    order="name asc", context=context)
                prev_sheet_ids = self.search(cr, uid, [('employee_id', '=', employee.id),
                                                       ('name', '<', start_date)], 
                                             order="name desc", limit=1, context=context)
                
                cumul = 0.0
                if prev_sheet_ids:
                    cumul = self.read(cr, uid, prev_sheet_ids[0], ['cumulative_difference'], context)['cumulative_difference']
                else:
                    cumul = employee.attendance_start
                    
                for sheet in self.browse(cr, uid, sheet_ids, context):                    
                    cumul += sheet.time_difference
                    res[sheet.id] = cumul
        
        return res

    def _day_of_week(self, cr, uid, ids, name, args, context=None):
        res = {}
        
        for sheet in self.browse(cr, uid, ids, context):
            res[sheet.id] = orm_date(sheet.name).strftime('%a')
        
        return res

    def _month(self, cr, uid, ids, name, args, context=None):
        res = {}
        
        for sheet in self.browse(cr, uid, ids, context):
            res[sheet.id] = sheet.name[:7]
        
        return res
    
    def _get_attendance_sheet_ids(self, cr, uid, ids, context=None):
        sheet_obj = self.pool.get('bss_attendance_sheet.sheet')
        
        sheet_ids = set()
        for attendance in self.browse(cr, uid, ids, context):
            server_tz = pytz.UTC
            employee_tz = timezone(attendance.employee_id.tz)
            attendance_time = server_tz.localize(datetime.strptime(attendance.name, '%Y-%m-%d %H:%M:%S')).astimezone(employee_tz)
            sheet_ids = sheet_ids.union(set(sheet_obj.search(cr, uid, [('name', '=', attendance_time.strftime('%Y-%m-%d')), 
                                                                       ('employee_id', '=', attendance.employee_id.id)], 
                                                             order='name asc', context=context)))
        
        log_debug_trigger(_logger, 'bss_attendance_sheet.sheet', sheet_ids, 'hr.attendance')
        return list(sheet_ids)

    def _get_breaks_settings_sheet_ids(self, cr, uid, ids, context=None):
        employee_obj = self.pool.get('hr.employee')
        sheet_obj = self.pool.get('bss_attendance_sheet.sheet')
        sheet_ids = set()
        for break_offered in self.browse(cr, uid, ids, context):
            employee_ids = employee_obj.search(cr, uid, [('company_id', '=', break_offered.company_id.id)], context=context)
            for employee_id in employee_ids:
                sheet_ids = sheet_ids.union(set(sheet_obj.search(cr, uid, [('name', '>=', break_offered.name), 
                                                                           ('employee_id', '=', employee_id)], 
                                                                 order='name asc', context=context)))
                
        log_debug_trigger(_logger, 'bss_attendance_sheet.sheet', sheet_ids, 'bss_attendance_sheet.breaks_settings')
        return list(sheet_ids)

    def _get_contract_week_sheet_ids(self, cr, uid, ids, context=None):
        sheet_obj = self.pool.get('bss_attendance_sheet.sheet')
        sheet_ids = set()
        for contract_week in self.browse(cr, uid, ids, context):
            sheet_ids = sheet_ids.union(set(sheet_obj.search(cr, uid, [('name', '>=', contract_week.name), 
                                                                       ('employee_id', '=', contract_week.contract_id.employee_id.id)], 
                                                             order='name asc', context=context)))
            
        log_debug_trigger(_logger, 'bss_attendance_sheet.sheet', sheet_ids, 'bss_attendance_sheet.contract_week')
        return list(sheet_ids)

    def _get_holidays_sheet_ids(self, cr, uid, ids, context=None):
        sheet_obj = self.pool.get('bss_attendance_sheet.sheet')
        sheet_ids = set()
        for holidays in self.browse(cr, uid, ids, context):
            sheet_ids = sheet_ids.union(set(sheet_obj.search(cr, uid, [('name', '>=', holidays.date_from_day),
                                                                       ('name', '<=', holidays.date_to_day), 
                                                                       ('employee_id', '=', holidays.employee_id.id)], 
                                                             order='name asc', context=context)))
            
        log_debug_trigger(_logger, 'bss_attendance_sheet.sheet', sheet_ids, 'hr.holidays')
        return list(sheet_ids)

    def _get_employee_sheet_ids(self, cr, uid, ids, context=None):
        sheet_obj = self.pool.get('bss_attendance_sheet.sheet')
        sheet_ids = set()
        for employee in self.browse(cr, uid, ids, context):
            sheet_ids = sheet_ids.union(set(sheet_obj.search(cr, uid, [('employee_id', '=', employee.id)], 
                                                             order='name asc', context=context)))
            
        log_debug_trigger(_logger, 'bss_attendance_sheet.sheet', sheet_ids, 'hr.employee')
        return list(sheet_ids)
    
    _columns = {
        'name': fields.date('Date', readonly=True),
        'day_of_week': fields.function(_day_of_week, type="char", method=True, string='Day'),
        'month': fields.function(_month, type="char", method=True, string='Month', store={
            'bss_attendance_sheet.sheet': (lambda self, cr, uid, ids, context=None: ids, ['name'], 10),  
        }),
        'create_date': fields.datetime(),
        'write_date': fields.datetime(),
        'employee_id': fields.many2one('hr.employee', 'Employee', readonly=True),
        'attendance_ids': fields.one2many('hr.attendance', 'attendance_sheet_id', string="Attendances"),
        'total_attendance': fields.function(_total, type="float", method=True, string='Total Attendance', multi=True, store={
            'hr.attendance' : (_get_attendance_sheet_ids, ['name', 'employee_id', 'type', 'action', 'attendance_sheet_id'], 10),
            'bss_attendance_sheet.sheet': (lambda self, cr, uid, ids, context=None: ids, ['name', 'attendance_ids'], 10),  
        }),
        'total_break': fields.function(_total, type="float", method=True, string='Total Breaks', multi=True, store={
            'hr.attendance' : (_get_attendance_sheet_ids, ['name', 'employee_id', 'type', 'action', 'attendance_sheet_id'], 10),
            'bss_attendance_sheet.breaks_settings' : (_get_breaks_settings_sheet_ids, ['company_id', 'name', 'break_offered', 'minimum_break'], 10),
            'bss_attendance_sheet.sheet': (lambda self, cr, uid, ids, context=None: ids, ['name', 'attendance_ids'], 10),
        }),
        'total_midday': fields.function(_total, type="float", method=True, string='Midday Break', multi=True, store={
            'hr.attendance' : (_get_attendance_sheet_ids, ['name', 'employee_id', 'type', 'action', 'attendance_sheet_id'], 10),                                                        
            'bss_attendance_sheet.breaks_settings' : (_get_breaks_settings_sheet_ids, ['company_id', 'name', 'midday_break_from', 'minimum_midday'], 10),
            'bss_attendance_sheet.sheet': (lambda self, cr, uid, ids, context=None: ids, ['name', 'attendance_ids'], 10),
        }),
        'total_recorded': fields.function(_total, type="float", method=True, string='Total Recorded', multi=True, store={
            'hr.attendance' : (_get_attendance_sheet_ids, ['name', 'employee_id', 'type', 'action', 'attendance_sheet_id'], 10),
            'bss_attendance_sheet.breaks_settings' : (_get_breaks_settings_sheet_ids, ['company_id', 'name', 'break_offered', 'minimum_break', 
                                                                                       'midday_break_from', 'minimum_midday'], 10),
            'bss_attendance_sheet.sheet': (lambda self, cr, uid, ids, context=None: ids, ['name', 'attendance_ids'], 10),       
        }),
        'holidays_time': fields.function(_total, type="float", method=True, string='Holidays Time', multi=True, store={
            'bss_attendance_sheet.contract_week' : (_get_contract_week_sheet_ids, 
                                                    ['sunday_hours', 'monday_hours', 'tuesday_hours', 'wednesday_hours', 
                                                     'thursday_hours', 'friday_hours', 'saturday_hours'], 10),
            'hr.holidays' : (_get_holidays_sheet_ids, ['state'], 10),
            'hr.employee' : (_get_employee_sheet_ids, ['category_ids'], 10),
            'bss_attendance_sheet.sheet': (lambda self, cr, uid, ids, context=None: ids, ['name', 'attendance_ids'], 10),
        }),
        'expected_time': fields.function(_total, type="float", method=True, string='Expected Time', multi=True, store={
            'bss_attendance_sheet.contract_week' : (_get_contract_week_sheet_ids, 
                                                    ['sunday_hours', 'monday_hours', 'tuesday_hours', 'wednesday_hours', 
                                                     'thursday_hours', 'friday_hours', 'saturday_hours'], 10),
            'bss_attendance_sheet.sheet': (lambda self, cr, uid, ids, context=None: ids, ['name', 'attendance_ids'], 10),
        }),
        'time_difference': fields.function(_total, type="float", method=True, string='Difference', multi=True, store={
            'hr.attendance' : (_get_attendance_sheet_ids, ['name', 'employee_id', 'type', 'action', 'attendance_sheet_id'], 10),
            'bss_attendance_sheet.breaks_settings' : (_get_breaks_settings_sheet_ids, ['company_id', 'name', 'break_offered', 'minimum_break', 
                                                                                       'midday_break_from', 'minimum_midday'], 10),
            'bss_attendance_sheet.contract_week' : (_get_contract_week_sheet_ids, 
                                                    ['sunday_hours', 'monday_hours', 'tuesday_hours', 'wednesday_hours', 
                                                     'thursday_hours', 'friday_hours', 'saturday_hours'], 10),
            'hr.holidays' : (_get_holidays_sheet_ids, ['state'], 10),
            'hr.employee' : (_get_employee_sheet_ids, ['category_ids'], 10),
            'bss_attendance_sheet.sheet': (lambda self, cr, uid, ids, context=None: ids, ['name', 'attendance_ids'], 10),
        }),
        'cumulative_difference': fields.function(_cumulative_difference, type="float", group_operator="empty", method=True, string='Cumulative Difference', store={
            'hr.attendance' : (_get_attendance_sheet_ids, ['name', 'employee_id', 'type', 'action', 'attendance_sheet_id'], 20),
            'bss_attendance_sheet.breaks_settings' : (_get_breaks_settings_sheet_ids, ['company_id', 'name', 'break_offered', 'minimum_break', 
                                                                                       'midday_break_from', 'minimum_midday'], 20),
            'bss_attendance_sheet.contract_week' : (_get_contract_week_sheet_ids, 
                                                    ['sunday_hours', 'monday_hours', 'tuesday_hours', 'wednesday_hours', 
                                                     'thursday_hours', 'friday_hours', 'saturday_hours'], 20),
            'hr.holidays' : (_get_holidays_sheet_ids, ['state'], 20),
            'hr.employee' : (_get_employee_sheet_ids, ['category_ids', 'attendance_start'], 20),
            'bss_attendance_sheet.sheet': (lambda self, cr, uid, ids, context=None: ids, ['name', 'attendance_ids'], 20),
        }),
    }
    
    _order = 'employee_id asc, name asc'
    
    def _check_sheet(self, cr, uid, employee_id, day, context=None):  
        sheet_ids = self.search(cr, uid, [('employee_id', '=', employee_id), ('name', '=', day)], 
                                limit=1, context=context)
        if not sheet_ids:
            self.create(cr, 1, {'name': day, 'employee_id': employee_id}, context)
        else:
            self.write(cr, 1, sheet_ids, {'name': day}, context)
    
    def _check_all_sheet(self, cr, uid, day, context=None):
        emp_obj = self.pool.get('hr.employee')
        for employee_id in emp_obj.search(cr, uid, [], context=context):
            self._check_sheet(cr, uid, employee_id, day, context)

    def _check_today(self, cr, uid, context=None):
        emp_obj = self.pool.get('hr.employee')
        tss_obj = self.pool.get('hr_timesheet_sheet.sheet')
        for employee in emp_obj.browse(cr, uid, emp_obj.search(cr, uid, [], context=context), context):
            self._check_sheet(cr, uid, employee.id, datetime.today().isoformat()[:10], context)
            action = self.pool.get('hr.timesheet.current.open').open_timesheet(cr, employee.user_id.id, None, context)
            if not action.get('res_id', False):
                tss_obj.create(cr, employee.user_id.id, {}, context)
            
bss_attendance_sheet()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
