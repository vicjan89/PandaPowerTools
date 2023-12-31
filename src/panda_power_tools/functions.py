import json


import pandapower as pp



def create_net(source_data):
    #Создание расчётной сети PandaPower
    net = pp.create_empty_network(source_data['name'])
    # Создание стандартных типов
    with open('../../../ElectricNetsCalc/std_lines.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    pp.create_std_types(net, data, element='line', overwrite=True, check_required=True)
    with open('../../../ElectricNetsCalc/std_trafos.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    pp.create_std_types(net, data, element='trafo', overwrite=True, check_required=True)
    with open('../../../ElectricNetsCalc/std_trafos3w.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    pp.create_std_types(net, data, element='trafo3w', overwrite=True, check_required=True)

    for item in source_data.get('buses', []):
        pp.create_bus(net=net, **item)
    for item in source_data.get('ext_grid', []):
        pp.create_ext_grid(net=net, **item)
    for item in source_data.get('lines', []):
        name1 = net.bus.at[item['from_bus'], 'name']
        name2 =  net.bus.at[item['to_bus'], 'name']
        pp.create_line(net=net, **item, name=name1+' - '+name2)
    for item in source_data.get('trafos', []):
        pp.create_transformer(net=net, **item)
    for item in source_data.get('trafos3w', []):
        pp.create_transformer3w(net=net, **item)
    for item in source_data.get('shunt', []):
        pp.create_shunt(net=net, **item)
    for item in source_data.get('switch', []):
        pp.create_switch(net=net, **item)

    return net

def define_c(u: float, case: str, lv_tol_percent: int) -> tuple[float, float]:
    '''
    Определяет коэффициент коррекции напряжения по IEC60909
    :param u: корректируемое напряжение
    :param case: режим работы энергосистемы 'min' или 'max'
    :param lv_tol_percent: допуск 10% или 6%
    :return: (cmin, cmax)
    '''
    if case not in ('max', 'min') or lv_tol_percent not in (6, 10) or u < 0:
        raise UserWarning("Неправильные параметры для определения коэффициента коррекции напряжения c")
    if u <= 1:
        cmin = 0.95
        if lv_tol_percent == 10:
            cmax = 1.1
        else:
            cmax = 1.05
    else:
        cmin = 1.0
        cmax = 1.1
    return cmin, cmax




