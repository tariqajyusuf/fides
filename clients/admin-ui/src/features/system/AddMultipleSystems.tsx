import {
  Box,
  Button,
  Flex,
  HStack,
  Spinner,
  Tooltip,
  useDisclosure,
  useToast,
} from "@fidesui/react";
import {
  createColumnHelper,
  getCoreRowModel,
  getFilteredRowModel,
  getSortedRowModel,
  getPaginationRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { useRouter } from "next/router";
import { useMemo, useState } from "react";

import { useAppSelector } from "~/app/hooks";
import { useFeatures } from "~/features/common/features";

import { successToastParams } from "~/features/common/toast";
import {
  FidesTableV2,
  GlobalFilterV2,
  DefaultCell,
  DefaultHeaderCell,
  IndeterminateCheckboxCell,
  TableActionBar,
  PaginationBar,
  RowSelectionBar,
  TableSkeletonLoader,
} from "~/features/common/tablev2";
import {
  DictSystems,
  selectAllDictSystems,
  useGetAllCreatedSystemsQuery,
  usePostCreatedSystemsMutation,
} from "~/features/plus/plus.slice";
import ConfirmationModal from "~/features/common/ConfirmationModal";

type MultipleSystemTable = DictSystems;

const columnHelper = createColumnHelper<MultipleSystemTable>();

type Props = {
  isSystem: boolean;
  redirectRoute: string;
};

export const AddMultipleSystemsV2 = ({ redirectRoute, isSystem }: Props) => {
  const systemText = isSystem ? "System" : "Vendor";
  const toast = useToast();
  const features = useFeatures();
  const router = useRouter();
  const { isLoading: isGetLoading } = useGetAllCreatedSystemsQuery(undefined, {
    skip: !features.dictionaryService,
  });
  const [
    postVendorIds,
    { isLoading: isPostLoading, isSuccess: isPostSuccess },
  ] = usePostCreatedSystemsMutation();

  const dictionaryOptions = useAppSelector(selectAllDictSystems);
  const [globalFilter, setGlobalFilter] = useState();
  const { isOpen, onClose, onOpen } = useDisclosure();

  const allRowsAdded = dictionaryOptions.every((d) => d.linked_system);
  const columns = useMemo(
    () => [
      columnHelper.display({
        id: "select",
        header: ({ table }) => (
          <IndeterminateCheckboxCell
            {...{
              checked: table.getIsAllRowsSelected(),
              indeterminate: table.getIsSomeRowsSelected(),
              onChange: table.getToggleAllRowsSelectedHandler(),
              manualDisable: allRowsAdded,
            }}
          />
        ),
        cell: ({ row }) => (
          <IndeterminateCheckboxCell
            {...{
              checked: row.getIsSelected(),
              disabled: !row.getCanSelect(),
              indeterminate: row.getIsSomeSelected(),
              onChange: row.getToggleSelectedHandler(),
              initialValue: row.original.linked_system,
            }}
          />
        ),
      }),
      columnHelper.accessor((row) => row.legal_name, {
        id: "legal_name",
        cell: (props) => <DefaultCell value={props.getValue()} />,
        header: (props) => <DefaultHeaderCell value={systemText} {...props} />,
      }),
    ],
    [allRowsAdded]
  );

  const rowSelection = useMemo(() => {
    const rowSelection: Record<string, boolean> = {};
    dictionaryOptions.forEach((ds, index) => {
      if (ds.linked_system) {
        rowSelection[index] = true;
      }
    });
    return rowSelection;
  }, [dictionaryOptions]);

  const tableInstance = useReactTable<MultipleSystemTable>({
    columns,
    data: dictionaryOptions,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    onGlobalFilterChange: setGlobalFilter,
    enableRowSelection: true,
    enableSorting: true,
    enableGlobalFilter: true,
    state: {
      globalFilter,
    },
    initialState: {
      rowSelection,
      pagination: {
        pageSize: 25,
      },
    },
  });

  const addVendors = async () => {
    const vendorIds = tableInstance
      .getSelectedRowModel()
      .rows.filter((r) => !r.original.linked_system)
      .map((r) => r.original.vendor_id);
    if (vendorIds.length > 0) {
      await postVendorIds(vendorIds);
      router.push(redirectRoute);
      toast(
        successToastParams(
          `Successfully added ${
            vendorIds.length
          } ${systemText.toLocaleLowerCase()}`
        )
      );
    }
  };

  const anyNewSelectedRows = tableInstance
    .getSelectedRowModel()
    .rows.some((row) => !row.original.linked_system);

  if (isPostLoading || isPostSuccess) {
    return (
      <Flex height="100%" justifyContent="center" alignItems="center">
        <Spinner />
      </Flex>
    );
  }

  if (isGetLoading) {
    return <TableSkeletonLoader rowHeight={36} numRows={15} />;
  }

  const toolTipText = allRowsAdded
    ? `All ${systemText.toLocaleLowerCase()} have already been added`
    : `Select a ${systemText.toLocaleLowerCase()} `;

  return (
    <Flex flex={1} direction="column" overflow="auto">
      <ConfirmationModal
        isOpen={isOpen}
        isCentered
        onCancel={onClose}
        onClose={onClose}
        onConfirm={addVendors}
        title="Confirmation"
        message={`You are about to add ${
          tableInstance
            .getSelectedRowModel()
            .rows.filter((r) => !r.original.linked_system).length
        } ${systemText.toLocaleLowerCase()}`}
      />
      <TableActionBar>
        <GlobalFilterV2
          globalFilter={globalFilter}
          setGlobalFilter={setGlobalFilter}
          placeholder="search"
        />
        <Tooltip
          label={toolTipText}
          shouldWrapChildren
          placement="top"
          isDisabled={
            (anyNewSelectedRows && !allRowsAdded) ||
            (anyNewSelectedRows && allRowsAdded)
          }
        >
          <Button
            onClick={onOpen}
            size="xs"
            variant="outline"
            disabled={!anyNewSelectedRows}
          >
            Add {`${systemText}s`}
          </Button>
        </Tooltip>
      </TableActionBar>
      <FidesTableV2<MultipleSystemTable>
        columns={columns}
        data={dictionaryOptions}
        tableInstance={tableInstance}
        rowActionBar={<RowSelectionBar tableInstance={tableInstance} />}
      />
      <PaginationBar tableInstance={tableInstance} />
    </Flex>
  );
};