from __future__ import annotations

from typing import Any

import pandas as pd
import polars as pl
import pytest

import narwhals as nw

df_pandas = pd.DataFrame({"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]})
df_polars = pl.DataFrame({"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]})
df_lazy = pl.LazyFrame({"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]})


@pytest.mark.parametrize("df_raw", [df_pandas, df_lazy])
def test_len(df_raw: Any) -> None:
    result = len(nw.LazyFrame(df_raw).collect()["a"])
    assert result == 3
    result = len(nw.to_native(nw.LazyFrame(df_raw).collect()["a"]))
    assert result == 3


@pytest.mark.parametrize("df_raw", [df_pandas, df_lazy])
def test_dtype(df_raw: Any) -> None:
    result = nw.LazyFrame(df_raw).collect()["a"].dtype
    assert result == nw.Int64
    assert result.is_numeric()


def test_dtypes() -> None:
    df = pl.DataFrame(
        {
            "a": [1],
            "b": [1],
            "c": [1],
            "d": [1],
            "e": [1],
            "f": [1],
            "g": [1],
            "h": [1],
            "i": [1],
            "j": [1],
            "k": [1],
            "l": [1],
            "m": [True],
        },
        schema={
            "a": pl.Int64,
            "b": pl.Int32,
            "c": pl.Int16,
            "d": pl.Int8,
            "e": pl.UInt64,
            "f": pl.UInt32,
            "g": pl.UInt16,
            "h": pl.UInt8,
            "i": pl.Float64,
            "j": pl.Float32,
            "k": pl.String,
            "l": pl.Datetime,
            "m": pl.Boolean,
        },
    )
    result = nw.DataFrame(df).schema
    expected = {
        "a": nw.Int64,
        "b": nw.Int32,
        "c": nw.Int16,
        "d": nw.Int8,
        "e": nw.UInt64,
        "f": nw.UInt32,
        "g": nw.UInt16,
        "h": nw.UInt8,
        "i": nw.Float64,
        "j": nw.Float32,
        "k": nw.String,
        "l": nw.Datetime,
        "m": nw.Boolean,
    }
    assert result == expected
    result_pd = nw.DataFrame(df.to_pandas()).schema
    assert result_pd == expected


def test_cast() -> None:
    df = pl.DataFrame(
        {
            "a": [1],
            "b": [1],
            "c": [1],
            "d": [1],
            "e": [1],
            "f": [1],
            "g": [1],
            "h": [1],
            "i": [1],
            "j": [1],
            "k": [1],
            "l": [1],
            "m": [True],
        },
        schema={
            "a": pl.Int64,
            "b": pl.Int32,
            "c": pl.Int16,
            "d": pl.Int8,
            "e": pl.UInt64,
            "f": pl.UInt32,
            "g": pl.UInt16,
            "h": pl.UInt8,
            "i": pl.Float64,
            "j": pl.Float32,
            "k": pl.String,
            "l": pl.Datetime,
            "m": pl.Boolean,
        },
    )
    df = nw.DataFrame(df).select(  # type: ignore[assignment]
        nw.col("a").cast(nw.Int32),
        nw.col("b").cast(nw.Int16),
        nw.col("c").cast(nw.Int8),
        nw.col("d").cast(nw.Int64),
        nw.col("e").cast(nw.UInt32),
        nw.col("f").cast(nw.UInt16),
        nw.col("g").cast(nw.UInt8),
        nw.col("h").cast(nw.UInt64),
        nw.col("i").cast(nw.Float32),
        nw.col("j").cast(nw.Float64),
        nw.col("k").cast(nw.String),
        nw.col("l").cast(nw.Datetime),
        nw.col("m").cast(nw.Int8),
        n=nw.col("m").cast(nw.Boolean),
    )
    result = df.schema
    expected = {
        "a": nw.Int32,
        "b": nw.Int16,
        "c": nw.Int8,
        "d": nw.Int64,
        "e": nw.UInt32,
        "f": nw.UInt16,
        "g": nw.UInt8,
        "h": nw.UInt64,
        "i": nw.Float32,
        "j": nw.Float64,
        "k": nw.String,
        "l": nw.Datetime,
        "m": nw.Int8,
        "n": nw.Boolean,
    }
    assert result == expected
    result_pd = nw.from_native(df.to_pandas()).schema
    assert result_pd == expected