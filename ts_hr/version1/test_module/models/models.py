# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
import io
import base64
import xlrd
from io import StringIO


class test_module(models.Model):
    _name = 'test_module.test_module'
    _description = 'test_module.test_module'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100

################################################################################################
# HR CONFIGURATION

# Employee
class employee(models.Model):
    _name = 'hr.employee'
    _inherit = 'hr.employee'

    main_salary = fields.Float(string='Main Salary')
    code = fields.Char()
    Social_insurance_no = fields.Char(string='Social Insurance no')
    hr_work_class_id = fields.Many2one('hr.work.class')
    account_id = fields.Many2one('account.account', string='Account')
# HR Work Class
class hr_work_class(models.Model):
    _name = 'hr.work.class'

    name = fields.Char('name')
    work_time_id = fields.Many2one('hr.work.time')
    rule_late_id = fields.Many2one('hr.rule')
    rule_early_exit_id = fields.Many2one('hr.rule')
    rule_overtime_id = fields.Many2one('hr.rule')
    no_checkin_id = fields.Many2one('hr.no.check')
    no_checkout_id = fields.Many2one('hr.no.check')

# HR Work Time
class hr_work_time(models.Model):
    _name = 'hr.work.time'

    name = fields.Char('name')
    sat_from = fields.Float('sat_from')
    sat_to = fields.Float('sat_to')
    sun_from = fields.Float('sun_from')
    sun_to = fields.Float('sun_to')
    mon_from = fields.Float('mon_from')
    mon_to = fields.Float('mon_to')
    tue_from = fields.Float('tue_from')
    tue_to = fields.Float('tue_to')
    wed_from = fields.Float('wed_from')
    wed_to = fields.Float('wed_to')
    thur_from = fields.Float('thur_from')
    thur_to = fields.Float('thur_to')
    fri_from = fields.Float('fri_from')
    fri_to = fields.Float('fri_to')

# HR Rule
class hr_rule(models.Model):
    _name = 'hr.rule'

    name = fields.Char('name')
    rule_type_id = fields.Selection([
            ('1','Late'),
            ('2','Early Exit'),
            ('3',' Overtime')
        ],)
    hr_rule_det_ids= fields.One2many('hr.rule.det','hr_rule_id',string="Details")

# HR Rule Details :
class hr_rule_det(models.Model):
    _name = 'hr.rule.det'

    hr_rule_id = fields.Many2one('hr.rule')
    rule_min_from = fields.Integer('From')
    rule_min_to = fields.Integer('To')
    calc_same_time = fields.Boolean('  ')
    result_min = fields.Integer('result min.')
    result_day = fields.Float('result day')

# HR No Check
class hr_no_check(models.Model):
    _name = 'hr.no.check'

    name = fields.Char('name')
    check_type_id = fields.Selection([
            ('1','Check-In'),
            ('2','Check-Out'),
        ],)
    result_day = fields.Float('day')
    result_hour = fields.Float('Hour')

# End CONFIGURATION
##################################################################################################


###################################################################################################
# Start Transaction

# HR HOLIDAY GEN
class hr_holiday_gen(models.Model):
    _name = 'hr.holiday.gen'

    name = fields.Char(string='name')
    from_date = fields.Date(string='from date')
    to_date = fields.Date('To date')


# HR MISSION
class hr_mission(models.Model):
    _name = 'hr.mission'

    name = fields.Char(string='name')
    employee_id = fields.Many2one('hr.employee',string='Employee')
    from_date = fields.Date('from date')
    to_date = fields.Date('to date')

# HR LATE PERMISSION
class hr_late_permission(models.Model):
    _name = 'hr.late.permission'

    name = fields.Char(string='name')
    employee_id = fields.Many2one('hr.employee',string='Employee')
    permission_date = fields.Date('permission date')
    permission_type = fields.Selection([
            ('1','Paid'),
            ('2','not Paid')
        ],)
    late_type = fields.Selection([
        ('1','Late'),
        ('2','Early Exit'),
        ('3','Mid of day')
    ])
    duration = fields.Float('Duration (h)')

# HR BONUS PUNISH
class hr_bonus_punish(models.Model):
    _name = 'hr.bonus.punish'

    name = fields.Char(string='name')
    date = fields.Date(string='Date')
    type = fields.Selection([
        ('1','Bonus'),
        ('2','Deduct')
    ])
    employee_id = fields.Many2one('hr.employee', string='Employee')
    description = fields.Text(string='Description')
    no_of_day = fields.Integer(string= 'Number Of Day')

# HR allowances
class hr_allowance(models.Model):
    _name = 'hr.allowance'

    name = fields.Char(string='name')
    description = fields.Text(string='Description')
    value = fields.Float(string='Value')

# HR allowance employee
class hr_allowance_employee(models.Model):
    _name = 'hr.allowance.employee'
    employee_id = fields.Many2one('hr.employee', string='Employee')
    allowance_id = fields.Many2one('hr.allowance',string='Allowance')

# HR Deduct
class hr_deduct(models.Model):
    _name = 'hr.deduct'

    name = fields.Char(string='name')
    description = fields.Text(string='Description')
    value = fields.Float(string='Value')

# HR deduct employee
class hr_deduct_employee(models.Model):
    _name = 'hr.deduct.employee'
    employee_id = fields.Many2one('hr.employee', string='Employee')
    deduct_id = fields.Many2one('hr.deduct',string='Deduct')

# HR EMPLOYEE SHEET ITEM
class hr_employee_sheet_item(models.Model):
    _name = 'hr.employee.sheet.item'
    sheet_id = fields.Many2one('hr.employee.sheet')
    Day = fields.Selection([
        ('6' , 'Sunday'),
        ('0' , 'Monday'),
        ('1' , 'Tuesday'),
        ('2' , 'Wednesday'),
        ('3' , 'Thursday'),
        ('4' , 'Friday'),
        ('5' , 'Saterday')
    ])
    Date = fields.Date('Date')
    Status = fields.Selection([
        ('0','Attend'),
        ('1','Absent'),
        ('2','Holiday'),
        ('3','No check In'),
        ('4','No check Out'),
        ('5','Generation Holiday'),
        ('6','Leave'),
        ('7','Mission')
    ])
    check_in = fields.Datetime(string="Check In")
    late_punishment_min = fields.Integer('Late Punishment (Min)')
    late_punishment_day = fields.Float('Late Punishment (Day)')
    check_out = fields.Datetime(string="Check Out")
    Exit_Early_punishment_min = fields.Integer('Exit Early Punishment (Min)')
    Exit_Early_punishment_day = fields.Float('Exit Early Punishment (Day)')
    over_time_min = fields.Integer('OverTime (Min)')
    over_time_day = fields.Float('OverTime (day)')

# HR EMPLOYEE SHEET
class hr_employee_sheet(models.Model):
    _name = 'hr.employee.sheet'

    employee = fields.Many2one('hr.employee',string='Employee')
    date_from = fields.Date('From')
    date_end = fields.Date('To')
    hr_employee_sheet_item_id = fields.One2many('hr.employee.sheet.item','sheet_id')
    basic_salary = fields.Float('Basic Salary')
    total_salary = fields.Float(string = "Salary Total")
    # total_bonus refer to days taken as bonus
    total_bonus = fields.Integer(string='Bonus Total (Day)')
    total_bonus_in_salary = fields.Float('Bonus')
    # total_punish refer to days taken as punish
    total_punish = fields.Integer(string='punish total (Day)')
    total_punish_in_salary = fields.Integer(string='punish')
    total_absent = fields.Integer('Absent Total (Day)')
    total_absent_in_salary = fields.Float('absent')
    total_allowances = fields.Float(string='Allowances Total')
    total_deduct = fields.Float(string='Deducts Total')
    total_late = fields.Float('Late (day)')
    total_late_in_salary = fields.Float('late')
    total_over = fields.Float('Over (Day)')
    total_over_in_salary = fields.Float('Over')
    state_calc = fields.Selection([('draft', 'Draft'), ('done', 'Done')], default='draft')
    def action_CalcTime(self):
        for rec in self:



            # calc Bonus
            bonus_items = self.env['hr.bonus.punish'].search([
                ('employee_id', '=', rec['employee'].id),
                ('type','=','1'),
            ])
            total = 0.0
            for line in bonus_items:
                if (
                        line['date'] >= ((rec.date_from))
                        and
                        (line['date']) <= ((rec.date_end))
                ):
                    total += line['no_of_day']
            rec.update({
                'total_bonus': total,
            })

            # calc Punish total
            punish_items = self.env['hr.bonus.punish'].search([
                ('employee_id', '=', rec['employee'].id),
                ('type', '=', '2'),
            ])
            total = 0.0
            for line in punish_items:
                if (
                        line['date'] >= ((rec.date_from))
                        and
                        (line['date']) <= ((rec.date_end))
                ):
                    total += line['no_of_day']
            rec.update({
                'total_punish': total,
            })

            # calc total allowances
            allowances_items = self.env['hr.allowance.employee'].search([
                ('employee_id', '=', rec['employee'].id),
            ])
            total = 0.0
            for line in allowances_items:
                total += line.allowance_id.value
            rec.update({
                'total_allowances': total,
            })

            # calc total deducts
            deducts_items = self.env['hr.deduct.employee'].search([
                ('employee_id', '=', rec['employee'].id),
            ])
            total = 0.0
            for line in deducts_items:
                total += line.deduct_id.value
            rec.update({
                'total_deduct': total,
            })







            # Calc   Sheet

            self.env['hr.employee.sheet.item'].search([('sheet_id', '=', rec.id)]).sudo().unlink()
            items = self.env['hr.attendance'].search([
                ('employee_id', '=', rec['employee'].id)
            ])
            date_from = fields.Date.from_string(rec.date_from)
            date_end = fields.Date.from_string(rec.date_end)
            delta = date_end - date_from
            res = []
            for n in range(delta.days + 1):
                res.append(fields.Date.to_string(date_from + datetime.timedelta(days=n)))
                new_item = self.env['hr.employee.sheet.item']
                new_item.create({
                    'sheet_id': rec.id,
                    'Day': str(fields.Datetime.from_string(
                        fields.Date.to_string(date_from + datetime.timedelta(days=n))
                    ).weekday()),

                    'Date': (fields.Date.to_string(date_from + datetime.timedelta(days=n)))

                })

            for record in rec.hr_employee_sheet_item_id:
                # set holiday generation
                holid_gen_items = self.env['hr.holiday.gen'].search([])
                is_holid_gen = False
                for line in holid_gen_items:
                    if(
                            record['Date'] >=(( line['from_date']))
                            and
                            ( record['Date'])<= ( line['to_date'])
                    ):
                        is_holid_gen = True
                        print ( 'holid gene:    True' )
                        break
                # set Leaves
                leaves_items = self.env['hr.leave'].search([
                    ('employee_id', '=', rec['employee'].id)
                ])
                is_leave =False
                for line in leaves_items:
                    if(
                            (
                                    (  ( record['Date']) >= ( line['date_from']) )
                            and
                                    ( ( record['Date'])<= ( line['date_to']) )
                            )


                    ):
                        is_leave = True
                        break
                # set Mission
                mission_items = self.env['hr.mission'].search([
                    ('employee_id', '=', rec['employee'].id)
                ])
                is_mission = False
                for line in mission_items:
                    if(
                            (
                                    ( record['Date']) >= ( line['from_date'])
                            and
                                    ( record['Date'])<= ( line['to_date'])
                            )
                    ):
                        is_mission = True
                        break

                if record['Day'] == '0':
                    if rec.employee.hr_work_class_id.work_time_id.mon_from == 0.0:
                        record.update({
                            'Status': '2',
                        })
                    else:
                        record.update({
                            'Status': '1',
                        })
                        if(is_leave):
                            record.update({
                                'Status': '6',
                            })
                        if (is_holid_gen):
                            record.update({
                                'Status': '5',
                            })
                        if ( is_mission ):
                            record.update({
                                'Status': '7',
                            })
                if record['Day'] == '1':
                    if rec.employee.hr_work_class_id.work_time_id.tue_from == 0.0:
                        record.update({
                            'Status': '2',
                        })
                    else:
                        record.update({
                            'Status': '1',
                        })
                        if (is_leave):
                            record.update({
                                'Status': '6',
                            })
                        if (is_holid_gen):
                            record.update({
                                'Status': '5',
                            })
                        if ( is_mission ):
                            record.update({
                                'Status': '7',
                            })
                if record['Day'] == '2':
                    if rec.employee.hr_work_class_id.work_time_id.wed_from == 0.0:
                        record.update({
                            'Status': '2',
                        })
                    else:
                        record.update({
                            'Status': '1',
                        })
                        if (is_leave):
                            record.update({
                                'Status': '6',
                            })
                        if (is_holid_gen):
                            record.update({
                                'Status': '5',
                            })
                        if ( is_mission ):
                            record.update({
                                'Status': '7',
                            })
                if record['Day'] == '3':
                    if rec.employee.hr_work_class_id.work_time_id.thur_from == 0.0:
                        record.update({
                            'Status': '2',
                        })
                    else:
                        record.update({
                            'Status': '1',
                        })
                        if (is_leave):
                            record.update({
                                'Status': '6',
                            })
                        if (is_holid_gen):
                            record.update({
                                'Status': '5',
                            })
                        if ( is_mission ):
                            record.update({
                                'Status': '7',
                            })
                if record['Day'] == '4':
                    if rec.employee.hr_work_class_id.work_time_id.fri_from == 0.0:
                        record.update({
                            'Status': '2',
                        })
                    else:
                        record.update({
                            'Status': '1',
                        })
                        if (is_leave):
                            record.update({
                                'Status': '6',
                            })
                        if (is_holid_gen):
                            record.update({
                                'Status': '5',
                            })
                        if ( is_mission ):
                            record.update({
                                'Status': '7',
                            })
                if record['Day'] == '5':
                    if rec.employee.hr_work_class_id.work_time_id.sat_from == 0.0:
                        record.update({
                            'Status': '2',
                        })
                    else:
                        record.update({
                            'Status': '1',
                        })
                        if (is_leave):
                            record.update({
                                'Status': '6',
                            })
                        if (is_holid_gen):
                            record.update({
                                'Status': '5',
                            })
                        if ( is_mission ):
                            record.update({
                                'Status': '7',
                            })
                if record['Day'] == '6':
                    if rec.employee.hr_work_class_id.work_time_id.sun_from == 0.0:
                        record.update({
                            'Status': '2',
                        })
                    else:
                        record.update({
                            'Status': '1',
                        })
                        if (is_leave):
                            record.update({
                                'Status': '6',
                            })
                        if (is_holid_gen):
                            record.update({
                                'Status': '5',
                            })
                        if ( is_mission ):
                            record.update({
                                'Status': '7',
                            })
            for item in items:
                ref_from = 0.0
                ref_to = 0.0
                if (
                                     (
                                             fields.Date.from_string( item['check_in']) >=rec.date_from
                                             and
                                             fields.Date.from_string(   item['check_in']) <= rec.date_end
                                     )
                        or
                                     (
                                             fields.Date.from_string( item['check_out']) >=rec.date_from and
                                             fields.Date.from_string( item['check_out']) <= rec.date_end
                                     )
                        or
                                     (
                                             fields.Date.from_string( item['check_in']) >=rec.date_from and
                                             fields.Date.from_string( item['check_out']) <= rec.date_end)

                                       ):
                    for record in rec.hr_employee_sheet_item_id:
                        if record['Day'] == '0':
                            ref_from = rec.employee.hr_work_class_id.work_time_id.mon_from
                            ref_to = rec.employee.hr_work_class_id.work_time_id.mon_to



                        if record['Day'] == '1':
                            ref_from = rec.employee.hr_work_class_id.work_time_id.tue_from
                            ref_to = rec.employee.hr_work_class_id.work_time_id.tue_to

                        if record['Day'] == '2':
                            ref_from = rec.employee.hr_work_class_id.work_time_id.wed_from
                            ref_to = rec.employee.hr_work_class_id.work_time_id.wed_to

                        if record['Day'] == '3':
                            ref_from = rec.employee.hr_work_class_id.work_time_id.thur_from
                            ref_to = rec.employee.hr_work_class_id.work_time_id.thur_to

                        if record['Day'] == '4':
                            ref_from = rec.employee.hr_work_class_id.work_time_id.fri_from
                            ref_to = rec.employee.hr_work_class_id.work_time_id.fri_to

                        if record['Day'] == '5':
                            ref_from = rec.employee.hr_work_class_id.work_time_id.sat_from
                            ref_to = rec.employee.hr_work_class_id.work_time_id.sat_to

                        if record['Day'] == '6':
                            ref_from = rec.employee.hr_work_class_id.work_time_id.sun_from
                            ref_to = rec.employee.hr_work_class_id.work_time_id.sun_to




                        if (
                                fields.Date.from_string(item['check_in']) == fields.Date.from_string(record['Date'])
                                or
                                fields.Date.from_string(item['check_out']) == fields.Date.from_string(record['Date'])

                           ):
                            late_min = 0.0
                            late_day = 0.0
                            if(item['check_in'] ):
                                late_permission_items = self.env['hr.late.permission'].search([
                                                                ('employee_id', '=', rec['employee'].id),
                                                                ('late_type','=','1'),
                                                                ('permission_date','=', record['Date'])
                                                            ])
                                for lateline in late_permission_items:
                                    ref_from+= lateline['duration']
                                    break
                                    print ('duration:'+str( lateline['duration']))
                                hour_min_check_in = float( fields.Datetime.from_string(item['check_in']).hour+2) +float(fields.Datetime.from_string(item['check_in']).minute)/60
                                late =  ( hour_min_check_in- ref_from ) * 60
                                print('ref from' + str(ref_from))
                                print('check in :'+ str( hour_min_check_in))
                                print ('late :' +  str(late))
                                late_rule_items = rec.employee.hr_work_class_id.rule_late_id.hr_rule_det_ids
                                for rule_item in late_rule_items:
                                    if ( late>= rule_item.rule_min_from and late<= rule_item.rule_min_to ):
                                        if(rule_item.result_min !=0 ):
                                            late_min = late * rule_item.result_min
                                        elif (rule_item.result_day !=0):
                                            late_day = rule_item.result_day
                            early_exit_min = 0.0
                            early_exit_day = 0.0
                            overtime_min = 0.0
                            overtime_day = 0.0
                            if(item['check_out']):
                                early_exit_permission_items = self.env['hr.late.permission'].search([
                                    ('employee_id', '=', rec['employee'].id),
                                    ('late_type', '=', '2'),
                                    ('permission_date', '=', record['Date'])
                                ])
                                for early_exitline in early_exit_permission_items :
                                    ref_to -= early_exitline['duration']
                                    break
                                    print ('duration:' + str(early_exitline['duration']))

                                hour_min_check_out = float(fields.Datetime.from_string(item['check_out']).hour+2) + float(
                                    fields.Datetime.from_string(item['check_out']).minute) / 60
                                early_exit = (hour_min_check_out - ref_to) * 60
                                print ('early exit :' + str(early_exit))
                                if (early_exit >0):
                                    print( 'hallow overtime')
                                    overtime_rule_items = rec.employee.hr_work_class_id.rule_overtime_id.hr_rule_det_ids
                                    for rule_item in overtime_rule_items:
                                        if (early_exit >= rule_item.rule_min_from and early_exit <= rule_item.rule_min_to):
                                            if (rule_item.result_min != 0):
                                                overtime_min = early_exit * rule_item.result_min
                                            elif (rule_item.result_day != 0):
                                                overtime_day = rule_item.result_day
                                if( early_exit <0 ):
                                    early_exit= early_exit* (-1)
                                    early_exit_rule_items = rec.employee.hr_work_class_id.rule_early_exit_id.hr_rule_det_ids
                                    for rule_item in early_exit_rule_items:
                                        if (early_exit >= rule_item.rule_min_from and early_exit <= rule_item.rule_min_to):
                                            if (rule_item.result_min != 0):
                                                early_exit_min = early_exit * rule_item.result_min
                                            elif (rule_item.result_day != 0):
                                                early_exit_day = rule_item.result_day






                            record.update({
                                'check_in': item['check_in'],
                                'check_out': item['check_out'],
                                'Status':'0',
                                'late_punishment_min':late_min,
                                'late_punishment_day':late_day,
                                'Exit_Early_punishment_min' : early_exit_min,
                                'Exit_Early_punishment_day' : early_exit_day,
                                'over_time_min':overtime_min,
                                'over_time_day':overtime_day,
                            })
                            if(not item['check_in']):
                                record.update({
                                    'Status': '3',
                                    'late_punishment_min': rec.employee.hr_work_class_id.no_checkin_id.result_hour,
                                    'late_punishment_day': rec.employee.hr_work_class_id.no_checkin_id.result_day,
                                })
                            if(not item['check_out']):
                                record.update({
                                    'Status': '4',
                                    'Exit_Early_punishment_min': rec.employee.hr_work_class_id.no_checkout_id.result_hour,
                                    'Exit_Early_punishment_day': rec.employee.hr_work_class_id.no_checkout_id.result_day,
                                })

            # calc salary
            total_late_punishment_min = sum( item.late_punishment_min for item in rec.hr_employee_sheet_item_id)
            total_late_punishment_day = sum( item.late_punishment_day for item in rec.hr_employee_sheet_item_id)
            total_Exit_Early_punishment_min = sum( item.Exit_Early_punishment_min for item in rec.hr_employee_sheet_item_id)
            total_Exit_Early_punishment_day = sum( item.Exit_Early_punishment_day for item in rec.hr_employee_sheet_item_id)
            total_over_time_min = sum( item.over_time_min for item in rec.hr_employee_sheet_item_id)
            total_over_time_day = sum(item.over_time_day for item in rec.hr_employee_sheet_item_id)
            total_late = ( ( total_late_punishment_min/60.0 ) / 24.0 ) +  float( total_late_punishment_day)
            total_exit_early = ( (total_Exit_Early_punishment_min / 60.0) / 24.0 ) + float(total_Exit_Early_punishment_day)
            no_of_day = len(rec.hr_employee_sheet_item_id)
            salary = rec.employee.main_salary
            salary_of_day = salary / no_of_day

            total_late_exit_day =( total_late + total_exit_early )

            total_overtime = ( ( ( total_over_time_min / 60.0 ) / 24.0 ) + float( total_over_time_day) )
            total_bonus = rec.total_bonus
            total_punish = rec.total_punish
            total_allowances = rec.total_allowances
            total_deduct = rec.total_deduct
            no_of_absent = 0
            for item in rec.hr_employee_sheet_item_id:
                if item.Status == '1':
                    no_of_absent +=1
            total_absent = no_of_absent
            total_blus =( salary +  total_overtime * salary_of_day + total_bonus * salary_of_day + rec.total_allowances  )
            total_minus =(no_of_absent * salary_of_day + total_late_exit_day * salary_of_day +  total_punish * salary_of_day + rec.total_deduct )
            total_salary = total_blus - total_minus
            rec.update({
                'total_absent': no_of_absent,
                'total_absent_in_salary': no_of_absent * salary_of_day,
                'total_punish': total_punish,
                'total_punish_in_salary':total_punish * salary_of_day ,
                'total_bonus': total_bonus ,
                'total_bonus_in_salary': total_bonus * salary_of_day ,
                'total_late': total_late_exit_day ,
                'total_late_in_salary': total_late_exit_day * salary_of_day ,
                'total_over': total_overtime ,
                'total_over_in_salary': total_overtime * salary_of_day ,
                'basic_salary':salary ,
                'total_salary': total_salary ,
            })



            print( total_late_punishment_min )
            print( total_late_punishment_day )
            print( total_Exit_Early_punishment_min )
            print( total_Exit_Early_punishment_day )
            print( total_over_time_min )
            print( total_over_time_day )
            print('absent:'+ str(total_absent))













            # for item in items:
            #     if(
            #             ( item['check_in'] >=rec.date_from and item['check_in'] <= rec.date_end ) or
            #             ( item['check_out'] >=rec.date_from and item['check_out'] <= rec.date_end ) or
            #             ( item['check_in'] >=rec.date_from and item['check_out'] <= rec.date_end)
            #               ):
            #         new_item = self.env['hr.employee.sheet.item']
            #         new_item.create({
            #                         'sheet_id': rec.id,
            #                         'check_in': item['check_in'],
            #                         'check_out': item['check_out'],
            #                         'Day' : str( fields.Datetime.from_string(item['check_in']).weekday() ) ,
            #
            #                         'Date':( item['check_in'] or item['check_out'] )
            #
            #                          })

            # list_param = (str(rec.date_from).split('-'))
            # year = list_param[0]
            # month = list_param[1]
            # print (year)
            # print (month)
            # date_from = fields.Date.from_string(rec.date_from)
            # date_end = fields.Date.from_string(rec.date_end)
            # delta = date_end - date_from
            # print ('delta: ' + str( delta.days))
            # res = []
            # for n in range(delta.days + 1):
            #     res.append(fields.Date.to_string(date_from + datetime.timedelta(days=n)))
            # print (res)



            #d1 = fields.Datetime.from_string(rec.date_end)
            #d0 = fields.Datetime.from_string(rec.date_from)
            #month = Calendar().itermonthdates(2014, 1)
            #month = calendar.Calendar().itermonthdates( rec.date_from.strftime('%Y',rec.date_from.strptime(datetime, "%Y")),  )
            #date=  datetime.strptime(rec.date_from,"%Y-%m-%d")
            #print (date.year )

            #datetime.date.today().strftime("%d")
            #datetime.date.today().strftime("%Y")

# HR EMPLOYEE Time sheet Confirm
class hr_employee_timesheet_confirm(models.Model):
    _name = 'hr.employee.timesheet.confirm'

    date_from = fields.Date('From')
    date_end = fields.Date('To')
    hr_employee_sheet_ids = fields.One2many('hr.employee.timesheet.confirm.item','hr_employee_sheet_confirm')
    def upload_sheets(self):
        for rec in self:
            employee_sheets = self.env['hr.employee.sheet'].search([
                ('date_from','=',rec.date_from),
                ('date_end','=', rec.date_end),
            ])
            for item in employee_sheets:
                employee_sheets_confirm_item = self.env['hr.employee.timesheet.confirm.item']
                employee_sheets_confirm_item.create({
                    'hr_employee_sheet_confirm':rec.id ,
                    'hr_employee_sheet': item.id,
                })
    def delete_sheets(self):
        for rec in self:
            self.env['hr.employee.timesheet.confirm.item'].search([('hr_employee_sheet_confirm', '=', rec.id)]).sudo().unlink()

    def confirm_sheets(self):
        for rec in self:
            for item in rec.hr_employee_sheet_ids:
                item.hr_employee_sheet.update({
                    'state_calc':'done',
                })

# HR EMPLOYEE IME SHEET CONFIRM ITEM
class hr_employee_timesheet_confirm_item(models.Model):
    _name = 'hr.employee.timesheet.confirm.item'
    hr_employee_sheet_confirm = fields.Many2one('hr.employee.timesheet.confirm')
    hr_employee_sheet = fields.Many2one('hr.employee.sheet',string= 'sheet')
    name = fields.Char(related='hr_employee_sheet.employee.name')
    basic_salary = fields.Float(related='hr_employee_sheet.basic_salary')
    total_over_in_salary = fields.Float(related='hr_employee_sheet.total_over_in_salary')
    total_bonus_in_salary = fields.Float(related='hr_employee_sheet.total_bonus_in_salary')
    total_allowances = fields.Float(related='hr_employee_sheet.total_allowances')
    total_punish_in_salary = fields.Integer(related='hr_employee_sheet.total_punish_in_salary')
    total_deduct = fields.Float(related='hr_employee_sheet.total_deduct')
    total_late_in_salary = fields.Float(related= 'hr_employee_sheet.total_late_in_salary')
    total_salary = fields.Float(related= 'hr_employee_sheet.total_salary')
    check = fields.Boolean(string='Check')

# HR Upload Fie Attendance
class hr_upload_file_attendence(models.Model):
    _name = 'hr.upload.file.attendence'
    name = fields.Char(string='name')
    file= fields.Binary(string='file')
    file_name = fields.Char("File Name")
    def confirm_attendance(self):
        try:
            # import os
            # os.environ['TZ'] = 'UTC'  # Set the timezone
            # import time
            # if hasattr(time, 'tzset'):
            #     time.tzset()
            inputx = io.BytesIO()
            inputx.write(base64.decodebytes(self.file))
            book = xlrd.open_workbook(file_contents=inputx.getvalue())
            sheet = book.sheet_by_index(0)
            cell = sheet.cell(9, 3)
            cell2 = sheet.cell(1, 18)
            cel2_str = str(cell2)
            date_from = cel2_str[18:28]



            day_from = int(date_from[0:2])
            print('date from:'+str(date_from))
            print('day from:'+ str(day_from))
            month = int(date_from[3:5])
            year = int(date_from[6:10])
            print('month:'+str( month))
            print('year:'+ str( year))

            date_to = cel2_str[39:49]

            day_to = int(date_to[0:2])
            print('date to'+ str(date_to))
            print('day to:'+str( day_to))

            count = 0
            lst_employee = []
            for count in range(9, (sheet.nrows), 10):
                item = {}
                code = str(sheet.cell(count + 1, 0))
                print('code:'+code)
                item['code'] = code[15:len(code) - 1]
                print('code in det. :'+item['code'])
                i = 0
                lst_time = []
                for day in range(day_from, day_to + 1, 1):
                    line = {}
                    if (3 + i == 7):
                        i = i + 1
                    if (3 + i == 18):
                        i = i + 1
                    line['check_in'] = (sheet.cell(count, 3 + i))
                    line['check_out'] = (sheet.cell(count + 1, 3 + i))
                    line['day'] = day
                    i = i + 1
                    lst_time.append(line)
                item['sheet'] = lst_time
                lst_employee.append(item)
            print(lst_employee)
            for record in lst_employee:
                employee =self.env['hr.employee'].search([
                        ('code','=',record['code'])
                    ])
                if(len(employee)==0):
                    continue
                for item in record['sheet']:
                    check_in =str( item['check_in'])
                    check_in_h = int(check_in[(0+6):(2+6)])
                    check_in_min = int(check_in[(3+6):(5+6)])
                    check_out =str( item['check_out'])
                    check_out_h = int(check_out[(0+6):(2+6)])
                    check_out_min = int(check_out[(3+6):(5+6)])
                    #datetime.datetime(1970, 1, 1)
                    date_check_in = fields.Datetime(string="Date current action",
                                                    default=lambda *a: datetime(year, month, item['day'], check_in_h,
                                                                                check_in_min))
                    date_check_out = fields.Datetime(string="Date current action",
                                                     default=lambda *a: datetime(year, month, item['day'], check_out_h,
                                                                                 check_out_min))
                    user_tz = self.env.user.tz or 'UTC'
                    hr_attendance = self.env['hr.attendance']
                    if( (check_in_h!=0 or check_in_min!=0) and (check_out_h!=0 or check_out_min!=0)   ):
                        hr_attendance.create({
                            'employee_id':employee[0].id,
                            'check_in': datetime.datetime (year, month,item['day'],check_in_h,check_in_min,0 ).strftime("%Y-%m-%d %H:%M:%S") ,
                            'check_out':datetime.datetime(year, month,item['day'],check_out_h,check_out_min,0 ).strftime("%Y-%m-%d %H:%M:%S"),
                        })
                    elif(check_in_h!=0 or check_in_min!=0):
                        hr_attendance.create({
                            'employee_id': employee[0].id,
                            'check_in': datetime.datetime(year, month, item['day'], check_in_h, check_in_min, 0).strftime(
                                "%Y-%m-%d %H:%M:%S"),
                        })
                    elif(check_out_h!=0 or check_out_min!=0):
                        hr_attendance.create({
                            'employee_id': employee[0].id,
                            'check_out': datetime.datetime(year, month, item['day'], check_out_h, check_out_min,
                                                           0).strftime("%Y-%m-%d %H:%M:%S"),
                        })










        finally:
            print('')

# assighn  workclass of many of employee
class hr_workclass_employee(models.Model):
    _name = 'hr.workclass.employee'

    name = fields.Char()
    hr_work_class_id = fields.Many2one('hr.work.class',string='work class')
    employee_ids = fields.One2many('hr.workclass.employee.item','workclass_id')
    main_salary = fields.Float(string='main salary')
    account_id = fields.Many2one('account.account',string='Account')
    leaves_ids = fields.One2many('hr.holidays.status.value','workclass_employee')
    def action_assign(self):
        for rec in self:
            # assign work class
            for item in rec.employee_ids:
                if item.check:
                    item.employee_id.update({
                        'hr_work_class_id': rec['hr_work_class_id'],
                    })
            # assign salary
            for item in rec.employee_ids:
                if item.check:
                    item.employee_id.update({
                        'main_salary': rec['main_salary'],
                    })
            # assign account
            for item in rec.employee_ids:
                if item.check:
                    item.employee_id.update({
                        'account_id':rec['account_id'],
                    })
            # assign leaves
            # for item in rec.leaves_ids:
            #     for emp in rec.employee_ids:
            #         if emp.check:
            #             records= (self.env['hr.holidays'].search(
            #                 [
            #                     ('employee_id', '=', emp.employee_id.id),
            #                     ('holiday_status_id', '=', item.leave.id),
            #                 ]
            #             ))
            #             count = len(records)
            #             if(count>0):
            #                 for record in records:
            #                     record.update({
            #                         'number_of_days_temp': item.value,
            #                         'holiday_type': 'employee',
            #                         'state': 'validate',
            #                         'type': 'add',
            #                     })
            #             elif count==0:
            #                 leave_allocate = self.env['hr.holidays']
            #                 leave_allocate.create({
            #                     'holiday_status_id': item.leave.id,
            #                     'employee_id': emp.employee_id.id,
            #                     'number_of_days_temp': item.value,
            #                     'holiday_type': 'employee',
            #                     'state': 'validate',
            #                     'type': 'add',
            #                 })
    def action_upload_employee(self):
        for rec in self:
            employees_records = self.env['hr.employee'].search([])
            lst_employee =[]
            lst_employee.append( record.employee_id for record in rec.employee_ids)
            for item in employees_records:
                if item not in lst_employee:
                     new_item = self.env['hr.workclass.employee.item']
                     new_item.create({
                       'workclass_id': rec.id,
                       'employee_id': item.id
                     })

class hr_workclass_employee_item(models.Model):
    _name = 'hr.workclass.employee.item'
    workclass_id = fields.Many2one('hr.workclass.employee')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    check = fields.Boolean(string='Checked')

class hr_holidays_status_value(models.Model):
    _name = 'hr.holidays.status.value'
    workclass_employee = fields.Many2one('hr.workclass.employee')
    leave = fields.Many2one('hr.leave.type',string='leave')
    value = fields.Float(string='Value')

class hr_holiday_assign(models.Model):
    _name = 'hr.holiday.class.employee'

    year = fields.Integer( string='Year')
    employee_class_id = fields.Many2one('hr.workclass.employee',string='Employee Class')
    def action_assign(self):
        for rec in self:
            # assign leaves
            for item in rec.employee_class_id.leaves_ids:
                for emp in rec.employee_class_id.employee_ids:
                    if emp.check:
                        leave_allocate = self.env['hr.leave.allocation']
                        leave_allocate.create({
                            'holiday_status_id': item.leave.id,
                            'employee_id': emp.employee_id.id,
                            'number_of_days_display': item.value,
                            'holiday_type': 'employee',
                            'state': 'validate',
                        })



