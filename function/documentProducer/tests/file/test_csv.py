from file import csv


def get_lines() -> list:
    return ["\ufeff100006,Zollner Electronic Taicang Co Ltd       ,4502937213-734-041  ,2/27/19,SINGLE COLOR LED              ,3013853,1,10000,0.01993,0.0188,0,H2,804,LTST-C191KGKT            ,LTO   ,1770387-00               ,4016616,3015725,39,DHL INT'L      ,DHL#1738502581           ,5015430,CN \r\n",
            '100006,Zollner Electronic Taicang Co Ltd       ,4502930267-734-041  ,2/27/19,"SINGLE COLOR LED, RED, 1.2mm  ",3013793,2,4000,0.02173,0.0205,0,H2,804,LTST-S270KRKT            ,LTO   ,1768401-00               ,4016640,3016416,39,DHL INT\'L      ,DHL#1738502581           ,5015437,CN \r\n',
            '100006,Zollner Electronic Taicang Co Ltd       ,4502992302-708-041  ,2/27/19,FAN MB WITH CABLE             ,3014465,1,0,0,0,0,H2,804,XF-65654                 ,SAY   ,2017367-00               ,0,3016254,,,,5015312, \r\n',
            '91609,ZOLLNER ELEKTRONIK AG                   ,4502911101-784-011  ,2/27/19,3.3V SINGLE POWER SUPPLY 10/10,3013590,1,0,0,0,0,HK,804,KSZ8721BLI-TR            ,MCP   ,1684199-00               ,0,3016243,,,,5015323,']


def get_parsed_lines() -> list:
    """ Data just to get you familiar with what's expected (what the data looks like) """
    return [
        ['\ufeff100006', 'Zollner Electronic Taicang Co Ltd       ', '4502937213-734-041  ', '2/27/19',
         'SINGLE COLOR LED              ', '3013853', '1', '10000', '0.01993', '0.0188', '0', 'H2', '804',
         'LTST-C191KGKT            ', 'LTO   ', '1770387-00               ', '4016616', '3015725', '39',
         "DHL INT'L      ", 'DHL#1738502581           ', '5015430', 'CN '],
        ['100006', 'Zollner Electronic Taicang Co Ltd       ', '4502930267-734-041  ', '2/27/19',
         'SINGLE COLOR LED, RED, 1.2mm  ', '3013793', '2', '4000', '0.02173', '0.0205', '0', 'H2', '804',
         'LTST-S270KRKT            ', 'LTO   ', '1768401-00               ', '4016640', '3016416', '39',
         "DHL INT'L      ", 'DHL#1738502581           ', '5015437', 'CN '],
        ['100006', 'Zollner Electronic Taicang Co Ltd       ', '4502992302-708-041  ', '2/27/19',
         'FAN MB WITH CABLE             ', '3014465', '1', '0', '0', '0', '0', 'H2', '804', 'XF-65654                 ',
         'SAY   ', '2017367-00               ', '0', '3016254', None, None, None, '5015312', None],
        ['91609', 'ZOLLNER ELEKTRONIK AG                   ', '4502911101-784-011  ', '2/27/19',
         '3.3V SINGLE POWER SUPPLY 10/10', '3013590', '1', '0', '0', '0', '0', 'HK', '804', 'KSZ8721BLI-TR            ',
         'MCP   ', '1684199-00               ', '0', '3016243', None, None, None, '5015323', None]
    ]


def get_failed_parsed_lines() -> list:
    """ Data just to get you familiar with what's expected (what the data looks like) """
    return [
        ['\ufeff100006', 'Zollner Electronic Taicang Co Ltd       ', '4502937213-734-041  ', '2/27/19',
         'SINGLE COLOR LED              ', '3013853', '1', '10000', '0.01993', '0.0188', '0', 'H2', '804',
         'LTST-C191KGKT            ', 'LTO   ', '1770387-00               ', '4016616', '3015725', '39',
         "DHL INT'L      ", 'DHL#1738502581           ', '5015430', 'CN '],
        ['100006', 'Zollner Electronic Taicang Co Ltd       ', '4502930267-734-041  ', '2/27/19',
         'SINGLE COLOR LED, RED, 1.2mm  ', '3013793', '2', '4000', '0.02173', '0.0205', '0', 'H2', '804',
         'LTST-S270KRKT            ', 'LTO   ', '1768401-00               ', '4016640', '3016416', '39',
         "DHL INT'L      ", 'DHL#1738502581           ', '5015437', 'CN '],
        ['100006', 'Zollner Electronic Taicang Co Ltd       ', '4502992302-708-041  ', '2/27/19',
         'FAN MB WITH CABLE             ', '3014465', '1', '0', '0', '0', '0', 'H2', '804', 'XF-65654                 ',
         'SAY   ', '2017367-00               ', '0', '3016254', '', '', '', '5015312', ''],
        ['91609', 'ZOLLNER ELEKTRONIK AG                   ', '4502911101-784-011  ', '2/27/19',
         '3.3V SINGLE POWER SUPPLY 10/10', '3013590', '1', '0', '0', '0', '0', 'HK', '804', 'KSZ8721BLI-TR            ',
         'MCP   ', '1684199-00               ', '0', '3016243', '', '', '', '5015323', '']
    ]


def test_parse():
    lines = get_lines()
    parsed_lines = csv.parse(lines)

    assert parsed_lines == get_parsed_lines()


def test_fail_parse():
    """ check that all empty strings were parsed to None """
    lines = get_lines()
    parsed_lines = csv.parse(lines)

    assert parsed_lines != get_failed_parsed_lines()
