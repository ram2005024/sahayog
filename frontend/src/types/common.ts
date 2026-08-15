export type SuccessResponse<T> = {
  success: boolean;
  message: string;
  data: T;
};
export type ErrorResponse<T> = {
  success: boolean;
  message: string;
  error_code: string;
  details: T;
};
