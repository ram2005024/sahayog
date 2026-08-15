import { IncidentCreatePayload } from "@/schemas/incident.schema";

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
export type UploadedMedia = {
  type: string;
  url: string;
  meta_data: {
    public_id: string;
    url: string;
    format: string;
    size: number;
    width: number;
    height: number;
  };
};
export type IncidentRequest = Omit<
  IncidentCreatePayload,
  "images" | "audio"
> & {
  medias?: UploadedMedia[];
};
