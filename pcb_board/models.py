
from django.db import models
from accounts.models import  Profile
# Create your models here.
def hex_to_rgba(hex_color, alpha=1):
    hex_color = hex_color.lstrip('#')

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return f"rgba({r}, {g}, {b}, {alpha})"


class Board (models.Model):
    STATE_CHOICES = [
        ('pending', 'در دست بررسی'),
        ('preparing', 'در پروسه تولید'),
        ('shipping', 'در حال ارسال'),
        ('completed', 'پایان یافته'),
    ]

    BASE_MATERIAL_CHOICES = (
        ('fr4', 'FR-4'),
        ('flex', 'Flex'),
        ('aluminum', 'Aluminum'),
        ('copper', 'Copper Core'),
        ('rogers', 'Rogers'),
        ('ptfe', 'PTFE Teflon'),
    )
    UNIT_CHOICES = (
        ('mm', 'میلی متر'),
        ('inch', 'اینچ'),
    )
    PRODUCT_TYPE_CHOICES = (
        ('industrial', 'صنعتی / مصرفی'),
        ('aerospace', 'هوا فضا'),
        ('medical', 'پزشکی'),
    )
    SUBSTRATE_TYPE_CHOICES = (
        ('25µm', 'ضخامت دی‌الکتریک  ۲۵µm'),
        ('50µm', 'ضخامت دی‌الکتریک ۵۰µm'),
        ('transparent', ' شفاف'),
    )
    THICKNESS_CHOICES = (
        ('0.4', '0.4mm'),
        ('0.6', '0.6mm'),
        ('0.8', '0.8mm'),
        ('1.0', '1.0mm'),
        ('1.2', '1.2mm'),
        ('1.6', '1.6mm'),
        ('2.0', '2.0mm'),
    )
    COLOR_CHOICES = (
        ('green', 'سبز'),
        ('purple', 'بنفش'),
        ('red', 'قرمز'),
        ('yellow', 'زرد'),
        ('blue', 'آبی'),
        ('white', 'سفید'),
        ('black', 'سیاه'),
    )
    QTY_CHOICES = (
        ('5', '5'),
        ('10', '10'),
        ('15', '15'),
        ('20', '20'),
        ('25', '25'),
        ('30', '30'),
        ('50', '50'),
        ('75', '75'),
        ('100', '100'),
        ('125', '125'),
        ('150', '150'),
        ('200', '200'),
        ('250', '250'),
        ('300', '300'),
        ('350', '350'),
        ('400', '400'),
        ('450', '450'),
        ('500', '500'),
        ('600', '600'),
        ('700', '700'),
        ('750', '750'),
        ('800', '800'),
        ('900', '900'),
        ('1000', '1000'),
        ('1200', '1200'),
        ('1250', '1250'),
        ('1400', '1400'),
        ('1500', '1500'),
        ('1600', '1600'),
        ('1750', '1750'),
        ('1800', '1800'),
        ('2000', '2000'),
        ('2400', '2400'),
        ('2500', '2500'),
        ('2800', '2800'),
        ('3000', '3000'),
        ('3500', '3500'),
        ('4000', '4000'),
        ('4500', '4500'),
        ('5000', '5000'),
        ('5500', '5500'),
        ('6000', '6000'),
        ('6500', '6500'),
        ('7000', '7000'),
        ('7500', '7500'),
        ('8000', '8000'),
        ('8500', '8500'),
        ('9000', '9000'),
        ('9500', '9500'),
        ('10000', '10000'),
        ('11000', '11000'),
        ('12000', '12000'),
        ('13000', '13000'),
        ('14000', '14000'),
        ('15000', '15000'),
        ('16000', '16000'),
        ('17000', '17000'),
        ('18000', '18000'),
        ('19000', '19000'),
        ('25000', '25000'),
        ('30000', '30000'),
        ('40000', '40000'),
        ('50000', '50000'),
        ('60000', '60000'),
        ('70000', '70000'),
    )
        # MATERIAL_CHOICES = (
        #     ('FR4_TG135', 'FR4 TG135'),
        #     ('Nan_Ya_NP_140F', 'Nan Ya NP-140F'),
        #     ('KB6164_TG135', 'KB6164 - TG135'),
        #     ('S1000H_TG155', 'S1000H TG155'),
        #     ('S1141_TG140', 'S1141 TG140'),

        #     ('Electro_deposited', 'Electro-deposited'),
        #     ('Rolled_Annealed', 'Rolled Annealed'),

        #     ('RO4350B', 'RO4350B(Dk=3.48, Df=0.0037)'),

        #     ('ZYF300CA-P', 'ZYF300CA-P(Dk=3.0, Df=0.0018)'),
        #     ('ZYF300CA-C', 'ZYF300CA-C(Dk=2.94, Df=0.0016)'),
        #     ('ZYF265D', 'ZYF265D(Dk=2.65, Df=0.0019)'),
        #     ('ZYF255DA', 'ZYF255DA(Dk=2.55, Df=0.0018'),
        # )
        
    SURFACE_CHOICES = (
        ('HASL', 'HASL(with lead)'),
        ('LeadFree_HASL', 'LeadFree HASL'),
        ('ENIG', 'ENIG'),
        ('OSP', 'OSP'),
    )
    GOLD_THICKNESS_CHOICES = (
        ('1U', '1 U"'),
        ('2U', '2 U"'),
    )
    OUTER_COPPER_CHOICES = (
        ('1', '1 oz'),
        ('2', '2 oz'),
        ('2.5', '2.5 oz'),
        ('3.5', '3.5 oz'),
        ('4.5', '4.5 oz'),
    )
    COVERING_CHOICES = (
        ('Tented', 'Tented'),
        ('UnTented', 'UnTented'),
        ('Plugged', 'Plugged'),
        ('Epoxy', 'Epoxy Filled & Capped'),
        ('Copper', 'Copper paste Filled & Capped'),
    )
    MIN_VIA_CHOICES = (
        ('0.3', '0.3mm/(0.4/0.45mm)'),
        ('0.25', '0.3mm/(0.35/0.4mm)'),
        ('0.2', '0.3mm/(0.3/0.35mm)'),
        ('0.315', '0.3mm/(0.25/0.3mm)'),
    )
    TOLERANCE_CHOICES = (
        ('0.2', '±0.2mm(Regular)'),
        ('0.1', '±0.1mm(Precision)'),
    )
    TEST_CHOICES = (
        ('random', 'رندوم'),
        ('fully', 'تست کامل'),
    )
    
    
    name = models.CharField(max_length=30)
    base_material = models.CharField(
        max_length=20, choices=BASE_MATERIAL_CHOICES, default='FR_4')
    layers = models.IntegerField()
    substrate_type = models.CharField(
        max_length=20, choices=SUBSTRATE_TYPE_CHOICES, default='25µm', null=True,  blank=True)

    dimension_x = models.IntegerField()
    dimension_y = models.IntegerField()
    grid_x = models.IntegerField(null=True)
    grid_y = models.IntegerField(null=True)
    dimension_unit = models.CharField(max_length=20,
                                      choices=UNIT_CHOICES, default='mm')
    qty = models.CharField(max_length=20,
                           choices=QTY_CHOICES, default='5')
    product_type = models.CharField(max_length=20,
                                    choices=PRODUCT_TYPE_CHOICES, default='industrial')
    panel = models.BooleanField()
    PCB_thickness = models.CharField(max_length=20,
                                     choices=THICKNESS_CHOICES, default='0.4')
    PCB_color = models.CharField(
        max_length=20, choices=COLOR_CHOICES, default='green')
    silkscreen = models.CharField(
        max_length=20, choices=COLOR_CHOICES, default='white')
    surface_finish = models.CharField(
        max_length=20, choices=SURFACE_CHOICES, default='HASL')
    gold_thickness = models.CharField(max_length=20,
                                      choices=GOLD_THICKNESS_CHOICES, default='1U')
    outer_copper_weight = models.CharField(max_length=20,
                                           choices=OUTER_COPPER_CHOICES, default='1')
    via_covering = models.CharField(max_length=20,
                                    choices=COVERING_CHOICES, default='Tented')
    min_via = models.CharField(
        max_length=20, choices=MIN_VIA_CHOICES, default='0.3')
    board_outline_tolerance = models.CharField(max_length=20,
                                               choices=TOLERANCE_CHOICES, default='0.2')
    electrical_test = models.CharField(
        max_length=20, choices=TEST_CHOICES, default='random')
    
    description = models.TextField(verbose_name="توضیحات پروژه", blank=True)
    state = models.CharField(
        max_length=20, choices=STATE_CHOICES, default='pending')
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="orders",null=True)
    created_at = models.DateTimeField(null=True,verbose_name="تاریخ ایجاد")
    is_deleted = models.BooleanField(default=False)


    def priority_colors(self):
        colors = {
            'urgent': '#dc3545',
            'high': '#fd7e14',
            'medium': '#ffc107',
            'low': '#20c997'
        }

        hex_color = colors.get(self.priority, '#6c757d')

        return {
            "text": hex_color,
            "bg": hex_to_rgba(hex_color, 0.1)
        }

    def __str__(self):
        return f'{self.name} - {self.user.user.get_full_name}'
    