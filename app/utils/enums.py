from enum import StrEnum, auto


class VerifyServices(StrEnum):
    email = auto()
    apple = auto()
    bitbucket = auto()
    discord = auto()
    facebook = auto()
    fitbit = auto()
    github = auto()
    gitlab = auto()
    google = auto()
    kakao = auto()
    line = auto()
    linkedin = auto()
    microsoft = auto()
    naver = auto()
    notion = auto()
    soundcloud = auto()
    spotify = auto()
    tidal = auto()
    twitter = auto()


class Term(StrEnum):
    Fall = auto()
    Spring = auto()
    Summer = auto()


class EnrollmentStatus(StrEnum):
    enrolled = auto()
    withdrawn = auto()


class ProgramLevel(StrEnum):
    Bachelor = auto()
    Master =auto()
    PhD = auto()


class PaymentStatus(StrEnum):
    pending = auto()
    paid = auto()
    overdue = auto()


