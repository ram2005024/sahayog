export type SingleSignatureResponse = {
  signature: string;
  url: string;
  timestamp: number;
  public_id: string;
  api_key: string;

  upload_preset: string;
};

export type SignatureResponse = {
  signatures: SingleSignatureResponse[];
  exp_time: number;
};

export type SignatureAPIRequest = {
  file_length: number;
  file_types: ("image" | "audio")[];
};
