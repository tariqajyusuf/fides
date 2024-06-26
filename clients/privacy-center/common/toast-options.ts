import { UseToastOptions } from "fidesui";

const BaseToastOptions: UseToastOptions = {
  position: "top",
  duration: 5500,
};

export const ErrorToastOptions: UseToastOptions = {
  status: "error",
  ...BaseToastOptions,
};

export const ConfigErrorToastOptions: UseToastOptions = {
  title: "An error occurred while retrieving the Privacy Center config",
  ...ErrorToastOptions,
};

export const SuccessToastOptions: UseToastOptions = {
  status: "success",
  ...BaseToastOptions,
};
