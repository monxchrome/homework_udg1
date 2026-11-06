import csv
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Iterable, Protocol


@dataclass(frozen=True)
class Reservation:
    name: str
    nights: int
    price: Decimal

    @property
    def total(self) -> Decimal:
        return self.nights * self.price


class ReservationSource(Protocol):
    def load(self) -> Iterable[Reservation]:
        ...


class CSVSource:
    def __init__(self, path: str):
        self.path = Path(path)

    def load(self) -> Iterable[Reservation]:
        with self.path.open(newline="", encoding="utf-8") as file:
            for name, nights, price in csv.reader(file):
                yield Reservation(name.strip(), int(nights), Decimal(price.strip()))


class MemorySource:
    def __init__(self, reservations: Iterable[Reservation]):
        self.reservations = tuple(reservations)

    def load(self) -> Iterable[Reservation]:
        return iter(self.reservations)


def calculate_totals(reservations: Iterable[Reservation]) -> tuple[Decimal, ...]:
    return tuple(reservation.total for reservation in reservations)


class ReservationEngine:
    def __init__(self, source: ReservationSource):
        self.source = source

    def run(self) -> tuple[Decimal, ...]:
        return calculate_totals(self.source.load())


class TextR:
    def __init__(self, path: str = "report.txt"):
        self.path = Path(path)

    def save(self, totals: Iterable[Decimal]) -> None:
        self.path.write_text("\n".join(map(str, totals)), encoding="utf-8")


class ConsoleNotify:
    def send(self, totals: Iterable[Decimal]) -> None:
        print(f"Sent: {sum(totals, Decimal('0')):.2f} EUR")


if __name__ == "__main__":
    source = MemorySource([
        Reservation("Hotel A", 2, Decimal("50.00")),
        Reservation("Hotel B", 3, Decimal("40.00")),
        Reservation("Hotel C", 1, Decimal("75.50")),
    ])
    totals = ReservationEngine(source).run()
    TextR().save(totals)
    ConsoleNotify().send(totals)
