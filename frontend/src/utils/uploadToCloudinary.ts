import { SingleSignatureResponse } from "@/types/incident.type";
import axios from "axios";

export const uploadToCloudinary = async (
  file: File,
  signature_data: SingleSignatureResponse,
) => {
  const form = new FormData();
  form.append("file", file);
  form.append("public_id", signature_data.public_id);
  form.append("upload_preset", signature_data.upload_preset);
  form.append("api_key", signature_data.api_key);
  form.append("signature", signature_data.signature);
  form.append("timestamp", signature_data.timestamp.toString());
  const res = await axios.post(signature_data.url, form, {
    headers: { "Content-Type": "multipart/form-data" },
    withCredentials: false,
  });
  return res.data;
};
