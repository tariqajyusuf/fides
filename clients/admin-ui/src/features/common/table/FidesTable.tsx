import {
  ArrowDownIcon,
  ArrowUpIcon,
  Box,
  Flex,
  Table,
  TableContainer,
  Tbody,
  Td,
  Text,
  Th,
  Thead,
  Tr,
} from "@fidesui/react";
import React, { MutableRefObject, ReactNode, useEffect, useMemo } from "react";
import {
  Column,
  Hooks,
  TableInstance,
  TableState,
  useGlobalFilter,
  useSortBy,
  useTable,
} from "react-table";

import GlobalFilter from "~/features/datamap/datamap-table/filters/global-accordion-filter/global-accordion-filter";

export interface FidesObject {
  id?: string;
  name?: string;
}

type Props<T extends FidesObject> = {
  columns: Column<T>[];
  data: T[];
  showSearchBar?: boolean;
  searchBarPlaceHolder?: string;
  searchBarRightButton?: ReactNode;
  footer?: ReactNode;
  onRowClick?: (row: T) => void;
  customHooks?: Array<(hooks: Hooks<T>) => void>;
  tableInstanceRef?: MutableRefObject<TableInstance<T> | undefined>;
  initialState?: Partial<TableState<T>>;
};

export const FidesTable = <T extends FidesObject>({
  columns,
  data,
  showSearchBar,
  searchBarPlaceHolder,
  searchBarRightButton,
  footer,
  onRowClick,
  customHooks,
  tableInstanceRef,
  initialState,
}: Props<T>) => {
  const plugins = useMemo(() => {
    if (customHooks) {
      return [useGlobalFilter, useSortBy, ...customHooks];
    }
    return [useGlobalFilter, useSortBy];
  }, [customHooks]);

  const tableInstance = useTable(
    {
      columns,
      data,
      autoResetSortBy: false,
      initialState: initialState !== undefined ? initialState : {},
    },
    ...plugins
  );
  useEffect(() => {
    if (tableInstanceRef) {
      /* eslint-disable no-param-reassign */
      tableInstanceRef.current = tableInstance;
    }
  }, [tableInstance, tableInstanceRef]);

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
    tableInstance;

  return (
    <Box height="inherit">
      {showSearchBar ? (
        <Flex flexGrow={1} marginBottom={3} justifyContent="space-between">
          <GlobalFilter
            globalFilter={tableInstance.state.globalFilter}
            setGlobalFilter={tableInstance.setGlobalFilter}
            placeholder={searchBarPlaceHolder}
          />
          {searchBarRightButton || null}
        </Flex>
      ) : null}
      <TableContainer
        height="inherit"
        overflowY="auto"
        border="1px solid"
        boxSizing="border-box"
        borderColor="gray.200"
        borderRadius="6px 6px 0px 0px"
      >
        <Table {...getTableProps()} fontSize="sm">
          <Thead position="sticky" top="0" backgroundColor="gray.50">
            {headerGroups.map((headerGroup) => {
              const { key: headerRowKey, ...headerGroupProps } =
                headerGroup.getHeaderGroupProps();
              return (
                <Tr key={headerRowKey} {...headerGroupProps}>
                  {headerGroup.headers.map((column) => {
                    const { key: columnKey, ...headerProps } =
                      column.getHeaderProps(column.getSortByToggleProps());
                    let sortIcon: ReactNode = null;
                    if (column.isSorted) {
                      sortIcon = column.isSortedDesc ? (
                        <ArrowDownIcon color="gray.500" />
                      ) : (
                        <ArrowUpIcon color="gray.500" />
                      );
                    }

                    return (
                      <Th
                        key={columnKey}
                        {...headerProps}
                        textTransform="none"
                        fontSize="sm"
                        p={4}
                        data-testid={`column-${column.Header}`}
                      >
                        <Text
                          _hover={{ backgroundColor: "gray.100" }}
                          p={1}
                          borderRadius="4px"
                          pr={sortIcon ? 0 : 3.5}
                        >
                          {column.render("Header")}
                          {sortIcon}
                        </Text>
                      </Th>
                    );
                  })}
                </Tr>
              );
            })}
          </Thead>
          <Tbody {...getTableBodyProps()}>
            {rows.map((row) => {
              prepareRow(row);
              const { key: rowKey, ...rowProps } = row.getRowProps();
              const rowName = row.original.name;
              const rowId = row.original.id;
              return (
                <Tr
                  key={rowKey}
                  {...rowProps}
                  _hover={
                    onRowClick
                      ? { backgroundColor: "gray.50", cursor: "pointer" }
                      : undefined
                  }
                  data-testid={`row-${rowName ?? rowId}`}
                >
                  {row.cells.map((cell) => {
                    const { key: cellKey, ...cellProps } = cell.getCellProps();
                    return (
                      <Td
                        key={cellKey}
                        {...cellProps}
                        p={5}
                        verticalAlign="baseline"
                        width={cell.column.width}
                        onClick={
                          cell.column.Header !== "Enable" && onRowClick
                            ? () => {
                                onRowClick(row.original);
                              }
                            : undefined
                        }
                      >
                        {cell.render("Cell")}
                      </Td>
                    );
                  })}
                </Tr>
              );
            })}
          </Tbody>
          {footer}
        </Table>
      </TableContainer>
    </Box>
  );
};
