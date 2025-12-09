from .base import ChaosSystem
from .continuous.lorenz import Lorenz
from .continuous.rossler import Rossler
from .continuous.chua import Chua
from .continuous.duffing import Duffing
from .continuous.rabinovich_fabrikant import RabinovichFabrikant
from .continuous.arneodo import Arneodo
from .continuous.thomas import Thomas
from .continuous.lorenz84 import Lorenz84
from .continuous.chen import Chen
from .continuous.lu import Lu
from .continuous.halvorsen import Halvorsen
from .continuous.rucklidge import Rucklidge
from .continuous.sprott import Sprott
from .continuous.nose_hoover import NoseHoover
from .continuous.dadras import Dadras
from .continuous.dequan_li import DequanLi
from .continuous.four_wing import FourWing
from .continuous.finance import Finance
from .continuous.qi import Qi
from .continuous.wang import Wang
from .continuous.shimizu_morioka import ShimizuMorioka
from .continuous.tigan import Tigan
from .continuous.bouali import Bouali
from .continuous.newton_leipnik import NewtonLeipnik

from .discrete.logistic import Logistic
from .discrete.henon import Henon
from .discrete.tent import Tent
from .discrete.ikeda import Ikeda
from .discrete.gingerbread_man import GingerbreadMan
from .discrete.clifford import Clifford
from .discrete.dejong import DeJong
from .discrete.sine_map import SineMap
from .discrete.circle_map import CircleMap
from .discrete.standard_map import StandardMap
from .discrete.baker_map import BakerMap
from .discrete.cat_map import CatMap
from .discrete.logistic_cubic import LogisticCubic
from .discrete.gauss_map import GaussMap
from .discrete.sawtooth_map import SawtoothMap
from .discrete.bernoulli_map import BernoulliMap
from .discrete.lyapunov_map import LyapunovMap
from .discrete.chebyshev_map import ChebyshevMap

from .delay.mackey_glass import MackeyGlass
from .delay.ikeda_delay import IkedaDelay
from .delay.lang_kobayashi import LangKobayashi

from .fractional.fractional_lorenz import FractionalLorenz
from .fractional.fractional_chen import FractionalChen
from .fractional.fractional_lu import FractionalLu

from .hyperchaotic.hyper_lorenz import HyperLorenz
from .hyperchaotic.hyper_chen import HyperChen
from .hyperchaotic.hyper_lu import HyperLu
from .hyperchaotic.riki_hyperchaos import RikiHyperchaos
from .hyperchaotic.hyper_rossler import HyperRossler

CHAOS_SYSTEMS = {
    "lorenz": Lorenz,
    "rossler": Rossler,
    "chua": Chua,
    "duffing": Duffing,
    "rabinovich_fabrikant": RabinovichFabrikant,
    "arneodo": Arneodo,
    "thomas": Thomas,
    "lorenz84": Lorenz84,
    "chen": Chen,
    "lu": Lu,
    "halvorsen": Halvorsen,
    "rucklidge": Rucklidge,
    "sprott": Sprott,
    "nose_hoover": NoseHoover,
    "dadras": Dadras,
    "dequan_li": DequanLi,
    "four_wing": FourWing,
    "finance": Finance,
    "qi": Qi,
    "wang": Wang,
    "shimizu_morioka": ShimizuMorioka,
    "tigan": Tigan,
    "bouali": Bouali,
    "newton_leipnik": NewtonLeipnik,
    "logistic": Logistic,
    "henon": Henon,
    "tent": Tent,
    "ikeda": Ikeda,
    "gingerbread_man": GingerbreadMan,
    "clifford": Clifford,
    "dejong": DeJong,
    "sine_map": SineMap,
    "circle_map": CircleMap,
    "standard_map": StandardMap,
    "baker_map": BakerMap,
    "cat_map": CatMap,
    "logistic_cubic": LogisticCubic,
    "gauss_map": GaussMap,
    "sawtooth_map": SawtoothMap,
    "bernoulli_map": BernoulliMap,
    "lyapunov_map": LyapunovMap,
    "chebyshev_map": ChebyshevMap,
    "mackey_glass": MackeyGlass,
    "ikeda_delay": IkedaDelay,
    "lang_kobayashi": LangKobayashi,
    "fractional_lorenz": FractionalLorenz,
    "fractional_chen": FractionalChen,
    "fractional_lu": FractionalLu,
    "hyper_lorenz": HyperLorenz,
    "hyper_chen": HyperChen,
    "hyper_lu": HyperLu,
    "riki_hyperchaos": RikiHyperchaos,
    "hyper_rossler": HyperRossler,
}


def get_chaos_system(name, **kwargs):
    system_class = CHAOS_SYSTEMS.get(name.lower())
    if not system_class:
        raise ValueError(f"Unknown chaos system: {name}")
    return system_class(**kwargs)


def list_chaos_systems():
    return list(CHAOS_SYSTEMS.keys())


def get_system_type(system_name):
    continuous_systems = [
        "lorenz", "rossler", "chua", "duffing", "rabinovich_fabrikant", "arneodo",
        "thomas", "lorenz84", "chen", "lu", "halvorsen", "rucklidge", "sprott",
        "nose_hoover", "dadras", "dequan_li", "four_wing", "finance", "qi", "wang",
        "shimizu_morioka", "tigan", "bouali", "newton_leipnik"
    ]

    discrete_systems = [
        "logistic", "henon", "tent", "ikeda", "gingerbread_man", "clifford",
        "dejong", "sine_map", "circle_map", "standard_map", "baker_map",
        "cat_map", "logistic_cubic", "gauss_map", "sawtooth_map", "bernoulli_map",
        "lyapunov_map", "chebyshev_map"
    ]

    delay_systems = ["mackey_glass", "ikeda_delay", "lang_kobayashi"]

    fractional_systems = ["fractional_lorenz", "fractional_chen", "fractional_lu"]

    hyperchaotic_systems = [
        "hyper_lorenz", "hyper_chen", "hyper_lu", "riki_hyperchaos", "hyper_rossler"
    ]

    system_name = system_name.lower()

    if system_name in continuous_systems:
        return "continuous"
    elif system_name in discrete_systems:
        return "discrete"
    elif system_name in delay_systems:
        return "delay"
    elif system_name in fractional_systems:
        return "fractional"
    elif system_name in hyperchaotic_systems:
        return "hyperchaotic"
    else:
        return "unknown"


__all__ = [
    "ChaosSystem",
    "Lorenz", "Rossler", "Chua", "Duffing", "RabinovichFabrikant", "Arneodo",
    "Thomas", "Lorenz84", "Chen", "Lu", "Halvorsen", "Rucklidge", "Sprott",
    "NoseHoover", "Dadras", "DequanLi", "FourWing", "Finance", "Qi", "Wang",
    "ShimizuMorioka", "Tigan", "Bouali", "NewtonLeipnik",
    "Logistic", "Henon", "Tent", "Ikeda", "GingerbreadMan", "Clifford", "DeJong",
    "SineMap", "CircleMap", "StandardMap", "BakerMap", "CatMap", "LogisticCubic",
    "GaussMap", "SawtoothMap", "BernoulliMap", "LyapunovMap", "ChebyshevMap",
    "MackeyGlass", "IkedaDelay", "LangKobayashi",
    "FractionalLorenz", "FractionalChen", "FractionalLu",
    "HyperLorenz", "HyperChen", "HyperLu", "RikiHyperchaos", "HyperRossler",
    "CHAOS_SYSTEMS", "get_chaos_system", "list_chaos_systems", "get_system_type"
]
