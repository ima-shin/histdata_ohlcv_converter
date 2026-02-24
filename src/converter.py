import argparse
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
COLUMNS = ["DateTime", "Open", "High", "Low", "Close", "Volume"]
DT_FORMAT = "%Y%m%d %H%M%S"


def convert_symbol(symbol_dir: Path) -> None:
    symbol = symbol_dir.name
    csv_files = sorted(symbol_dir.glob("*.csv"))
    if not csv_files:
        print(f"[{symbol}] No CSV files found, skipping.")
        return

    frames = []
    for f in csv_files:
        df = pd.read_csv(f, sep=";", header=None, names=COLUMNS)
        frames.append(df)

    data = pd.concat(frames, ignore_index=True)
    data["DateTime"] = pd.to_datetime(data["DateTime"], format=DT_FORMAT)
    data = data.set_index("DateTime").sort_index()

    m15 = data.resample("15min").agg(
        Open=("Open", "first"),
        High=("High", "max"),
        Low=("Low", "min"),
        Close=("Close", "last"),
        Volume=("Volume", "sum"),
    )
    m15 = m15.dropna(how="all")

    out_dir = OUTPUT_DIR / symbol
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{symbol}_M15.csv"

    m15.index = m15.index.strftime(DT_FORMAT)
    m15.to_csv(out_file, sep=";", header=False)
    print(f"[{symbol}] Written {len(m15)} M15 bars -> {out_file}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert M1 OHLCV CSV to M15. "
                    "Pass one or more symbol directories (e.g. data/eurjpy). "
                    "If omitted, all subdirectories under data/ are processed."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        metavar="PATH",
        help="Path(s) to symbol directory (e.g. data/eurjpy data/eurusd)",
    )
    args = parser.parse_args()

    if args.paths:
        symbol_dirs = args.paths
    else:
        symbol_dirs = sorted(d for d in DATA_DIR.iterdir() if d.is_dir())
        if not symbol_dirs:
            print("No symbol directories found under data/")
            return

    for symbol_dir in symbol_dirs:
        symbol_dir = Path(symbol_dir)
        if not symbol_dir.is_dir():
            print(f"[{symbol_dir}] Directory not found, skipping.")
            continue
        convert_symbol(symbol_dir)


if __name__ == "__main__":
    main()
