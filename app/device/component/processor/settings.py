from app.device.benchmark_settings import BenchmarkProcessor
from app.device.component.settings import Component, ComponentSubSettings
from app.schema import UnitCodes



class Processor(Component):
    numberOfCores = {
        'type': 'integer',
        'min': 1,
        'sink': 1
    }
    speed = {
        'type': 'float',
        'unitCode': UnitCodes.ghz,
        'sink': 1
    }
    address = {
        'type': 'integer',
        'unitCode': UnitCodes.bit,
        'allowed': {8, 16, 32, 64, 128, 256},
        'sink': -1
    }
    benchmark = {
        'type': 'dict',
        'schema': BenchmarkProcessor,
        'writeonly': True,
    }
    benchmarks = {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': BenchmarkProcessor
        },
        'readonly': True
    }


class ProcessorSettings(ComponentSubSettings):
    _schema = Processor
