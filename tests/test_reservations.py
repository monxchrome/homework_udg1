from decimal import Decimal

from reservations import CSVSource, MemorySource, Reservation, ReservationEngine, TextR


class FakeSource:
    def load(self):
        yield Reservation("Hotel A", 2, Decimal("50.00"))
        yield Reservation("Hotel B", 3, Decimal("40.00"))


def test_engine_with_fake_source():
    result = ReservationEngine(FakeSource()).run()
    assert result == (Decimal("100.00"), Decimal("120.00"))
    assert sum(result) == Decimal("220.00")


def test_engine_with_memory_source():
    source = MemorySource([Reservation("Hotel C", 1, Decimal("75.50"))])
    assert ReservationEngine(source).run() == (Decimal("75.50"),)


def test_engine_with_csv_source(tmp_path):
    path = tmp_path / "reservations.csv"
    path.write_text("Hotel A,2,50.00\nHotel B,3,40.00\n", encoding="utf-8")
    assert ReservationEngine(CSVSource(str(path))).run() == (
        Decimal("100.00"), Decimal("120.00")
    )


def test_text_report(tmp_path):
    path = tmp_path / "report.txt"
    TextR(str(path)).save([Decimal("100.00"), Decimal("120.00")])
    assert path.read_text(encoding="utf-8") == "100.00\n120.00"
