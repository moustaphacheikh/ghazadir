MESSAGE_STATUS_ACCEPTED       = 'accepted'
MESSAGE_STATUS_QUEUED           = 'queued'
MESSAGE_STATUS_SENDING          = 'sending'
MESSAGE_STATUS_SENT             = 'sent'
MESSAGE_STATUS_RECEIVING        = 'receiving'
MESSAGE_STATUS_RECEIVED         = 'received'
MESSAGE_STATUS_DELIVERED         = 'delivered'
MESSAGE_STATUS_UNDELIVERED      = 'undelivered'
MESSAGE_STATUS_FAILED           = 'failed'
MESSAGE_STATUS_CHOICES = (
    (MESSAGE_STATUS_ACCEPTED, 'Accepted'),
    (MESSAGE_STATUS_QUEUED, 'Queued'),
    (MESSAGE_STATUS_SENDING, 'Sending'),
    (MESSAGE_STATUS_SENT, 'Sent'),
    (MESSAGE_STATUS_RECEIVING, 'Receiving'),
    (MESSAGE_STATUS_RECEIVED, 'Received'),
    (MESSAGE_STATUS_DELIVERED, 'Delivered'),
    (MESSAGE_STATUS_UNDELIVERED, 'Undelivered'),
    (MESSAGE_STATUS_FAILED, 'Failed'),
)
STATUS = [MESSAGE_STATUS_ACCEPTED ,
MESSAGE_STATUS_QUEUED  ,
MESSAGE_STATUS_SENDING  ,
MESSAGE_STATUS_SENT      ,
MESSAGE_STATUS_RECEIVING  ,
MESSAGE_STATUS_RECEIVED   ,
MESSAGE_STATUS_DELIVERED  ,
MESSAGE_STATUS_UNDELIVERED,
MESSAGE_STATUS_FAILED]

CITY_1 = 'نواكشوط'
CITY_2 = 'نواديبو'
CITY_3 = 'روصو'
CITY_4 = 'عدل بكرو'
CITY_5 = 'بوغي'
CITY_6 = 'كيفة'
CITY_7 = 'الزويرات'
CITY_8 = 'كيهيدي'
CITY_9 = 'بوكادوم'
CITY_10 = 'بوتلميت'
CITY_11 = 'أطار'
CITY_12 = 'برينة'
CITY_13 = 'غابو'
CITY_14 = 'حمود'
CITY_15 = 'مال'
CITY_16 = 'نبيكا'
CITY_17 = 'جوراي'
CITY_18 = 'تمبدغة'
CITY_19 = 'مقطع الحجار'
CITY_22 = 'كرو'
CITY_23 = 'سودود'
CITY_24 = 'سيليبابي'
CITY_25 = 'فوم ليكليت'
CITY_26 = 'لقصيبة'
CITY_27 = 'بوصطيلة'
CITY_28 = 'صنكرافة'
CITY_29 = 'طينطان'
CITY_30 = 'ألاك'
CITY_31 = 'تجكجة'
CITY_32 = 'ولاتة'
CITY_33 = 'العيون'
CITY_34 = 'بابابى'
CITY_34 = 'أكجوجت'
CITY_35 = 'شكار'
CITY_36 = 'النعمة'

CITY_CHOICES = (
(CITY_1 , 'نواكشوط'),
(CITY_2 , 'نواديبو'),
(CITY_3 , 'روصو'),
(CITY_4 , 'عدل بكرو'),
(CITY_5 , 'بوغي'),
(CITY_6 , 'كيفة'),
(CITY_7 , 'الزويرات'),
(CITY_8 , 'كيهيدي'),
(CITY_9 , 'بوكادوم'),
(CITY_10 , 'بوتلميت'),
(CITY_11 , 'أطار'),
(CITY_12 , 'برينة'),
(CITY_13 , 'غابو'),
(CITY_14 , 'حمود'),
(CITY_15 , 'مال'),
(CITY_16 , 'نبيكا'),
(CITY_17 , 'جوراي'),
(CITY_18 , 'تمبدغة'),
(CITY_19 , 'مقطع الحجار'),
(CITY_22 , 'كرو'),
(CITY_23 , 'سودود'),
(CITY_24 , 'سيليبابي'),
(CITY_25 , 'فوم ليكليت'),
(CITY_26 , 'لقصيبة'),
(CITY_27 , 'بوصطيلة'),
(CITY_28 , 'صنكرافة'),
(CITY_29 , 'طينطان'),
(CITY_30 , 'ألاك'),
(CITY_31 , 'تجكجة'),
(CITY_32 , 'ولاتة'),
(CITY_33 , 'العيون'),
(CITY_34 , 'بابابى'),
(CITY_34 , 'أكجوجت'),
(CITY_35 , 'شكار'),
(CITY_36 , 'النعمة'),
    )

CITIES = [c[0] for c in CITY_CHOICES]
