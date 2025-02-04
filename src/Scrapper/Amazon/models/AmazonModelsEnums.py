from enum import Enum

class LANGUAGE(Enum):
    Spanish = "es"
    English = "en"
    French = "fr"
    German = "de"
    Italian = "it"
    Japan = "jp"
    Chinese = "cn"
    Portuguese = "pt"

class CATEGORY(Enum):
    Electronics = "electronics"
    Toys = "toys"
    Computers = "computers"
    Books = "books"
    Fashion = "fashion"
    Home = "home-garden"
    Sports = "sports"
    Cars = "automotive"

class CONDITION(Enum):
    New = "2224371011"
    Used = "2224369011"
    Refurbished = "2224373011"