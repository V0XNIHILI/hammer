#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  library_filter.py
#  hammer-tech library filter.
#
#  See LICENSE for licence details.

from numbers import Number
from typing import TYPE_CHECKING, Any, Callable, List, NamedTuple, Optional, Tuple, Union

from hammer_utils import get_or_else, assert_function_type

if TYPE_CHECKING:
    # grumble grumble, we need a better Library class generator
    # Here is a stub class for type checking purposes only
    from hammer_tech import LibraryPrefix, SpiceModelFile
    class Library:
        @property
        def extra_prefixes(self) -> List[LibraryPrefix]: pass
        @property
        def ecsm_liberty_file(self) -> Optional[str]: pass
        @property
        def gds_file(self) -> Optional[str]: pass
        @property
        def spice_file(self) -> Optional[str]: pass
        @property
        def verilog_synth(self) -> Optional[str]: pass
        @property
        def verilog_sim(self) -> Optional[str]: pass
        @property
        def spice_model_file(self) -> Optional[SpiceModelFile]: pass
        @property
        def power_grid_library(self) -> Optional[str]: pass
        @property
        def klayout_techfile(self) -> Optional[str]: pass

PathsFunctionType = Callable[["Library"], List[str]]


def check_paths_func(func: PathsFunctionType) -> None:
    """
    Check that the given function obeys the paths_func type specification.
    """
    assert_function_type(func, ["Library"], List[str])  # type: ignore


ExtractionFunctionType = Callable[["Library", List[str]], List[str]]


def check_extraction_func(func: ExtractionFunctionType) -> None:
    """
    Check that the given function obeys the paths_func type specification.
    """
    assert_function_type(func, ["Library", List[str]], List[str])  # type: ignore


def check_filter_func(func: Callable[["Library"], bool]) -> None:
    """
    Check that the given function obeys the filter_func type specification.
    """
    assert_function_type(func, ["Library"], bool)  # type: ignore


class LibraryFilter(NamedTuple('LibraryFilter', [
    ('tag', str),
    ('description', str),
    # Is the resulting string intended to be a file?
    ('is_file', bool),
    # Function to extract desired path(s) out of the library.
    # Returns a list of library-relative paths.
    ('paths_func', PathsFunctionType),
    # Function to extract desired string(s) out of the library, given full
    # paths and the Library.
    # Returns a list of strings.
    ('extraction_func', Optional[ExtractionFunctionType]),
    # Additional filter function to use to exclude possible libraries.
    ('filter_func', Optional[Callable[["Library"], bool]]),
    # Sort function to control the order in which outputs are listed
    ('sort_func', Optional[Callable[["Library"], Union[Number, str, tuple]]]),
    # List of functions to call on the list-level (the list of elements generated by func) before output and
    # post-processing.
    ('extra_post_filter_funcs', List[Callable[[List[str]], List[str]]])
])):
    """
    "Library" filter containing a filtering function, identifier tag, and a short
    human-readable description.
    """
    __slots__ = ()

    @staticmethod
    def new(
            tag: str, description: str, is_file: bool,
            paths_func: PathsFunctionType,
            extraction_func: Optional[ExtractionFunctionType] = None,
            filter_func: Optional[Callable[["Library"], bool]] = None,
            sort_func: Optional[Callable[["Library"], Union[Number, str, tuple]]] = None,
            extra_post_filter_funcs: Optional[List[Callable[[List[str]], List[str]]]] = None) -> "LibraryFilter":
        """Convenience "constructor" with some default arguments."""

        check_paths_func(paths_func)
        if extraction_func is not None:
            check_extraction_func(extraction_func)
        if filter_func is not None:
            check_filter_func(filter_func)

        return LibraryFilter(
            tag, description, is_file,
            paths_func,
            extraction_func,
            filter_func,
            sort_func,
            list(get_or_else(extra_post_filter_funcs, []))
        )
